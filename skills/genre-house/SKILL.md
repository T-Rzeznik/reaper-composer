---
name: genre-house
description: Musicological context for composing house music in Reaper — tempo/key conventions, subgenre structures (deep, tech, progressive, future, bass, classic/soulful house), the four-on-the-floor groove, drum/hat patterns, synth/VST archetypes, harmony, and the production moves (sidechain pump, filtered loops, swing) that define it. Load when the requested genre is house or any of its subgenres.
---

# House composition reference

House is groove-first dance music built on a steady four-on-the-floor kick, off-beat hats,
and a hypnotic, loop-based arrangement that evolves through subtraction and addition rather
than big EDM-style drops. If the user only says "house", default to **tech house or deep
house** (the most common modern requests) and confirm direction.

## Tempo, key, structure by subgenre

| Subgenre | BPM | Typical key | Signature |
|---|---|---|---|
| Deep house | 118–124 | minor (jazzy 7ths/9ths) | warm pads, soulful chords, rolling sub bass |
| Tech house | 124–128 | minor | stripped, percussive, tight bass stabs, groove-driven |
| Progressive house | 124–130 | minor | long evolving builds, melodic lead breakdown |
| Future house | 124–128 | minor | metallic/filtered bass "drop", vocal chops |
| Bass house | 126–130 | minor | aggressive growl/donk bass, big drop energy |
| Classic / Soulful | 120–126 | major or minor | piano stabs, organ, disco/funk samples-as-MIDI |

Feel: mostly straight, but **swing/shuffle on the hats** (10–25%) is what gives house its
groove — nudge off-beat hats slightly late rather than dead-on the grid.

## Song structure

Intro → Build → Drop/Groove → Breakdown → Build → Drop/Groove 2 → Outro, in 8/16-bar blocks.
Unlike big-room EDM, the "drop" is a **full groove** (kick + bass + hats + hook), not a
silence-then-impact. The arrangement evolves by **adding/removing one element at a time**.
- **Intro** 16–32 bars: DJ-friendly, drums + a filtered element, easy to mix in.
- **Groove** 16–32 bars: the full loop — the song lives here.
- **Breakdown** 16 bars: strip to chords/pad/vocal, build tension back up.
- **Outro** 16–32 bars: reduce to drums for mixing out.

## Drums (MIDI; verify mapping with the loaded drum instrument)

- **Kick** on all four beats (C1, 36). Punchy, short.
- **Clap/snare** on beats 2 and 4 (clap D#1/39 layered with snare D1/38).
- **Closed hats** on the off-beats (the "and" of each beat) — the signature house pulse;
  open hat (A#1/46) on off-beats for drive. Add 1/16 closed-hat ghosts with swing for groove.
- **Percussion**: shakers, congas, rimshots, rides for movement — house leans heavily on
  layered percussion loops.

## Instrument / VST archetypes (map to whatever is installed)

- **Bass**: rolling sub or plucky filtered bass that locks to the kick rhythm (often plays
  on the off-beats between kicks). Deep house = warm round sub; tech house = short stabby.
- **Chords/Stabs**: Rhodes/electric-piano, organ, or filtered synth stabs — jazzy 7th/9th
  voicings for deep house, classic piano chords for soulful.
- **Pads**: warm analog pads under the chords with long reverb (breakdowns).
- **Lead/Vocal chop**: short topline or chopped vocal for the hook (progressive/future).
- **FX**: white-noise sweeps, vinyl crackle, short risers between sections.
If a named synth isn't installed, substitute the closest wavetable/virtual-analog or
electric-piano instrument and set a comparable patch via parameters.

## Harmony & melody

- Minor keys with extended jazz voicings (7ths, 9ths, sus) define deep/soulful house;
  tech house is often a static 1–2 chord vamp or just a bassline + stab.
- Common progressions: i–VII–VI–VII, ii–V–i, or a 2-chord loop. Keep it hypnotic and repetitive.
- Bass usually plays a syncopated off-beat pattern around the chord root, weaving with the kick.
- Toplines/stabs are short, rhythmic, and looped — groove over melody.

## Production moves (these define the sound)

- **Sidechain pump**: bass and pads/chords duck on every kick and recover over the beat.
  Emulate with a per-beat volume envelope (`add_envelope_point`, target volume, dip on the
  kick then ramp back up). Subtler than EDM but essential to the "breathing" house groove.
- **Hat swing**: offset off-beat hats slightly late for shuffle — do NOT quantize dead straight.
- **Filtered evolution**: automate a low-pass cutoff on the bass/chord bus to open across an
  intro/build and close on the outro (fx_param envelope) — house evolves via filtering.
- **Arrangement by subtraction**: respect section `energy` — mute/remove elements in
  breakdowns and reintroduce them one per 8 bars to build tension.
- **Width & space**: keep kick + sub mono and centered; spread hats, percussion, and pads wide.
