---
name: mixing
description: How to mix and balance a Reaper project through reaper-mcp — running the analyze tools (which render the master and measure LUFS, true peak, clipping, per-band balance, stereo width, plus optional Gemini listening feedback), interpreting those metrics against genre targets, and translating findings into concrete level/EQ/pan/send fixes in an analyze→fix→re-analyze loop. Load this for any mixing or "balance the mix" task.
---

# Mixing a Reaper project

Composing writes the notes; mixing makes them sit together and hit the right loudness. This is
the only channel through which you can effectively "hear" the result, so lean on it.

## The analyze tools (read `reaper-mcp-reference` first)

- **`reaper_analyze_project`** — the one-call path. It **renders the master mix to a temp file**,
  measures it with local DSP, and (unless `include_ai=false`) sends a small proxy + the metrics
  to **Gemini** for written, grounded feedback. It writes a temp file but does **not** modify or
  export the project.
- **`reaper_analyze_mix`** — same analysis on an audio file you already have (pass `audio_path`).
- **Dependencies & graceful degradation:** the analysis needs the server's optional deps
  (`pip install -e .[analyze]`), and the AI layer needs `GEMINI_API_KEY`. **Try `include_ai=true`
  first; if it errors (missing key/deps), retry with `include_ai=false` to get the DSP metrics
  alone.** Never hard-fail the mix because the AI layer isn't configured — the numbers are still
  fully actionable. If even DSP analysis is unavailable, tell the user what to install and fall
  back to balancing by structure/knowledge.

These tools report the **master mix**, not per-track levels — you reason about the whole and
adjust individual tracks to fix it.

## Reading the metrics

| Metric | What it tells you | Act when |
|---|---|---|
| **Integrated LUFS** | Overall loudness | Off the genre target (below) |
| **True/sample peak** | Headroom / clipping | Peak > -1 dBTP, or any clipped samples → pull back |
| **Crest factor** | Dynamics (peak-to-loudness) | Very low = squashed; very high = lifeless/uneven |
| **Per-band balance** | Tonal balance | A band sticks out → boomy (low), muddy (low-mid), harsh (high-mid), thin (no lows) |
| **Stereo correlation/width** | Mono-compatibility | Low end not centered, or correlation near -1 (phase issues) |

### Rough LUFS targets by genre (integrated)
- Loud/club EDM, festival, dubstep: **-8 to -6**
- House, trap, pop-leaning: **-9 to -7**
- Metal/rock: **-9 to -7** (keep some crest so it punches)
- More dynamic / cinematic / lo-fi: **-14 to -10**
These are mastering-ballpark; prioritize **no clipping and clean balance** over hitting a number.

## Translating findings into reaper-mcp moves

- **Loudness too low / too high** → nudge `set_master_volume_db`, or raise/lower groups of
  tracks with `set_track_volume_db`. Re-analyze; don't overshoot.
- **Clipping / no headroom** → pull down the offending tracks (usually kick/bass/lead) or the
  master; check the low end first.
- **Frequency imbalance** → EQ on the offending track via `set_fx_param` (look up the EQ's real
  param names with `list_fx_params` first — never assume). Boomy → cut lows on non-bass tracks;
  harsh → dip high-mids on leads/cymbals; muddy → cut low-mids on pads/guitars.
- **Masking** (two sounds fighting) → carve a dip in one where the other lives, or pan them apart
  with `set_track_pan`.
- **Width / mono issues** → keep kick + sub **centered and mono**; spread pads/hats with pan;
  if correlation is bad, narrow the offending wide element.
- **Space/glue** → bus reverb/delay via `add_send` rather than per-track, and keep sends modest.

## The loop

1. `reaper_analyze_project` (AI on; fall back to DSP-only if it errors).
2. Identify the 1–3 biggest issues (loudness, clipping, the worst band, mono-compat).
3. Apply targeted fixes with the tools above. Report each change in plain language.
4. Re-analyze to confirm it improved. **Cap at ~3 passes** — stop when it's balanced and within
   headroom, or when further moves stop helping. Don't chase a perfect number forever.

Make decisive engineering choices; explain the "why" briefly so the user can learn the move.
