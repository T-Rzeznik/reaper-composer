---
name: genre-edm
description: Musicological context for composing EDM in Reaper — tempo/key conventions, subgenre song structures (house, future bass, dubstep, trance, etc.), drum patterns, synth/VST archetypes, harmony, and the production moves (sidechain, risers, drops) that define the genre. Load when the requested genre is EDM or any of its subgenres.
---

# EDM composition reference

Ground arrangement and composition choices in these conventions. When the user names a
subgenre, follow its row; when they only say "EDM", default to **future bass or melodic
house** (broad, accessible) and ask which direction.

## Tempo, key, structure by subgenre

| Subgenre | BPM | Typical key | Drop/structure signature |
|---|---|---|---|
| House / Tech house | 122–128 | minor | 4-on-floor, groove-driven, drop = filtered loop + bass |
| Future bass | 140–160 (feels half) | major or minor | supersaw/vocal-chop chords, pitch-bent drop |
| Dubstep | 140 (half-time drums) | minor | heavy wobble/growl bass drop, snare on 3 |
| Trance | 130–138 | minor | long build, rolling bass, euphoric lead drop |
| Trap (EDM) | 140–160 (half-time) | minor | 808 sub, rapid hats, big snare |
| Drum & bass | 170–176 | minor | breakbeat, fast sub bass |
| Big room / Festival | 126–132 | minor | huge supersaw lead + kick-only drop |

## Song structure (the EDM template)

Intro → Build 1 → Drop 1 → Breakdown → Build 2 → Drop 2 → Outro. In bars (8-bar blocks):
- **Intro** 16 bars: filtered/atmospheric, establish key and a melodic hook.
- **Build** 8 bars: riser, drum roll (accelerating snare), filter open, often a 1-bar
  silence/impact right before the drop.
- **Drop** 16 bars: full energy — the hook. This is the song; design it first.
- **Breakdown** 16 bars: strip back to chords/vocal, emotional reset.
- **Drop 2** usually = Drop 1 with a variation (new fill, extra layer).
- **Outro** 16 bars: filter down, elements drop out for mixing.

## Drums (MIDI, General-MIDI-ish mapping; verify with the loaded drum instrument)

- **Kick** on every beat (4-on-floor) for house/trance; on 1 (+ syncopation) for half-time
  trap/dubstep. Kick pitch ~ C1 (MIDI 36).
- **Clap/snare** on beats 2 and 4 (backbeat). Snare ~ D1 (38), clap ~ D#1 (39).
- **Closed hats** on offbeats or 1/8–1/16 grid; open hat (A#1, 46) on the "and" for drive.
- **Build fills**: snare roll subdividing 1/8 → 1/16 → 1/32 over the last 1–2 bars.

## Synth / VST archetypes (map to whatever is installed)

- **Lead**: supersaw / detuned-saw poly (Serum, Vital, Sylenth1, Massive). Unison + slight
  detune; wide.
- **Bass**: sub sine for the low end + a mid "reese"/growl layer for character. Keep the sub
  mono and centered.
- **Chords/Pads**: warm poly with reverb; future bass uses bright, slightly detuned stabs.
- **Pluck**: short-decay synth for arps/toplines.
- **FX**: white-noise riser, downlifter, impact/boom on the downbeat of drops.
If a named synth isn't installed, substitute the closest available wavetable/virtual-analog
synth and set a comparable patch via parameters.

## Harmony & melody

- Minor keys dominate; common progressions: i–VI–III–VII, vi–IV–I–V (major-borrowed for
  uplifting future bass), or a static 2-chord vamp under a strong topline.
- Drops often reuse the breakdown's chord progression with the full arrangement on top.
- Toplines are short, repeated, hook-first motifs — memorability over complexity.
- Bass generally follows the chord root; in sub-heavy styles it locks to the kick rhythm.

## Production moves (do these — they define the sound)

- **Sidechain pump**: the classic kick-ducks-everything feel. Emulate with a volume envelope
  on bass/chord tracks that dips to ~ -inf/low on each kick and recovers over the beat
  (`add_envelope_point`, target volume, sawtooth-up shape per beat). Essential for house/future bass.
- **Filter automation on builds**: open a low-pass cutoff from closed→open across the build
  (fx_param envelope on the synth's filter cutoff).
- **Risers into drops**: automate a noise synth's pitch/volume up over the build; land an
  impact on the drop's downbeat, often with a beat of silence just before.
- **Width**: leads/pads wide, kick + sub mono. Pan hats/percussion slightly for space.
- **Energy contour**: respect the section `energy` values — breakdowns must actually drop in
  density so the second drop hits harder.
