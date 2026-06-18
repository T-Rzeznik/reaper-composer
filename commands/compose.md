---
description: The one command — generate a full song in Reaper from a plain-English request. Runs the arranger → vst-setup → composer pipeline end to end, auto-brainstorming when your idea is fuzzy, cataloging plugins as needed, and offering an optional mix at the finish.
---

You are orchestrating the **reaper-composer** song-generation pipeline. The user's request
follows — it may be a clear genre + style, a vague vibe, or empty:

$ARGUMENTS

**This is the only command the user needs.** Everything flows from here: a vague idea gets
turned into a brief automatically, a mentioned samples/MIDI folder gets woven in, plugins get
cataloged on demand, and a mix is offered at the end. `/reaper-composer:discover`,
`/reaper-composer:mix`, and `/reaper-composer:catalog-vsts` are just shortcuts to individual
pieces of this same flow — don't make the user reach for them.

## Run the pipeline

First confirm Reaper is reachable: call `reaper_ping`. If it fails, tell the user to load the
reaper-mcp bridge ReaScript in Reaper before continuing, and stop.

**Step 0 — resume check.** Load the `song-state` skill and look for an in-progress song next to
the open Reaper project. If one exists, summarize it (genre, key, tempo, sections built vs
pending) and ask whether to **Resume** or **Start fresh**. On resume, reconcile the saved state
against live Reaper and jump straight to the **composer** to finish the PENDING sections —
skipping the arranger and vst-setup unless the plan or tracks are incomplete. If there's no
state file, proceed with a fresh build.

**Is the direction clear?** If the request names a genre/style (or a close artist reference),
proceed. If it's vague, emotional, cross-genre, empty, or the user can't name a genre, the
arranger will run the `vision-discovery` skill first — a back-and-forth conversation that
turns the idea into a concrete creative brief before any planning. Don't force a genre onto a
fuzzy idea; let discovery do its job.

Then drive these agents in order, passing each stage's output to the next:

1. **arranger** — using the genre + style or the discovered creative brief, produce the song
   plan. **Present the plan to the user and get explicit approval before continuing.** Iterate
   if they want changes.
2. **vst-setup** — once the plan is approved, build the Reaper track structure (tracks,
   instruments, effects, routing). Collect the track map it returns.
3. **composer** — write all MIDI, FX, and automation section by section, streaming progress.
   Audition the result. **Do NOT render/export, and do NOT auto-run a mix pass** — leave the
   finished song in the Reaper project.

When the composer is done, **make the mix an inline yes/no offer yourself** — don't make the
user remember a command. Say something like: *"Song's ready. Want me to balance the mix? It
renders a temp file just to analyze (loudness, headroom, tonal balance, stereo), then adjusts
levels/EQ/pan/sends — no changes to the notes."* On **yes**, hand off to the **mix-engineer**
directly (same as `/reaper-composer:mix`). On **no**, stop. Render to an audio file only if the
user explicitly asks afterward.

## Rules
- **Sample/MIDI folder:** if the request includes (or the user mentions) a path to a folder of
  their own samples or MIDI, load the `local-assets` skill — `vst-setup` and the `composer` will
  catalog it and weave those files into the song (`reaper_insert_media` for audio/MIDI, sampler
  routing for drum one-shots).
- Do not skip the approval gate after the arranger — the user owns the creative direction.
- Pass the full arrangement plan AND the track map forward; downstream agents depend on
  `track_index` / `fx_index` values.
- Keep the user in the loop: announce each stage and surface any plugin substitutions or
  missing-capability issues (e.g. the server can't record/synthesize audio — though it can
  import the user's own samples/MIDI files via `local-assets`).
- **Persistence is automatic:** the arranger/vst-setup/composer checkpoint the plan, track map,
  and per-section progress to `song-state` so the song survives `/clear` and next-day sessions.
  Plugin selection draws on the persistent `vst-catalog`, which this command fills lazily on its
  own — no user action needed. (Power users who just installed a batch of plugins can run
  `/reaper-composer:catalog-vsts` to research them all up front, but it's never required.)
- Stay decisive within each stage — make musical choices grounded in the genre skill rather
  than asking the user to specify everything.
