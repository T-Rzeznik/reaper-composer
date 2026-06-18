---
description: Generate a full song in Reaper from a genre + style. Runs the arranger → vst-setup → composer pipeline end to end.
---

You are orchestrating the **reaper-composer** song-generation pipeline. The user's request
follows — it may be a clear genre + style, a vague vibe, or empty:

$ARGUMENTS

## Run the pipeline

First confirm Reaper is reachable: call `reaper_ping`. If it fails, tell the user to load the
reaper-mcp bridge ReaScript in Reaper before continuing, and stop.

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
   Audition the result. **Do NOT render/export** — leave the finished song in the Reaper
   project. Render only if the user explicitly asks for an audio file afterward.

## Rules
- Do not skip the approval gate after the arranger — the user owns the creative direction.
- Pass the full arrangement plan AND the track map forward; downstream agents depend on
  `track_index` / `fx_index` values.
- Keep the user in the loop: announce each stage and surface any plugin substitutions or
  missing-capability issues (e.g. a requested sample, since the server is MIDI-only).
- Stay decisive within each stage — make musical choices grounded in the genre skill rather
  than asking the user to specify everything.
