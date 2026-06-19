---
name: drum-maps
description: Build, store, read, and verify per-kit drum note maps so the composer triggers the right samples. Researches a drum VST's MIDI note→drum layout (model knowledge first, then the web) and persists it as a dedicated, hand-editable JSON file under ~/.reaper-composer/drum-maps/. Load inside vst-setup when a drum instrument needs its note map resolved, and whenever the user asks to look up / fix / verify a kit's drum mapping. Fixes the #1 drum bug: GM note numbers that miss where a kit's samples actually live.
---

# Per-kit drum maps (look it up once, reuse forever)

Drum samplers almost never follow General MIDI — each puts the kick/snare/hat on its own notes.
There's no MCP tool that reads a kit's layout, so we **research it (online if needed) and save it
to a file**, keyed to the plugin, then reuse it on every future song. The `vst-catalog` points at
these files; this skill owns their format, lookup, and verification.

## Where drum-map files live

```
~/.reaper-composer/drum-maps/<slug>.json
    (Windows: C:\Users\<user>\.reaper-composer\drum-maps\)
```

- **`<slug>`** = the plugin's display name, made filename-safe: keep letters/digits, replace any
  run of spaces/punctuation with a single `-`. `Superior Drummer 3` → `Superior-Drummer-3.json`;
  `EZdrummer 2` → `EZdrummer-2.json`; `Sitala` → `Sitala.json`.
- Use your normal filesystem tools (`Read`, `Write`, `Glob`). `Write` creates the
  `drum-maps/` parent dir automatically. This is **runtime user data — never committed** to the
  plugin repo. The user may hand-edit these files to correct a mapping; treat an existing file as
  the source of truth (don't overwrite a `verified: true` file without asking).

## File format

```json
{
  "schema_version": 1,
  "plugin": "Superior Drummer 3",
  "exact_fx_name": "VST3i: Superior Drummer 3 (Toontrack)",
  "mapping": "custom",
  "source": "web",
  "verified": false,
  "reference_url": "https://www.toontrack.com/...  (where you found it, if web)",
  "researched_at": "2026-06-19T00:00:00Z",
  "comment": "SD3 'GM' preset; the SDX library you loaded may differ — verify if drums sound wrong.",
  "notes": {
    "36": "kick",
    "38": "snare",
    "37": "snare rim / sidestick",
    "39": "clap",
    "42": "closed hat",
    "44": "pedal hat",
    "46": "open hat",
    "41": "low tom", "43": "mid tom", "45": "high tom",
    "49": "crash", "51": "ride"
  }
}
```

- `mapping` — `gm` (matches `music-theory` §5), `fixed` (a known pad layout, e.g. Sitala's
  chromatic-from-36), `custom` (kit-specific, from the docs), or `unknown` (couldn't determine).
- `source` — `model` (your own knowledge), `web` (researched), or `user` (hand-set/confirmed).
- `notes` — `{ "<midi_number>": "<drum>" }`. **MIDI numbers, never octave labels** — VSTs
  disagree on whether 36 is "C1" or "C2"; the number is unambiguous (`music-theory` §2/§5). Cover
  at least kick, snare, closed hat, open hat, clap; add toms/crash/ride/perc when the genre uses
  them. Many kits offer alternate articulations on extra notes — record the main one per drum.
- `verified` — `false` from model/web knowledge; `true` only once it's been confirmed against the
  actual loaded instrument (user audition, or a map we set ourselves as in `local-assets`).

## Resolving a kit's map (the routine)

Given a drum instrument's `name` + `exact_fx_name`:

1. **Read** `~/.reaper-composer/drum-maps/<slug>.json`. If it exists, use it — done (offer to
   verify if `verified: false`). The maps accumulate; you research each kit once.
2. **Tier 1 — model knowledge.** If you know the kit's default layout (Sitala = chromatic pads
   from 36; GM-ish acoustic samplers like MT Power Drum Kit / SSD5 Free / DrumGizmo; EZdrummer /
   Superior Drummer default GM preset…), write the file from knowledge, `source: "model"`.
3. **Tier 2 — look it up online.** If you don't know it, do a focused `WebSearch` like
   `"<plugin name> MIDI note mapping kick snare hi-hat"` or `"<plugin> drum map note numbers"`,
   and at most one or two `WebFetch`es of the manual / developer page / a reputable forum thread.
   Extract the note→drum numbers, write the file with `source: "web"` and the `reference_url`.
   Prefer the official manual; corroborate a forum answer if it's the only source.
4. **If the web is inconclusive**, write the file with `mapping: "unknown"` and a best-effort
   `notes` (GM as a guess) plus a `comment` saying it's unconfirmed — then **flag it** so it gets
   verified before the composer relies on it. Don't loop on searches; one good pass.

## Verifying a map (turn `unknown`/unconfirmed into `verified`)

We can't "hear" individual notes through the analyze tools, but the user can. When a map is
unverified and it matters (drums are central to the genre), offer a quick check:

1. On the loaded drum track, write a short, slow probe with `reaper_add_midi_notes`: one hit per
   drum you mapped, spaced ~0.5 s apart, and tell the user the order ("kick, snare, closed hat,
   open hat, clap").
2. `reaper_transport_play` and ask: did each land on the right sound? If something's off (e.g.
   "the 3rd one is a tom, not a hat"), correct that note in the file.
3. Set `verified: true`, `source: "user"`, and delete the probe (`reaper_delete_item`) before
   composing for real.

This is optional and user-driven — don't force it, but it's the only reliable confirmation, so
offer it whenever a kit's map is unconfirmed.

## Handing the map to the rest of the pipeline

`vst-setup` calls this routine for the drum track, then puts the resolved `notes` (+ `mapping`/
`verified`) into the **track map**; the composer writes drum notes at those MIDI numbers instead
of GM (`music-theory` §5). The `vst-catalog` entry for the kit stores a pointer
(`drum_map: { mapping, map_file: "drum-maps/<slug>.json", verified }`) so future runs find the
file instantly without re-researching.
