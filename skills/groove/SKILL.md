---
name: groove
description: Humanization and feel for written MIDI — velocity shaping (accents, ghost notes, dynamic curves), micro-timing (push/pull, swing application, small jitter), per-instrument feel templates, and note-length/legato choices. Load alongside music-theory and songwriting before the reaper_add_midi_notes batch; this is what stops MIDI sounding robotic and on-grid. All offsets are in seconds, matching reaper-mcp's time arguments.
---

# Groove & humanization (stop the robot)

Perfectly quantized, uniform-velocity MIDI is the dead giveaway of machine-written music.
`music-theory` gives you the grid positions; this skill nudges velocity and timing **off** the
grid by musically-meaningful amounts so the part breathes. Apply it as the *last* shaping pass
on a section's note list, just before `reaper_add_midi_notes`. Everything here is in **seconds**
(reaper-mcp's unit); convert from the `sec_per_beat` you already computed.

## 1. Velocity shaping (never a flat 96)

Velocity is dynamics *and* groove. Two notes at the same pitch with different velocities are two
different musical events.

- **Accent map**: emphasize the metric structure. In 4/4, beat 1 strongest, beat 3 medium,
  2 & 4 backbeat-strong for snares; offbeats lighter. A usable hi-hat pattern:
  `beat 1 = 100, the "&"s = 70, beats 2/3/4 = 85` — then add ±5 random jitter (item 4).
- **Ghost notes**: quiet (velocity ~20–45) snare/hat hits between the main hits give a groove
  its life. Sprinkle them on the "e" and "a" of beats, well below the backbeat.
- **Dynamic curve across a phrase**: don't hold one level. Crescendo into the phrase climax
  (item 4 of `songwriting`), back off at the resolution. A lead line might ramp velocity
  60→70→80→95 toward its high note, then settle to 75.
- **Layer-appropriate ranges**: leads/vocals 70–110 with wide variation; pads 55–80 (gentle);
  sub-bass 90–110 but *consistent* (the low end shouldn't wobble in level); drums use the full
  range so accents read.

## 2. Micro-timing (push, pull, and human jitter)

Real players don't hit the grid exactly, and they don't all sit *on* it.

- **Humanize jitter**: offset each note's start by a small random amount. Per layer (vary the
  per-note offset by note index so it's not identical):
  - Tight electronic drums: **±5–12 ms** (±0.005–0.012 s)
  - Live-feel drums / keys / guitar: **±15–30 ms**
  - Lush/loose parts (pads, ambient): **±20–40 ms**
  - Sub-bass and the kick: keep **tight** (≤±5 ms) so the low end stays locked.
- **Push / pull (intentional, not random)** — a feel, applied consistently to a whole part:
  - **Behind the beat (lay back)**: snare/vocals slightly late (+10–25 ms) → relaxed, soulful,
    hip-hop/neo-soul feel.
  - **Ahead (push)**: hats/rhythm parts slightly early (−5–15 ms) → urgent, driving, punk/DnB.
  - Keep the kick on the grid as the anchor; push/pull the parts *around* it.
- **Note lengths aren't the full grid**: a "quarter note" played staccato might be 0.5× its
  slot; legato lines overlap slightly (next note starts ~10–20 ms *before* the previous ends) so
  the synth glides/legato-triggers. Vary lengths — uniform durations sound typed.

## 3. Swing (apply it, don't just know it)

`music-theory` carries the swing math; this skill says *use* it where the genre wants it.
Delay every offbeat 8th (the "and") to `beat_start + sec_per_beat * (1 + s) / 2`:

- House/techno: usually straight (s≈0) or light swing (s≈0.1) on hats only.
- Hip-hop / trap / lo-fi / shuffle: **s≈0.5–0.6** on hats and snares for the lazy bounce.
- Apply swing to the *feel* layers (hats, plucks), not always the kick or sub.

## 4. Per-instrument feel templates (starting points)

Vary the random component by note index (no `Math.random` in this environment — derive jitter
from the note's position, e.g. alternate +offset/−offset or use a fixed pseudo-pattern).

| Part | Velocity | Timing | Length |
|---|---|---|---|
| **Kick** | 95–110, beat 1 hardest | on grid, ≤±5 ms | short |
| **Snare/clap** | 100–120 on 2 & 4; ghosts 20–40 | optional +10–20 ms lay-back | short |
| **Hi-hats** | accent map (item 1) + ±8 jitter | swing where genre wants | short, some open longer |
| **Sub bass** | 90–110, *consistent* | locked, ≤±5 ms | legato, ties to kick rhythm |
| **Lead** | 70–110, phrase curve | ±10–20 ms human | mix staccato/legato per phrasing |
| **Pads/chords** | 55–80, gentle swells | ±20–40 ms, loose | long, overlapping |
| **Pluck/arp** | 60–90, slight accent on downbeats | tight + light swing | short |

## 5. Velocity-to-timbre awareness

Many instruments map velocity to brightness/attack (velocity layers, filter-to-velocity), so
velocity *is* tone, not just loudness. If you've set up such a mapping via `set_fx_param`, lean
on it: hard accents come through brighter automatically — another reason flat velocity sounds
lifeless. (If a part needs a fixed timbre regardless of dynamics, automate the level instead and
keep velocity steadier.)

---

**Workflow:** take the shaped, developed note list from `songwriting`, then for each part apply
an accent/velocity curve (1), add the right timing jitter and any push/pull or swing (2–3) using
the per-instrument template (4) — then write it in one `reaper_add_midi_notes` batch. Keep the
kick and sub tight; let everything else breathe.
