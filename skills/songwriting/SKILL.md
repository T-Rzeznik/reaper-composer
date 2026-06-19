---
name: songwriting
description: Genre-agnostic composition craft — the difference between correct notes and good ones. Voice leading, motif development (theme & variation), tension/release arcs, counter-melody and call-and-response, phrase structure, and the rule that no section repeats identically. Load alongside music-theory when writing any melodic/harmonic part; music-theory spells the notes, this skill decides which ones and in what shape.
---

# Songwriting craft (good notes, not just correct ones)

`music-theory` tells you which notes are *in key* and how to spell a chord. This skill is about
which of those notes to actually play, and how to develop them so the result sounds *composed*
rather than generated. The single biggest reason AI-written music sounds generic is **literal
repetition of a static motif over block chords** — everything below is the antidote. Apply these
as you assemble each section's note list, before the `reaper_add_midi_notes` batch.

## 1. Voice leading (chords that flow)

Don't re-spell every chord in root position from the offset table — that lurches. Keep common
tones and move the rest by the **smallest** interval.

- Spell the first chord, then for each next chord pick the inversion whose notes are *closest*
  to the previous voicing. Hold any shared tone in the same octave; move changed tones ≤2–3
  semitones where possible.
- Example, C → Am → F → G (key of C): instead of `60,64,67 / 57,60,64 / 53,57,60 / 55,59,62`,
  voice-lead the top: `E,G,C(60,64,67) → E,A,C(64,69,72) → F,A,C(65,69,72) → G,B,D(67,71,74)` —
  the top voice walks `C→C→C→D`, smooth.
- Keep the **bass note** (chord root, often −12/−24) separate from the chord voicing so the
  voicing can invert freely while the low end states the harmony.
- Pads: spread across ~2 octaves, double the root on top. Stabs/plucks: keep tight (one octave).

## 2. Motif development (theme & variation)

State a short idea (the hook/motif), then **transform** it on each repeat. A 2-bar motif that
recurs 8 times should appear in 4–5 *different* forms, not 8 identical ones. Transformations:

| Move | What you do |
|---|---|
| **Sequence** | Repeat the motif shifted up/down by a scale step or third |
| **Inversion** | Flip the contour — where it went up, go down by the same scale steps |
| **Rhythmic displacement** | Start the motif half a beat / a beat later |
| **Augment / diminish** | Double or halve the note lengths |
| **Fragmentation** | Take just the last 2–3 notes and repeat/develop them |
| **Ornament** | Add a passing/neighbor tone, a grace note, a slide into the target |
| **Re-harmonize** | Same melody notes, new chord under them → new emotional color |

Rule of thumb: **AABA** or **statement → answer → statement → development** across a 4-phrase
section. The hook is recognizable throughout; the variations keep it alive.

## 3. Phrase structure (where ideas breathe)

- Think in **antecedent/consequent** ("question/answer") pairs — a 2-bar phrase that feels
  open, answered by a 2-bar phrase that resolves. Most 8-bar sections = two such pairs.
- Leave **space**. A melody that plays on every beat has no shape. Rests are phrasing. End
  phrases with a held note or a gap so the next one lands.
- Land the **hook's strongest note on a downbeat** (bar 1 or bar 5 of the section), and aim
  phrase resolutions at chord tones on strong beats; use non-chord tones (passing/neighbor) on
  weak beats to create motion.

## 4. Tension & release (the arc)

Energy isn't just density — it's harmonic and melodic *pull*. Build tension, then resolve it.

- **Harmonic**: approach the tonic from its dominant (V→i / V→I) at section boundaries for
  resolution; sit on an unresolved chord (the V, or a suspended chord) under a build to create
  pull. Pedal tones (a held bass note under changing chords) ratchet tension.
- **Melodic**: rising contour + climbing register = rising tension; the highest note of a
  section ("climax tone") should arrive late (≈70–80% through), then fall to resolve.
- **Map it to the plan's `energy` values**: a breakdown should genuinely *release* (simpler
  harmony, lower register, more space) so the next drop's tension lands harder. Don't keep every
  section at full melodic density.

## 5. Counter-melody, call-and-response, and role separation

A song is layers in conversation, not stacked loops.

- Give parts **distinct registers and rhythms** so they don't fight: lead sings the long notes,
  bass holds roots/locks to the kick, a pluck/arp fills the gaps *between* the lead's phrases
  (call-and-response), pads sustain underneath.
- When the lead rests, let another voice answer — a bass fill, an arp run, a vocal-chop stab.
  This is what makes an arrangement feel "full" without everything playing at once.
- A **counter-melody** moves contrary to the lead (lead goes up, counter goes down) and is
  rhythmically offset, often an octave away. One well-placed counter-line lifts a chorus.

## 6. The non-negotiable rule: never paste a section identically

Every time a section recurs (verse 2, drop 2, the looped 8-bar core), change **at least one**
thing so the ear stays engaged:

- Add or remove a layer (drop the hats for 4 bars; add an octave-up lead on the repeat).
- A **fill** in the last bar of every 4 or 8 (drum fill, melodic turnaround, a riser into the
  next phrase).
- Vary the melody per item 2; re-voice the chords per item 1.
- A 1-beat drop-out / silence before a big downbeat.

When the genre skill says "Drop 2 = Drop 1 with a variation," *this* is the variation menu.

---

**Workflow:** decide the section's harmonic motion and the motif first, voice-lead the chords
(1), develop the motif across the phrases (2–3), shape the tension arc (4), then add the
answering/counter layers (5) — and make sure no recurrence is literal (6). Then hand the shaped
note list to `groove` for velocity/timing feel before the `reaper_add_midi_notes` batch.
