# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project State

A Claude Code **plugin** (agents + skills + commands) — not a standalone application, so
there is no build/test/lint step. The deliverable is plugin assets, and they exist now:

- `.claude-plugin/plugin.json` — manifest; `.claude-plugin/marketplace.json` — makes the
  repo installable (`/plugin marketplace add t-rzeznik/reaper-composer` →
  `/plugin install reaper-composer@reaper-composer`). `plugin.json` alone is NOT installable.
- `commands/compose.md` — the orchestrator, invoked as `/reaper-composer:compose` (commands
  and skills are namespaced by plugin name once installed)
- `commands/discover.md` — `/reaper-composer:discover`, the brainstorm entry point: runs the
  `vision-discovery` skill, then offers to continue into the same build pipeline
- `commands/mix.md` — `/reaper-composer:mix`, an opt-in mix/balance pass (invokes `mix-engineer`)
- `commands/catalog-vsts.md` — `/reaper-composer:catalog-vsts`, eager full scan that researches
  every installed plugin into the persistent `vst-catalog` (compose fills it lazily on its own)
- `agents/{arranger,vst-setup,composer}.md` — the three-stage build pipeline;
  `agents/mix-engineer.md` — opt-in mixing/balance (no compositional changes)
- `skills/vision-discovery/` — conversational discovery the arranger runs FIRST when the
  request is vague/genre-less/hybrid; produces a creative brief + genre routing
- `skills/music-theory/` — lookup tables (MIDI notes, scales, chords, bar→seconds + swing math,
  GM drum map); the composer uses these instead of computing notes/timing inline
- `skills/mixing/` — how to read the analyze tools and translate metrics into mix fixes
- `skills/recommended-vsts/` — free VSTs by role; `vst-setup` suggests these (with an
  install→rescan loop) when no suitable instrument is installed, instead of forcing a synth
- `skills/local-assets/` — use a user-pointed folder of samples/MIDI: scan + catalog, place
  audio/`.mid` on the timeline via `reaper_insert_media` (one-shots dropped directly by default;
  sampler routing only if the user asks for MIDI-triggered drums)
- `skills/reaper-mcp-reference/` — the reaper-mcp tool contract (load before any DAW call)
- `skills/vst-catalog/` — builds + reads a persistent, per-plugin catalog of the user's INSTALLED
  VSTs (what each is, roles/genres it suits, starting sound); `vst-setup` selects from it instead
  of blind name-matching, researching new plugins incrementally (model-knowledge first)
- `skills/song-state/` — persists per-project song state (brief, plan, track map, per-section
  built/pending) so a `/clear` or next-day session can resume; checkpointed by the build agents,
  read at the start of compose/discover to offer Resume
- `skills/genre-{edm,house,trap,metal,rock-and-roll}/` — per-genre musicological context
- `skills/genre-template/` — copy to add a new genre (not a real genre; agents ignore it)
- `README.md` — user-facing docs (install, usage, architecture)

To "run" it: load the plugin in Claude Code with Reaper + the reaper-mcp bridge live, then
invoke `/reaper-composer:compose <genre>, <style>`. Verify the DAW link with `reaper_ping`
first — nothing works until it returns Reaper's version.

**Adding a genre = adding a `skills/genre-<name>/SKILL.md` only.** Agents are genre-agnostic;
never branch genre logic into agent files (see principle below).

## Persistence / context tracking

Two on-disk JSON files give the plugin memory across runs (the persistence *logic* lives in
skills, keeping agents thin — consistent with the design principle below):

- **VST catalog** — `~/.reaper-composer/vst-catalog.json` (machine-global; Windows
  `C:\Users\<user>\.reaper-composer\`). One researched entry per installed plugin, keyed by
  exact FX name. Built **incrementally**: each scan diffs `reaper_list_installed_fx` against the
  catalog and only researches new plugins (model-knowledge first, web only for unknowns).
  `vst-setup` selects from it; `/reaper-composer:catalog-vsts` does a full eager scan.
- **Song state** — `<project-dir>/.reaper-composer/song-state.json` (per-project, beside the
  `.rpp`). Holds the brief, approved plan, track map, and per-section `built`/`pending` status.
  The arranger/vst-setup/composer **checkpoint** it; compose/discover read it at startup to offer
  **Resume**, reconciling against live Reaper (`list_tracks`/`list_items`) before continuing.
  Unsaved project → prompt to save (temp fallback under `~/.reaper-composer/unsaved-projects/`).

Both are **runtime user-machine data — never commit them to the plugin repo.**

## What This Plugin Does

Generates full songs in [Reaper](https://www.reaper.fm/) (a DAW) from a natural-language
request (genre + style/artist reference). The plugin orchestrates a three-agent build pipeline
plus an opt-in mix stage that drive Reaper through the Reaper MCP server.

## Critical External Dependency: the `reaper-mcp` server

All DAW manipulation goes through the **`reaper-mcp` MCP server**
(`github.com/t-rzeznik/reaper-mcp`), already wired into the user's `~/.claude.json` and
reported working end-to-end. Do not invent MCP tool signatures — match what the server
actually provides.

How it works: `Claude Code ──stdio/MCP──▶ reaper-mcp server ──TCP 127.0.0.1:8765──▶ bridge
ReaScript inside Reaper`. The bridge must be re-loaded from Reaper's action list every time
Reaper restarts. Every MCP call is one Reaper undo step.

### Tool surface (~55 tools, all `reaper_`-prefixed)

- **Session/discovery:** `ping`, `get_project_info`, `list_installed_fx`, `analyze_project`,
  `analyze_mix`. Read tools take a `response_format` arg (`markdown` | `json`).
- **Tracks:** `list_tracks`, `get_track_state`, `create/delete/rename_track`,
  `set_track_volume_db`, `set_track_pan`, `set_track_mute`, `set_track_solo`, master equivalents.
- **FX:** `list_track_fx`, `add_fx_to_track`, `remove_fx`, `set_fx_enabled`,
  `list_fx_presets`, `set_fx_preset`, `list_fx_params`, `set_fx_param` (by index or name).
- **Automation:** `add_envelope_point` (targets: volume / pan / fx_param), `clear_envelope`,
  `set_track_automation_mode` — a track must be in `read` mode for written envelopes to play back.
- **MIDI/items:** `insert_midi_item(track, start_sec, end_sec)` → then
  `add_midi_notes(track, item_index, notes:[{pitch,start_sec,length_sec,velocity?,channel?}])`
  to write a whole part in one call (preferred); `add_midi_note(...)` for a single note;
  `insert_media(track, file_path, start_sec)` imports an audio or `.mid` file from disk;
  `list_items`, `delete_item`.
- **Transport/timeline:** `transport_play/stop/record/pause`, `set_cursor`, `set_tempo`,
  `set_time_selection`, `set_loop_enabled`, record arm/input.
- **Markers/routing:** `list/add_markers`, `add_region`, `goto/delete_marker`, sends.
- **Output:** `render_project`; `run_action` (escape hatch — any Reaper command ID).

When an FX name isn't found, call `list_installed_fx` and copy the exact name including the
`VST3:` / `VST3i:` prefix — Reaper matches by exact suffix.

## ⚠️ Constraints from the real tool surface

These shape every agent's behavior. An early design draft assumed otherwise (vision-based FX
control, sample-vs-MIDI choices); the real server supports none of that, so keep these in mind:

1. **No vision / screenshot tool exists.** FX are NOT controlled by screenshotting and parsing
   VST UIs (an early plan idea). The composer drives plugins entirely through named/indexed
   parameters: `list_fx_params` → `set_fx_param`.
2. **MIDI and automation are time-based (seconds), not bars/beats.** The composer converts
   musical time → seconds itself using the project tempo.
3. **Created sounds are MIDI; the server can't record/synthesize audio.** New parts are MIDI
   driving instrument plugins. It *can* import existing files, though — `reaper_insert_media`
   drops the user's own audio samples/loops or `.mid` clips onto a track (see `local-assets`).

## Architecture

A three-agent build pipeline plus an opt-in mix stage, with genre knowledge factored out into
reusable skills. Two commands enter the pipeline: `/reaper-composer:compose` (clear genre +
style) and `/reaper-composer:discover` (a vibe with no genre — runs the `vision-discovery`
skill first to produce a creative brief, which the arranger also triggers automatically for
fuzzy requests). `/reaper-composer:mix` runs the mix stage separately.

1. **Research & Arrangement Agent** (`arranger`) — turns genre + style (or a discovered brief)
   into a section-by-section song plan (intro/verse/chorus/breakdown/drop, tempo, key,
   per-section instrumentation + energy). User approves or iterates before anything is built.
2. **VST Selection & Setup Agent** — picks instruments/effects for the genre and loads them
   into Reaper's track structure via MCP.
3. **Composition Agent** — writes MIDI (`insert_midi_item` → batch `add_midi_notes`, in
   seconds; computes notes/timing from the `music-theory` skill's tables), automation
   envelopes, and FX control via MCP. Drives plugins through their **named/indexed parameters**
   (`list_fx_params` → `set_fx_param`) — there is no UI vision; see constraints below. Streams
   progress updates to the user.

Plus, **opt-in only** (never automatic — it renders a temp file to analyze):
4. **Mix Engineer** (`mix-engineer`) — runs the analyze→fix→re-analyze loop via
   `analyze_project`, balancing levels/EQ/pan/sends. Makes no compositional changes.

The build agents run in sequence and communicate to refine details (e.g. the VST agent confirms
compatibility with the composition agent).

### Design Principle: agents are general, genres are skills

Keep the agents genre-agnostic. **All genre-specific knowledge lives in skills** — one
skill per genre (EDM, metal, etc.) holding drum patterns, tempo ranges, song structures, VST
archetypes, harmonic/melodic conventions, and production techniques. Agents pull the relevant
skill for musicological context and ask clarifying questions within it ("hard drop or
build?"). When adding genre support, add or extend a skill — do not branch genre logic inside
agent code.
