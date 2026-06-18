---
name: genre-metal
description: Musicological context for composing metal in Reaper — tempo/tuning conventions, subgenre structures (thrash, death, metalcore, djent, etc.), riff and drum patterns (blast beats, double-kick, breakdowns), guitar/VST archetypes, and production moves. Load when the requested genre is metal or any of its subgenres.
---

# Metal composition reference

Ground choices in these conventions. If the user only says "metal", default to **modern
metalcore/djent** (the most common request) and confirm direction.

## Tempo, tuning, structure by subgenre

| Subgenre | BPM | Tuning | Signature |
|---|---|---|---|
| Thrash | 160–220 | E / Eb standard | fast palm-muted gallops, tight snare |
| Death | 180–260 | drop B / C standard | blast beats, tremolo riffs, growls |
| Metalcore | 120–180 | drop C / drop D | melodic leads + breakdowns, half-time chugs |
| Djent / Prog | 100–160 (odd meters) | drop G/F, 7–8 string | syncopated polymetric chugs, ambient leads |
| Doom / Sludge | 60–90 | very low | slow, heavy, sustained power chords |
| Black | 150–220 | standard/lower | tremolo + blast beats, atmospheric |

Many metal riffs use low tunings — express pitch in MIDI note numbers; a drop-C low string
root is ~ C1–C2. Odd time signatures (7/8, 5/4) are common in prog/djent — set the plan's
time signature accordingly and compute the bar grid from it.

## Song structure

Intro → Verse (riff A) → Pre-chorus → Chorus → Verse → Chorus → Bridge/Breakdown → Solo →
Final chorus/Breakdown → Outro. Metalcore foregrounds the **breakdown** (half/quarter-time
chug section, maximum heaviness); prog foregrounds **dynamic shifts** between heavy and clean/ambient.

## Drums (MIDI; verify mapping with the loaded drum instrument)

- **Double kick**: rapid 1/16 kick (C1, 36) under fast sections — the backbone of heavy parts.
- **Blast beat**: alternating kick + snare on 1/16s (death/black).
- **Backbeat snare** (D1, 38) on 2 and 4 for groove/metalcore.
- **Breakdown**: half-time feel — snare on 3, kick locked to the guitar chug rhythm.
- **China/crash** accents on riff downbeats; ride for verses.

## Guitar / VST archetypes

- **Rhythm guitar**: high-gain amp sim (Neural DSP, STL, ML Sound Lab, or stock ReaPlugs +
  amp sim). Double-track L/R hard-panned for width. Tight palm mutes = short note lengths +
  consistent velocity.
- **Lead guitar**: same amp, less gain, center or slightly panned; legato/bend phrasing.
- **Bass**: follows rhythm guitar root, with grind/distortion to cut through; often a clean
  + distorted layer.
- **Drums**: a sampled metal drum instrument (Superior Drummer / GetGood Drums style; or
  any installed drum sampler) — pick the closest installed.
- **Ambient/lead synth** (prog/metalcore): pads behind clean sections.

## Riffs & harmony

- Riffs are rhythmic first: palm-muted root chugs (short, low, repeated) punctuated by
  power-chord stabs and tremolo runs. Build chug rhythms against the kick pattern.
- Power chords (root + fifth) for heaviness; add the octave for fullness.
- Minor/Phrygian/Locrian and the harmonic-minor flavor define the dark tonality;
  chromatic passing tones and tritones for tension.
- Leads use minor pentatonic + harmonic minor; fast alternate-picked or tremolo lines.

## Production moves

- **Tightness**: palm-mute chugs need short note lengths and quantized starts so the
  L/R guitars and kick lock. Sloppy timing kills heaviness.
- **Width**: hard-pan the two rhythm guitar tracks L/R; keep kick, snare, bass centered.
- **Breakdown impact**: drop density and tempo feel right before the breakdown (a beat of
  space or a cymbal choke), then hit the half-time chug hard.
- **High-pass the lows** off everything except kick/bass to keep the low end clean under heavy gain.
