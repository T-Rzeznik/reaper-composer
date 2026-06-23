---
name: stem-generation
description: Generate brand-new instrument/texture audio stems from a text prompt with a local, $0-per-clip model (Meta MusicGen-small via Hugging Face transformers), then drop them on the Reaper timeline. Use when the user wants AI-generated audio parts (a pad bed, a texture, an ambient layer, a bassline sketch, a vocal-chop-style hook) rather than MIDI driving a VST — e.g. "generate a stem for…", "make me an AI pad layer", "I want a generated texture under the chorus". The agent feeds the song's key/BPM/section context into the prompt. Complements the MIDI composer; does not replace it for precise melodic lines.
---

# Generating new audio stems (local MusicGen, $0/clip)

You can synthesize new audio parts from a text description and place them in the song. This is
the *generation* counterpart to `local-assets` (which uses the user's own files): generate a WAV
to disk with a local model, then drop it on the timeline with `reaper_insert_media`. No new MCP
surface is needed — the integration is identical to placing any audio item.

**Backend:** Meta's **MusicGen-small** run locally via Hugging Face `transformers`. It is free
per clip (no API key, no per-use cost), runs on CPU (slow) or a CUDA GPU (fast), and downloads
~1.2 GB on first use. The helper lives beside this skill at `scripts/generate_stem.py`.

## What this is good (and bad) at — be honest with the user

- **Good for:** beds, pads, textures, ambient layers, lo-fi/loop sketches, "vibe" material,
  rough bassline/drum-loop ideas. Things where *texture matters more than exact notes*.
- **Weak at:** precise melodies, tight key adherence, clean single hits, anything that must lock
  to the grid. For those, the **MIDI composer is still better** — say so.
- Output is a *sketch/texture*, not a radio-ready stem. Key/tempo are honored only
  approximately (you put them in the prompt; verify by ear).
- It produces a continuous clip that **drifts off-grid** — you must sync it (Step 4) before
  trusting placement.

If the user wants a clean, in-key melodic or drum part, steer them to the normal MIDI pipeline
instead of generating a stem.

## Step 0 — one-time setup check

The model needs Python deps. Before the first generation, check they're present and, if not,
tell the user the single install line (don't try to install silently):

```
pip install "transformers>=4.40" torch scipy
```

Run a quick probe (the script self-reports a clear error + this same install line if deps are
missing): if `python <skill-dir>/scripts/generate_stem.py --help` errors on import, surface the
install instructions and stop until the user has installed them. A CUDA GPU is optional but makes
generation many times faster; on CPU a single ~8 s clip can take 1–3 minutes — warn the user.

## Step 1 — gather context

Pull from `song-state` (or ask if missing):
- **BPM** and **key** of the project,
- the **section** the stem is for and its bar length → seconds via the `music-theory` bar grid,
- the **role** the user wants (pad / texture / bass / lead-ish / fx / loop).

## Step 2 — build the prompt

Compose a short, concrete English description. MusicGen responds to genre + instrument + mood +
production words. Keep it to one instrument/role and explicitly **exclude** what you don't want.

Role recipes (adapt to the genre skill in play):
- **Pad / bed:** `"warm analog pad, lush, slow attack, {genre}, no drums, no bass"`
- **Texture / ambient:** `"airy ambient texture, granular shimmer, evolving, no rhythm"`
- **Bass sketch:** `"deep rolling sub bass, dry, {genre}, no drums, no melody"`
- **Loop / groove:** `"{genre} drum loop, punchy, dry, looping"`
- **Hook / lead-ish:** `"simple {genre} synth lead motif, bright, no drums"` (expect rough pitch)

Always fold in tempo and key — either in the prompt text or via the script's `--bpm`/`--key`
flags (which append them for you). Example final prompt:
`"warm analog pad, lush, slow attack, deep house, no drums, no bass"` + `--bpm 124 --key "F minor"`.

## Step 3 — generate to disk

Write stems to the runtime data dir (never into the project or the plugin repo):
`~/.reaper-composer/stems/<project-name>/<role>-<section>.wav` (Windows:
`C:\Users\<user>\.reaper-composer\stems\…`).

Run the helper with the `Bash` tool (it prints the final WAV path on stdout):

```
python "<skill-dir>/scripts/generate_stem.py" \
  --prompt "warm analog pad, lush, slow attack, deep house, no drums, no bass" \
  --bpm 124 --key "F minor" \
  --duration 8 \
  --out "C:/Users/<user>/.reaper-composer/stems/<project>/pad-chorus.wav"
```

Pick `--duration` to roughly cover the section (it can loop to fill). Generate one role per call.
Tell the user it's running and that CPU generation is slow.

## Step 4 — sync, then place (the critical part)

MusicGen does **not** emit bar-locked audio, so treat the clip like an off-tempo loop:

1. `reaper_insert_media(track_index, wav_path, section_start_sec)` onto its **own** track
   (one stem = one track, so it can be muted/mixed/replaced independently). Use the
   `music-theory` bar grid so it lands on the section downbeat.
2. **Match it to the grid.** Reaper won't time-stretch on its own — if the generated clip's
   internal tempo differs from the project (it usually does, slightly), it will drift. Set the
   item to stretch to the project tempo, or trim/loop it to the section's exact bar length, so
   downbeats line up. Honest > silently-out-of-time: if it won't sit in the grid cleanly, tell
   the user and offer to regenerate (a new `--seed`) or shorten the section it covers.
3. Audition the section to confirm it sits with the existing parts (key clash, masking).

## Step 5 — report

Tell the user exactly what you generated and placed: prompt used → file → track → section/time,
how long it took, and any honest caveats (pitch drift, had to time-stretch, key felt off).
Offer to **regenerate with a different seed/prompt** if they don't like it — generation is cheap
to retry. Stems are *material added to the arrangement*, not a replacement for it.

> Generated WAVs under `~/.reaper-composer/stems/` are runtime user-machine data — **never commit
> them to the plugin repo.**
