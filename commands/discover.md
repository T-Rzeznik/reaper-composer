---
description: Brainstorm a song when you don't have a genre in mind. Runs a back-and-forth conversation to turn a vibe/idea into a concrete creative brief, then (with your go-ahead) builds it in Reaper.
---

You are running the **reaper-composer** discovery flow — the entry point for users who have a
musical idea but can't name a genre. Whatever the user gave you (a mood, a scene, an artist
mashup, a half-formed vibe, or nothing yet) follows:

$ARGUMENTS

## What to do

1. **Run the `vision-discovery` skill now.** Converse back and forth — collaboratively, a
   question or two at a time — translating vague language into musical decisions, offering A/B
   choices, and using reference anchors. Keep going until the vision passes the skill's
   convergence test (you can state tempo, mood/key, structure shape, key instrumentation, and
   2–3 references and the user confirms). This step does NOT touch Reaper.

2. **Present the creative brief** the skill produces and confirm it with the user.

3. **Offer to build it.** Ask whether they want to proceed into the full song-generation
   pipeline now. Only if they say yes:
   - Confirm Reaper is reachable with `reaper_ping`; if it fails, tell them to load the
     reaper-mcp bridge ReaScript and stop here (the brief is saved in the conversation).
   - Hand the brief to the **arranger** → get plan approval → **vst-setup** → **composer**,
     exactly as the `/reaper-composer:compose` command does. Do NOT render/export or auto-run a
     mix pass; when the song is done, offer the optional mix step (`/reaper-composer:mix`).

## Rules
- Discovery is the point of this command — don't shortcut to a genre guess. If the user
  actually already knows the genre, say so and suggest `/reaper-composer:compose` instead.
- The brief is the handoff contract; pass it intact to the arranger (including the genre
  routing / hybrid element sourcing the skill decided).
- Keep the user in control: confirm the brief before building, and never start writing to
  Reaper without their go-ahead.
