---
name: music-theory
description: Lookup tables for turning musical intent into exact MIDI numbers and second-positions — bar/beat→seconds timing math, the MIDI note-number map, scale and chord note sets for any key, swing/triplet offsets, and the General MIDI drum map. Load before writing any MIDI so notes, chords, and timing are computed from tables instead of guessed. Used mainly by the composer; the arranger uses the scale tables for key choice.
---

# Music theory reference (compute, don't guess)

LLMs reliably make off-by-one and wrong-note errors doing this arithmetic inline. Use these
tables. All reaper-mcp time arguments are in **seconds** (see `reaper-mcp-reference`), so the
timing section is how you get there from bars/beats.

## 1. Timing: bars/beats → seconds

```
sec_per_beat = 60 / bpm
sec_per_bar  = beats_per_bar * sec_per_beat          # 4/4 → 4 * 60/bpm
section_start_sec = (start_bar - 1) * sec_per_bar    # bars are 1-indexed in plans
note_start_sec    = section_start_sec + (beat_in_bar - 1) * sec_per_beat + subdivision_offset
```

Worked example at **128 BPM, 4/4**: `sec_per_beat = 0.46875`, `sec_per_bar = 1.875`.
Bar 33 starts at `(33-1)*1.875 = 60.0s`. Beat 3 of bar 33 = `60.0 + 2*0.46875 = 60.9375s`.

Common note lengths in seconds = `sec_per_beat * factor`: whole `*4`, half `*2`, quarter `*1`,
eighth `*0.5`, sixteenth `*0.25`, dotted = `*1.5` of the base, triplet = base `*(2/3)`.

### Swing & triplets
- **Triplet grid**: three even notes per beat → each `sec_per_beat / 3` apart.
- **Swing (shuffle)**: delay every off-beat (the "and"). At swing ratio `s` (0 = straight,
  ~0.5–0.67 typical), the off-beat 8th starts at `beat_start + sec_per_beat * (1 + s) / 2`
  rather than `+ sec_per_beat/2`. Hard shuffle ≈ triplet feel (off-beat at `+2/3` of the beat).

## 2. MIDI note numbers

`note_number = (octave + 1) * 12 + pitch_class`. Pitch classes:
`C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11`.
Anchors: **C-1 = 0**, **C1 = 24**, **C2 = 36**, **middle C = C4 = 60**, **A4 (440 Hz) = 69**,
**C5 = 72**, **G9 = 127**. To transpose an octave, ±12.

## 3. Scales (semitone steps from the root)

| Scale | Intervals (semitones) |
|---|---|
| Major (Ionian) | 0 2 4 5 7 9 11 |
| Natural minor (Aeolian) | 0 2 3 5 7 8 10 |
| Harmonic minor | 0 2 3 5 7 8 11 |
| Dorian | 0 2 3 5 7 9 10 |
| Phrygian | 0 1 3 5 7 8 10 |
| Mixolydian | 0 2 4 5 7 9 10 |
| Locrian | 0 1 3 5 6 8 10 |
| Major pentatonic | 0 2 4 7 9 |
| Minor pentatonic | 0 3 5 7 10 |
| Blues | 0 3 5 6 7 10 |

Add the root's MIDI number to each interval. **Example — F minor (root F3 = 53):**
`53,55,56,58,60,61,63` (then +12 for the next octave). **A minor pentatonic (A2 = 45):**
`45,48,50,52,55`.

## 4. Chords (semitone offsets from the chord root)

| Chord | Offsets | Chord | Offsets |
|---|---|---|---|
| Major triad | 0 4 7 | Minor triad | 0 3 7 |
| Diminished | 0 3 6 | Augmented | 0 4 8 |
| Major 7 | 0 4 7 11 | Minor 7 | 0 3 7 10 |
| Dominant 7 | 0 4 7 10 | Minor 7♭5 | 0 3 6 10 |
| Major 9 | 0 4 7 11 14 | Minor 9 | 0 3 7 10 14 |
| sus2 / sus4 | 0 2 7 / 0 5 7 | Power chord (5) | 0 7 (+12 for octave) |
| Add9 | 0 4 7 14 | 6 | 0 4 7 9 |

**Example — C major triad (C4 = 60):** `60,64,67`. **A minor 7 (A3 = 57):** `57,60,64,67`.
Voice chords by dropping/raising tones an octave (±12) to keep a smooth range; for pads,
spread across ~2 octaves; for stabs, keep tight.

## 5. General MIDI drum map (the notes our genre skills reference)

| Note | Drum | Note | Drum |
|---|---|---|---|
| 35 / 36 | Acoustic / Bass kick | 42 | Closed hi-hat |
| 38 | Acoustic snare | 44 | Pedal hi-hat |
| 40 | Electric snare | 46 | Open hi-hat |
| 37 | Side stick / rim | 49 / 57 | Crash 1 / 2 |
| 39 | Hand clap | 51 / 59 | Ride 1 / 2 |
| 41 43 45 47 48 50 | Toms (low→high) | 54 | Tambourine |
| 56 | Cowbell | 53 | Ride bell |

**Caveat:** this is the GM standard. Many drum VSTs (Superior Drummer, GetGood, Battery,
samplers) remap pads. When in doubt, the genre skill says "verify against the loaded drum
instrument" — trust the loaded instrument's mapping over this table if they conflict.

## Using this with the batch writer

Assemble a section's notes as a list of `{pitch, start_sec, length_sec, velocity, channel}`
using the tables above, then write them with `reaper_add_midi_notes` in one call (see
`reaper-mcp-reference`) rather than one note at a time.
