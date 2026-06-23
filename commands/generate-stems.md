---
description: (Optional, standalone) Generate brand-new audio stems with a local, free model (MusicGen-small) and drop them on the Reaper timeline. Use for AI-generated texture/pad/bed/loop layers — not precise MIDI parts. A standalone tool run on demand; it is not part of the /reaper-composer:compose pipeline.
---

You are running the **reaper-composer** stem-generation pass. Any direction the user gave (the
role they want, the section, a vibe — e.g. "a warm pad under the chorus", "an ambient texture
bed", "a rough sub-bass sketch") follows:

$ARGUMENTS

## What to do

1. Confirm Reaper is reachable with `reaper_ping`; if it fails, tell the user to load the
   reaper-mcp bridge ReaScript and stop.
2. Load the `stem-generation` skill and follow it: check the local model deps are installed
   (one-time `pip install "transformers>=4.40" torch scipy`), build a prompt from the song's
   key/BPM/section (read `song-state` for context), generate a WAV with the local model, then
   place and **sync** it on its own track with `reaper_insert_media`.
3. Audition the section and report what you generated (prompt → file → track → time) with honest
   caveats. Offer to regenerate with a different seed/prompt if they don't like it.

## Rules
- This is an **opt-in** step. Generation is **local and free per clip** but slow on CPU (1–3 min
  per short clip) — warn the user before a long run.
- Generated stems are *textures/sketches*, not radio-ready and not grid-locked. For precise,
  in-key melodic or drum parts, steer the user to the normal MIDI pipeline
  (`/reaper-composer:compose`) instead — say so honestly.
- **Do NOT render/export** a final audio file unless the user explicitly asks.
- Generated WAVs live under `~/.reaper-composer/stems/` (runtime user-machine data) — never
  commit them to the plugin repo.
