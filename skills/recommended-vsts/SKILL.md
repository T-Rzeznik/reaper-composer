---
name: recommended-vsts
description: A catalog of solid FREE VST instruments and effects by role (EDM/hip-hop/rock drums, 808/sub/electric bass, synth leads/pads, distortion guitar amp sims, pianos/keys, plus mixing FX), with what each is good for and how to find it. Load when the user lacks a suitable installed plugin for a role (e.g. no real drum sampler) and needs a recommendation, or when they ask what free VSTs to install. The reaper-mcp server can only use INSTALLED plugins, so recommending → installing → rescanning is the loop.
---

# Recommended free VSTs by role

Use this when `reaper_list_installed_fx` turns up nothing appropriate for a role — most often
**drums** (don't force a synth to play a drum part; recommend a real drum sampler instead).
Everything here is free. Match the genre's needs (from the genre skill) to a recommendation,
suggest 1–2 options, and walk the user through installing + rescanning (see bottom).

Prefer hosts that are **free and standalone** (no paid Kontakt full version needed): Vital,
Surge XT, Sitala, Spitfire LABS app, Decent Sampler.

## Drums

| Need | Free pick | Notes |
|---|---|---|
| **EDM / electronic kit** | **Sitala** (Decomposer) | Dead-simple 16-pad drum sampler; load any one-shots (kick/clap/hat/perc). Ideal for EDM/house/techno. |
| **Hip-hop / trap (808s + kit)** | **Sitala** + free 808/trap one-shots | Map an 808 one-shot to a pad, or play the 808 as a pitched sub with **Vital/Surge** (see Bass). |
| **Acoustic / rock / pop kit** | **MT Power Drum Kit 2** (Manda Audio) | Free, mixed acoustic kit with a pattern library; great for rock/pop. |
| **Rock / metal kit** | **Steven Slate Drums 5 Free (SSD5 Free)** | Free curated kit, punchy and mix-ready; good for metal/rock. |
| **Open-source acoustic** | **DrumGizmo** | Free multi-mic sampled kits if you want full control. |

> Key point: if the genre needs drums and no drum sampler is installed, **recommend one of these
> rather than loading a synth on the drum track.** A synth playing GM note numbers will not sound
> like drums.

## Bass

| Need | Free pick | Notes |
|---|---|---|
| **808 / sub bass** | **Vital** or **Surge XT** | Sine/triangle sub patch with glide for sliding 808s; saturate to read on small speakers. |
| **Synth bass (reese/growl)** | **Vital**, **Surge XT** | Wavetable; great for EDM/future-bass mid-bass layers. |
| **Electric bass (fingered)** | **Ample Bass P Lite II** (Ample Sound) | Free sampled P-bass for rock/metal/funk basslines. |

## Synths — leads, pads, plucks, chords

| Need | Free pick | Notes |
|---|---|---|
| **Modern wavetable (EDM lead/bass/pad)** | **Vital** | The standout free synth — Serum-like; supersaws, growls, pads, FX risers. First choice for EDM/house/trap melodic parts. |
| **Powerful hybrid all-rounder** | **Surge XT** (open-source) | Huge preset library, does almost anything; leads, pads, plucks, FX. |
| **Classic virtual-analog** | **TAL-NoiseMaker** | Warm analog leads/basses/pads; lightweight. |
| **Vintage poly (pads/strings-ish)** | **OB-Xd** (discoDSP) | Oberheim-style analog pads and brass. |
| **FM (bells, e-piano, metallic bass)** | **Dexed** | DX7 emulation; FM tones, plays .syx patches. |

## Guitar (incl. distortion / metal)

Distorted guitar = a guitar tone **instrument or DI** run into an **amp sim + cab impulse**.

| Need | Free pick | Notes |
|---|---|---|
| **High-gain amp (metal/rock)** | **Ignite Amps Emissary** + **Ignite Amps NadIR** (cab IR loader) + a free cab impulse | Free, genuinely heavy. Add **TSE808** (free) as a boost in front for tight metal chugs. |
| **Amp captures / modern tones** | **Neural Amp Modeler (NAM)** | Free, open; load community amp captures + a cab IR. |
| **Playable guitar instrument (MIDI)** | **Ample Guitar M Lite II** (acoustic), **Spitfire LABS** electric guitars | For writing guitar parts as MIDI; route a clean electric into an amp sim for distortion. |

> Note: convincing MIDI metal rhythm guitar is hard — sampled guitar + amp sim helps, but tell
> the user it's an approximation. Power-chord/palm-mute tightness (short notes, locked timing)
> matters more than the plugin.

## Keys, pianos, orchestral, textures

| Need | Free pick | Notes |
|---|---|---|
| **Acoustic / electric pianos, strings, choirs, odd textures** | **Spitfire LABS** (free app + free instrument packs) | Enormous free library; great for chords, pads, cinematic beds, lo-fi keys. |
| **Free sampler for community libraries** | **Decent Sampler** | Loads thousands of free sample libraries. |
| **Simple piano** | **Keyzone Classic** | Lightweight free acoustic/electric piano. |

## Mixing & FX (free — useful to the mix-engineer too)

| Role | Free pick |
|---|---|
| EQ | **TDR Nova** (dynamic EQ), **MeldaProduction MEqualizer** |
| Compressor | **TDR Kotelnikov**, **MCompressor** |
| Reverb | **Valhalla Supermassive** (also delay), **OrilRiver** |
| Delay | **Valhalla Supermassive** |
| Limiter | **LoudMax** |
| Bundle | **MeldaProduction MFreeFXBundle** (many of the above in one install) |

## The install → rescan loop (important)

The reaper-mcp server can only load plugins Reaper has **scanned**. So when you recommend
something the user doesn't have:

1. Suggest 1–2 specific free options for the role (developer + plugin name so they can search).
2. Tell them to install it, then in Reaper rescan: **Options → Preferences → Plug-ins → VST →
   "Re-scan"** (or "Clear cache and re-scan"). VST3 installs to the standard folder; if Reaper
   doesn't find it, point its VST path at the install folder and rescan.
3. After they confirm, call `reaper_list_installed_fx` again, find the exact name (with its
   `VST3:` / `VST3i:` prefix), and load it.
4. If they'd rather not install anything right now, proceed with the closest installed
   alternative and **clearly note the compromise** (e.g. "using a synth sub for drums — a real
   drum sampler like Sitala would sound much better").
