---
name: genre-template
description: TEMPLATE — not a real genre. Copy this directory to skills/genre-<name>/ and fill in every section to add support for a new genre. Delete this description line and write a real one (the description is what the agents use to decide when to load the skill, so make it specific to the genre and its subgenres).
---

<!--
HOW TO USE THIS TEMPLATE
1. Copy the whole folder: skills/genre-template/ -> skills/genre-<your-genre>/
2. Set `name:` to genre-<your-genre> (kebab-case, must match the folder).
3. Rewrite `description:` so it names the genre + its subgenres — the agents match on it.
4. Fill every section below with concrete, buildable conventions. Delete these comments.
No agent code changes are ever needed; agents pick up the skill by its name/description.
Keep advice CONCRETE and MIDI/parameter-oriented — the composer writes notes in seconds
and sets FX params by name (see the reaper-mcp-reference skill).
-->

# <Genre> composition reference

One paragraph: what defines this genre sonically, and what to default to if the user is vague
(name the default subgenre and say you'll confirm direction).

## Tempo, key, structure by subgenre

| Subgenre | BPM | Typical key/tuning | Signature (rhythm/drop/structure) |
|---|---|---|---|
| <sub 1> | <range> | <key> | <one-line defining trait> |
| <sub 2> | <range> | <key> | <one-line defining trait> |

Note any feel quirks: half-time vs straight, swing/shuffle, common time signatures.

## Song structure

The genre's typical arrangement in named sections, with rough bar lengths (use 4/8-bar
blocks). Call out the section that carries the genre's identity (the drop, the chorus, the
breakdown, the solo…) — the arranger designs that first.

## Drums (MIDI; verify mapping against the loaded drum instrument)

- Kick: <pattern + typical MIDI note, e.g. C1/36>
- Snare/clap: <pattern + note>
- Hats/cymbals: <pattern + note>
- Fills/transitions: <what marks section changes>

## Instrument / VST archetypes (map to whatever is installed)

- <role>: <synth/amp archetype + how to set its starting sound via parameters>
- … (lead, bass, chords/pads, rhythm, percussion, FX as relevant)
State the fallback: if a named plugin isn't installed, substitute the closest available and note it.

## Harmony & melody

- Common keys/scales/modes and signature chord progressions.
- How the bass relates to the chords and the kick.
- Melody/topline/riff conventions (phrasing, repetition, range).

## Production moves (the things that *define* the sound)

- The 2–5 signature techniques (e.g. sidechain, palm-mute tightness, swing, reverb washes),
  each expressed as concrete reaper-mcp actions (envelope on a param, note-length choices,
  panning, sends). Respect each section's `energy` value from the plan.
