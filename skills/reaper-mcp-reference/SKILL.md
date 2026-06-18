---
name: reaper-mcp-reference
description: How to drive Reaper through the reaper-mcp server — the exact tool surface, the workflows for building tracks/MIDI/FX/automation, and the non-obvious conventions (time in seconds, read-mode for envelopes, FX matched by exact name). Load this before issuing any reaper_* tool call.
---

# Driving Reaper via reaper-mcp

All DAW actions go through the `reaper`-prefixed MCP tools provided by the
`reaper-mcp` server (`github.com/t-rzeznik/reaper-mcp`). This skill is the contract:
do not invent tool names or arguments — every tool below exists, and nothing outside
this list does.

## Before you start

1. Call `reaper_ping` to confirm the bridge is reachable. If it errors with
   "could not reach Reaper bridge", the in-Reaper bridge ReaScript isn't running —
   tell the user to re-load it from Reaper's action list (it must be re-loaded every
   time Reaper restarts).
2. Call `reaper_get_project_info` to learn current tempo, and `reaper_list_tracks`
   to see existing tracks before creating new ones.

## Hard rules (these are the things that go wrong)

- **Time is in SECONDS, not bars/beats.** MIDI notes, item bounds, envelope points,
  markers, and the cursor are all positioned in seconds. Convert musical time yourself:
  `seconds_per_beat = 60 / bpm`; a bar in 4/4 = `4 * 60 / bpm` seconds. Compute the
  project's bar grid up front and reuse it.
- **Envelopes only play back in `read` mode.** After writing automation to a track,
  call `reaper_set_track_automation_mode(track_index, "read")` or it will look like
  nothing happened.
- **FX are matched by exact name suffix, including the prefix.** When `add_fx_to_track`
  fails with "not found", call `reaper_list_installed_fx`, copy the exact string
  (e.g. `VST3i: Vital (Vital Audio)` for an instrument, `VST3: Pro-Q 3 (FabFilter)`
  for an effect), and pass that verbatim. Instruments carry an `i` suffix on the type.
- **FX parameters are set by name or index — there is NO screenshot/vision.** Always
  `reaper_list_fx_params` first to discover real parameter names/ranges, then
  `reaper_set_fx_param`. Never assume a parameter exists.
- **No audio/sample import.** This server writes MIDI only. There is no tool to drop
  a `.wav` onto a track. If a sample is unavoidable, the only escape hatch is
  `reaper_run_action` with a Reaper command ID.
- **One MCP call = one undo step.** Safe to iterate; the user can Ctrl+Z any single action.

## Tool surface (~53 tools, all `reaper_`-prefixed)

**Session / discovery** — `ping`, `get_project_info`, `list_installed_fx`,
`analyze_project`, `analyze_mix`. Read tools accept `response_format` = `markdown` | `json`
(use `json` when you'll parse the result).

**Tracks** — `list_tracks`, `get_track_state`, `create_track`, `delete_track`,
`rename_track`, `set_track_volume_db`, `set_track_pan`, `set_track_mute`,
`set_track_solo`; master: `get_master_track`, `set_master_volume_db`.

**FX** — `list_track_fx`, `add_fx_to_track`, `remove_fx`, `set_fx_enabled`,
`list_fx_presets`, `set_fx_preset`, `list_fx_params`,
`set_fx_param(track_index, fx_index, param, value)` — `param` is an index-as-string
or a case-insensitive name; `value` must be within the param's min..max.

**Automation** — `add_envelope_point(track_index, target, time_sec, value, fx_index=-1,
param="", shape=linear, value_is_db=False)` where `target` ∈ volume | pan | fx_param
(fx_param requires `fx_index` + `param`); `clear_envelope`; `set_track_automation_mode`.

**MIDI / items** — `insert_midi_item(track_index, start_sec, end_sec)` returns
`{item_index, ...}`, then `add_midi_note(track_index, item_index, pitch 0-127,
start_sec, length_sec, velocity 1-127, channel 0-15)`. Also `list_items`, `delete_item`
(later item indices shift down by one after a delete).

**Transport / timeline** — `transport_play`, `transport_stop`, `transport_record`,
`transport_pause`, `set_cursor`, `set_tempo`, `set_time_selection`,
`clear_time_selection`, `set_loop_enabled`, `set_track_record_arm`,
`set_track_record_input`.

**Markers / routing** — `list_markers`, `add_marker`, `add_region`, `delete_marker`,
`goto_marker`, `list_sends`, `add_send`, `set_send_volume_db`, `remove_send`.

**Output** — `render_project` (uses the project's last-used render settings),
`run_action(command_id)` — escape hatch to trigger any Reaper action by command ID.

## Canonical workflows

**New instrument track:**
`create_track` → `rename_track` → `add_fx_to_track` (instrument first in chain) →
`list_fx_params` → `set_fx_param` for the starting sound → optional FX (EQ, comp) added after.

**Write a MIDI part:** compute the bar grid in seconds → `insert_midi_item` spanning the
section → loop `add_midi_note` for each note. Keep one item per section per track so it's
easy to delete/redo a section.

**Section markers:** after laying out the arrangement, `add_marker` at each section's
start second (intro/verse/drop/…) so the user can navigate the timeline.

**Mix pass:** `analyze_mix` to read levels → adjust with `set_track_volume_db` /
`set_track_pan`, bus reverb/delay via `add_send`.

**Automation (e.g. a filter sweep on a build):** `set_track_automation_mode(idx,"read")`
→ `add_envelope_point` with `target="fx_param"`, the filter cutoff `param`, several points
across the build's seconds, `shape="linear"` (or hold then ramp).

**Final:** `transport_play` from the start to audition. Leave the song in the project —
**only call `render_project` if the user explicitly asks to render/export to a file.**
