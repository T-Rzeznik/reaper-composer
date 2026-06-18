---
name: genre-trap
description: Musicological context for composing trap in Reaper — tempo/key conventions, subgenre structures (modern/mainstream trap, drill, hybrid/festival trap, lo-fi/melodic), the 808 sub-bass + hi-hat-roll signature, half-time drum patterns, synth/VST archetypes, harmony, and production moves (808 glides, hat triplets, pitched 808 basslines). Load when the requested genre is trap or a trap subgenre.
---

# Trap composition reference

Trap is built on a booming **808 sub-bass** (which doubles as the bassline AND the kick),
**rapid, rolling hi-hats**, hard snares/claps on the backbeat, and sparse, dark, atmospheric
melodies. Tempos are written fast but **feel half-time**. If the user only says "trap",
default to **modern melodic trap** and confirm direction.

## Tempo, key, structure by subgenre

| Subgenre | BPM (written / feel) | Typical key | Signature |
|---|---|---|---|
| Modern / mainstream | 140–160 / ~70–80 | minor | 808 glides, triplet hats, dark melody |
| Drill | 140–150 / half | minor (Phrygian flavor) | sliding 808s, syncopated "drill" hat pattern |
| Hybrid / Festival trap | 140–150 | minor | EDM-sized leads + trap drums, big drop |
| Lo-fi / Melodic | 130–150 / half | minor (7ths) | jazzy chords, mellow, vinyl texture |

**Half-time feel** is the key concept: the snare lands on beat 3 (not 2 and 4), so a 140 BPM
track grooves like 70. Write hats on the fast grid, snare/kick on the slow feel.

## Song structure

Intro → Verse → Hook/Chorus → Verse → Hook → Bridge → Hook → Outro (instrumental "type beat"
form). 8/16-bar sections. The **hook** carries the identity — strongest melody + fullest 808.
Beats are often loop-based with 8-bar variations (add/drop hats, double-time the hats into a
transition). For hybrid/festival trap, treat the hook like an EDM drop.

## Drums (MIDI; verify mapping with the loaded drum instrument)

- **808 / Kick**: the 808 IS the kick and bass. Place hits on syncopated downbeats (1, the
  "and" of 2/3, etc.), pitched to the song's root and chord roots — see production moves.
- **Snare/Clap** on **beat 3** (half-time backbeat), often layered (clap D#1/39 + snare D1/38).
  Sometimes a rimshot pickup before it.
- **Hi-hats** (closed F#1/42) are the trap signature: a steady 1/8 or 1/16 base pattern with
  **rolls** — bursts of 1/16, 1/32, and **triplet** subdivisions, with rising velocity.
  Vary roll placement every 1–2 bars so it never feels static. Open hat (A#1/46) for accents.
- **Percussion**: occasional rimshot, snap, or perc loop; keep it sparse.

## Instrument / VST archetypes (map to whatever is installed)

- **808**: a sine/triangle sub instrument with pitch glide/portamento and a distortion/
  saturation stage so it reads on small speakers. This is the most important sound — spend
  time on it. Set a short pitch glide between consecutive 808 notes for the signature slide.
- **Lead/Melody**: bells, plucks, detuned saws, flutes, or pitched vocal chops — dark,
  reverby, often in a high register over the sparse low end.
- **Chords/Keys**: piano, Rhodes, or pad with minor/jazzy voicings (lo-fi/melodic).
- **FX**: risers, downlifters, reverse cymbals, vocal ad-lib stabs for transitions.
If a named plugin isn't installed, substitute the closest sub/sine instrument for the 808
(crucial) and the nearest pluck/bell synth for the melody, and note the substitution.

## Harmony & melody

- Minor keys dominate; drill leans Phrygian/harmonic-minor for menace. Lo-fi uses 7th/9th
  jazz chords.
- Melodies are simple, dark, and repetitive — a short motif looped, lots of space.
- **The 808 plays the bassline**: it follows the chord roots/melody root notes, so its pitch
  changes per chord. Glide between 808 notes for the sliding-bass sound (especially drill).
- Leave space — trap is defined as much by silence as by notes.

## Production moves (these define the sound)

- **Pitched, gliding 808s**: write the 808 as actual pitched MIDI notes following the
  harmony, with short note overlaps + the instrument's glide on, so consecutive notes slide.
  This is the core of the genre.
- **Hi-hat rolls with triplets + velocity ramps**: program rolls by hand — subdivide into
  1/16/1/32/triplets and ramp velocity up through each roll. Don't write a flat hat line.
- **Half-time snare**: snare on 3, never a straight 2-and-4 backbeat, or it stops sounding like trap.
- **808/kick clash control**: since the 808 is sub AND kick, don't stack a second sustained
  sub under it — keep the low end mono and let the 808 own it.
- **Transitions**: drop the drums out for a bar, add a riser/reverse cymbal, then slam back
  into the hook. Respect each section's `energy` value.
