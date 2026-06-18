---
name: genre-rock-and-roll
description: Musicological context for composing classic rock and roll in Reaper — tempo/key conventions, subgenres (1950s rock & roll, rockabilly, blues-rock, surf, doo-wop-influenced), the 12-bar blues form, shuffle/backbeat drums, boogie-woogie basslines, guitar/piano/VST archetypes, harmony, and the production moves (slapback echo, shuffle swing, walking bass) that define the era. Load when the requested genre is rock and roll, rockabilly, or related 50s/60s rock.
---

# Rock and roll composition reference

Classic rock and roll (1950s–early 60s: Chuck Berry, Little Richard, Elvis, Buddy Holly) is
built on the **12-bar blues** form, a driving **backbeat with shuffle feel**, **boogie-woogie
basslines**, and bright guitar + piano. It's band music — guitar, piano, upright/electric
bass, drums, sometimes sax. If the user only says "rock and roll", default to **up-tempo
50s rock & roll (Chuck Berry style)** and confirm direction.

## Tempo, key, structure by subgenre

| Subgenre | BPM | Typical key | Signature |
|---|---|---|---|
| 50s rock & roll | 140–180 | A, E, G (guitar keys) | 12-bar blues, shuffle, guitar+piano |
| Rockabilly | 150–200 | E, A | slapback echo, upright slap bass, sparse drums |
| Blues-rock | 110–150 | E, A, G | heavier 12-bar, bluesy lead guitar |
| Surf rock | 150–180 | minor/major | reverb-drenched tremolo-picked guitar lead |
| Doo-wop influenced | 90–130 | major | I–vi–IV–V "50s progression", smooth |

**Feel: shuffle / swing.** Most 50s rock & roll swings the 1/8 notes (triplet feel) rather
than playing them straight. Surf and some Buddy Holly are straighter. Set swing accordingly.

## Song structure

Intro → Verse → Verse → Guitar/Sax Solo → Verse → Outro, or strophic 12-bar choruses with a
solo chorus in the middle. Sections are usually **12 bars** (one blues cycle) or 8 bars.
The **solo chorus** (guitar or sax taking a full 12-bar cycle) is the genre's showcase moment.
Often a 2–4 bar intro lick and a tag/ending lick.

## The 12-bar blues (the backbone)

In the key's I–IV–V (e.g. in A: A–D–E), one common form, one chord per bar:
```
I  I  I  I   IV IV I  I   V  IV I  V(turnaround)
```
Dominant 7th chords (A7, D7, E7) give the bluesy color. The turnaround (bar 12) leads back to I.

## Drums (MIDI; verify mapping with the loaded drum instrument)

- **Backbeat**: snare (D1/38) hard on beats **2 and 4** — the heartbeat of the genre.
- **Kick** (C1/36) on 1 (and often 3), simple and steady.
- **Ride/hi-hat**: a **shuffle pattern** — swung 1/8s on the ride or hat (triplet feel), or
  a steady train-beat. Rockabilly often uses brushes and a sparser kit.
- **Fills**: simple snare/tom fills into section changes; nothing busy.

## Instrument / VST archetypes (map to whatever is installed)

- **Lead/Rhythm guitar**: bright, clean-to-edge-of-breakup electric (Telecaster/Gretsch
  voicing) with a touch of tube amp grit. Double-stop licks, bends, chuck-berry-style intros.
- **Piano**: boogie-woogie / barrelhouse acoustic piano — rolling left-hand patterns and
  triplet right-hand stabs. Central to Little Richard / Jerry Lee Lewis sounds.
- **Bass**: upright/electric playing a **walking or boogie-woogie bassline** (root–3rd–5th–6th
  patterns) outlining each chord; locks with the kick.
- **Sax** (optional): honking tenor sax for solos/riffs.
- **Drums**: a dry, vintage-voiced acoustic kit.
If a named instrument isn't installed, substitute the closest clean electric-guitar amp sim,
acoustic piano, and upright/electric bass, and note the substitution.

## Harmony & melody

- I–IV–V dominant-7th harmony over the 12-bar form is the default; doo-wop uses I–vi–IV–V.
- Melodies and licks draw on the **blues scale and minor/major pentatonic** with bluesy bends
  and chromatic passing notes (b3, b5).
- Vocal-style phrasing: call-and-response between the vocal line and a guitar/piano answer.
- Guitar intros and turnarounds are signature licks — write a memorable 2-bar hook.

## Production moves (these define the era's sound)

- **Shuffle/swing the 1/8s**: write ride/hat, piano, and bass with a triplet swing feel
  (notes land on the 1st and 3rd of each beat's triplet), not straight — this is non-negotiable
  for 50s rock & roll.
- **Boogie-woogie walking bass**: program the bass to walk the chord tones each bar in steady
  1/8 or 1/4 notes, following the 12-bar changes — it drives the whole track.
- **Slapback echo**: a short (~80–120 ms) single delay on vocals/guitar is the defining 50s/
  rockabilly effect — set it via a delay FX's time parameter (one slap, low feedback).
- **Backbeat emphasis**: hit the snare on 2 and 4 with strong, consistent velocity.
- **Keep it live and dry**: minimal layering, light reverb (spring/plate), instruments
  panned like a small stage. Respect section `energy` — solos peak, verses sit back.
