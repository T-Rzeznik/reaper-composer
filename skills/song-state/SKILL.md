---
name: song-state
description: Persist and resume per-project song state — the creative brief, approved plan (key/tempo/time-sig/sections), the track map (track_index → role → instrument/fx indices + fx chain), and which sections are BUILT vs PENDING. Stored next to the Reaper project at <project-dir>/.reaper-composer/song-state.json. Load at the START of a compose/discover run to detect an in-progress song and offer to RESUME, at each pipeline checkpoint (after plan approval, after vst-setup, after each composed section) to save progress, and on resume to reconcile saved state against live Reaper (reaper_list_tracks / reaper_list_items) before continuing. Handles the unsaved-project case.
---

# Per-project song state (resume across sessions)

The pipeline keeps the plan, track map, and build progress only in the conversation — so a
`/clear`, a fresh context window, or a next-day session loses all of it, and the agent can't
tell what's already on the timeline. This skill checkpoints song state to disk **next to the
Reaper project**, so any later run can pick up exactly where the last one left off.

## Where state lives

```
<reaper-project-dir>/.reaper-composer/song-state.json
```

i.e. a `.reaper-composer/` sidecar dir alongside the project's `.rpp`. It travels with the
project. Use `Read`/`Write`/`Glob`; `Write` creates the `.reaper-composer` parent dir
automatically. Runtime user data — never committed to the plugin repo.

### Resolving the project dir

Call `reaper_get_project_info` (json) to get the project path.
- **Saved project** (e.g. `C:\Music\DeepHouseNight\DeepHouseNight.rpp`) → state goes at
  `C:\Music\DeepHouseNight\.reaper-composer\song-state.json`. Store the `.rpp` path in the file.
- **Unsaved / untitled project** (empty or untitled path) → **ask the user to save the project
  first** ("Save your Reaper project — File → Save — so I can checkpoint progress next to it").
  - If they save, resolve the path and proceed.
  - If they decline, fall back to `~/.reaper-composer/unsaved-projects/<timestamp>/song-state.json`
    (use the current time from `reaper_get_project_info` or any stable token — never block on
    it), and warn that resume won't auto-link to the project until they save. On a later save,
    offer to migrate that temp file into the project sidecar.

## Schema

The `track_map` mirrors `vst-setup`'s output contract, so persisting is a straight
serialization of what the agents already pass in-context.

```json
{
  "schema_version": 1,
  "project_path": "C:\\Music\\DeepHouseNight\\DeepHouseNight.rpp",
  "project_name": "DeepHouseNight",
  "created_at": "2026-06-18T13:20:00Z",
  "updated_at": "2026-06-18T14:05:00Z",
  "phase": "composing",
  "brief": {
    "genre": "deep house",
    "style": "late-night rooftop, warm and hypnotic",
    "references": ["Lane 8", "Yotto"],
    "genre_skills": ["genre-house"],
    "source": "discover"
  },
  "plan": {
    "tempo": 124,
    "key": "F minor",
    "time_signature": "4/4",
    "sections": [
      { "name": "intro", "start_bar": 1,  "length_bars": 16, "energy": 3, "instruments": ["pads","kick","hat"], "status": "built" },
      { "name": "drop",  "start_bar": 17, "length_bars": 16, "energy": 8, "instruments": ["kick","bass","lead"], "status": "pending" }
    ],
    "arrangement_notes": "Sidechain pads+bass to kick; filter-sweep the lead on the build."
  },
  "track_map": [
    {
      "track_index": 0,
      "role": "kick",
      "instrument_fx_name": "VST3i: Sitala (Decomposer)",
      "instrument_fx_index": 0,
      "fx_chain": [
        { "fx_index": 0, "name": "VST3i: Sitala (Decomposer)", "kind": "instrument" },
        { "fx_index": 1, "name": "VST3: TDR Nova (Tokyo Dawn Labs)", "kind": "eq" }
      ],
      "notes": "electronic kick, centered/mono"
    }
  ],
  "last_section_completed": "intro"
}
```

- `phase` — `planned` → `tracks_built` → `composing` → `done`. A coarse pointer to where the
  pipeline is.
- `plan.sections[].status` — `pending` or `built`. This is the per-section progress tracker.
- `fx_chain` stores both `fx_index` **and** exact `name` so reconciliation can re-find an FX
  even after indices shift (reaper-mcp indices shift down when items/FX are deleted).

## Checkpoint protocol — WHEN to save

Each checkpoint = one `Read` (to merge with what's on disk) → update fields → one `Write`,
bumping `updated_at`.

- **After the arranger's plan is approved** → write `brief` + `plan` with every section
  `status: "pending"`; `phase: "planned"`.
- **After vst-setup returns the track map** → write `track_map`; `phase: "tracks_built"`.
- **After the composer finishes each section** → flip that section to `status: "built"`, set
  `last_section_completed`, `phase: "composing"`. (This is the checkpoint the composer
  currently never does — it's what makes resume possible.)
- **When the song is finished** → `phase: "done"`.

## Resume protocol — on load at the start of a run

1. Resolve the project dir and `Read` `song-state.json`.
   - **Absent** → fresh song; proceed through the normal pipeline.
   - **Present** → summarize it to the user and offer a choice, e.g.:
     > "Found an in-progress song next to this project: **deep house, F minor, 124 BPM —
     > 4 of 7 sections built.** Resume where it left off, or start fresh?"
2. **Project identity check.** Compare `reaper_get_project_info`'s path to the saved
   `project_path`. If they differ (project renamed/moved, or this is a different project that
   happens to have a sidecar), warn and confirm before resuming.
3. **Reconcile with live Reaper before continuing — live Reaper is the source of truth.** The
   saved file can drift if the user edited manually.
   - `reaper_list_tracks`: verify each `track_map` entry's `track_index` still exists with the
     expected role/name. If tracks shifted, remap indices using the stored exact FX names; if a
     track is gone, note it (vst-setup may need to rebuild it).
   - `reaper_list_items`: for every section marked `built`, confirm it actually has items on the
     timeline. If a built section's items are gone, **re-mark it `pending`** so it gets rebuilt.
   - Patch the in-memory state to match reality, then `Write` the corrected file.
4. Hand the reconciled plan + track map to the composer, which composes **only the PENDING
   sections** (skipping built ones).

## Boundaries

This skill owns build/compositional progress. The `mix-engineer` may *read* this file for
genre/loudness context but must **never write** to it — mixing is not tracked as build progress.
