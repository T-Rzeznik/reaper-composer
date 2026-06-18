---
description: Mix and balance the current Reaper project — analyze the master (loudness, headroom, tonal balance, stereo) and apply level/EQ/pan/send fixes. Opt-in; renders a temp file for analysis only.
---

You are running the **reaper-composer** mix pass. Any focus the user gave (e.g. "the vocal's
buried", "too boomy", a target loudness) follows:

$ARGUMENTS

## What to do

1. Confirm Reaper is reachable with `reaper_ping`; if it fails, tell the user to load the
   reaper-mcp bridge ReaScript and stop.
2. Hand off to the **mix-engineer** agent, passing along any focus note above. It will:
   - explain that the mix check renders a temp file for analysis (not an export) and may use
     Gemini if configured;
   - run the analyze → fix → re-analyze loop (loudness, clipping/headroom, tonal balance,
     mono-compatibility), degrading to DSP-only metrics if the AI layer isn't set up;
   - apply level/EQ/pan/send fixes and report before/after.

## Rules
- This is an **opt-in** step and is **non-destructive to the music** — the mix-engineer changes
  only levels/EQ/pan/sends, never notes, instruments, or arrangement.
- **Do NOT render/export a final audio file** unless the user explicitly asks; the temp render
  is for analysis only.
- If the project has no content yet, say so — there's nothing to mix until a song exists
  (`/reaper-composer:compose` or `/reaper-composer:discover`).
