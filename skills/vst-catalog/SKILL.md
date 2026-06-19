---
name: vst-catalog
description: Build and read a persistent, per-plugin catalog of the user's INSTALLED VSTs — what each plugin IS (synth/sampler/effect + synthesis type), what it's GOOD FOR (roles, genres, strengths), and how to dial a starting sound. Stored machine-global at ~/.reaper-composer/vst-catalog.json and updated incrementally (only newly-installed plugins get researched). Load this inside vst-setup BEFORE matching plan roles to plugins so selection uses real per-plugin knowledge instead of blind name-matching, and load it when the user asks to (re)scan or refresh their VST catalog.
---

# Persistent VST catalog

The user's installed plugins are the same across every song they make, but `vst-setup`
currently re-discovers them blind every run. This skill builds a **durable catalog** of what
each installed plugin actually is and what it's good for, so plugin selection draws on real
knowledge that accumulates over time instead of guessing from the name.

The catalog is machine-global (plugins are a property of the machine, not a song), researched
**once per plugin**, and reused forever.

## Where the catalog lives

```
~/.reaper-composer/vst-catalog.json        (Windows: C:\Users\<user>\.reaper-composer\)
```

Use your normal filesystem tools (`Read`, `Write`, `Glob`) — the plugin runs on the same
machine as Reaper. `Write` to that path **creates the `.reaper-composer` parent dir
automatically**; you don't need to (and can't) `mkdir` it. This is runtime user data — it is
never committed to the plugin repo.

## Schema

Keyed by the **exact FX name** — the verbatim string `reaper_add_fx_to_track` needs (with its
`VST3:` / `VST3i:` prefix; instruments carry the `i`). That way a catalog lookup yields a value
you can load directly.

```json
{
  "schema_version": 1,
  "scanned_at": "2026-06-18T13:20:00Z",
  "plugins": {
    "VST3i: Vital (Vital Audio)": {
      "name": "Vital",
      "exact_fx_name": "VST3i: Vital (Vital Audio)",
      "vendor": "Vital Audio",
      "kind": "instrument",
      "subtype": "wavetable synth",
      "roles": ["lead", "bass", "pad", "pluck", "fx-riser"],
      "genres": ["edm", "house", "trap", "future-bass"],
      "strengths": "Serum-like wavetable; supersaws, growls, evolving pads, FX risers. Free.",
      "starting_sound": "Osc1 saw/wavetable; lowpass cutoff to taste; unison 5–7 voices for a supersaw; env attack 0 for plucks.",
      "free": true,
      "installed": true,
      "source": "model",
      "researched_at": "2026-06-18T13:20:00Z"
    },
    "VST3i: Sitala (Decomposer)": {
      "name": "Sitala",
      "exact_fx_name": "VST3i: Sitala (Decomposer)",
      "vendor": "Decomposer",
      "kind": "instrument",
      "subtype": "drum sampler",
      "roles": ["drums", "kick", "snare", "clap", "hihat", "perc", "808"],
      "genres": ["edm", "house", "trap", "techno"],
      "strengths": "16-pad one-shot drum sampler. Free. You load your own samples onto pads.",
      "starting_sound": "Load one-shots per pad; tune/decay per pad to taste.",
      "drum_map": {
        "mapping": "fixed",
        "map_file": "drum-maps/Sitala.json",
        "verified": false
      },
      "free": true,
      "installed": true,
      "source": "model",
      "researched_at": "2026-06-18T13:20:00Z"
    },
    "VST3: Pro-Q 3 (FabFilter)": {
      "name": "Pro-Q 3",
      "exact_fx_name": "VST3: Pro-Q 3 (FabFilter)",
      "vendor": "FabFilter",
      "kind": "effect",
      "subtype": "EQ",
      "roles": ["eq", "mixing"],
      "genres": ["any"],
      "strengths": "Transparent dynamic/linear-phase EQ; surgical cuts and broad tonal shaping.",
      "starting_sound": "Add bands by name via list_fx_params; HP rumble <30Hz, gentle high shelf for air.",
      "free": false,
      "installed": true,
      "source": "model",
      "researched_at": "2026-06-18T13:20:00Z"
    }
  }
}
```

Field notes:
- `kind` — `instrument` or `effect`. `subtype` — what it actually is (wavetable synth, FM synth,
  drum sampler, amp sim, EQ, compressor, reverb, delay, …).
- `roles` / `genres` — the matchable indexes `vst-setup` queries. Use lowercase, hyphenated.
- `installed` — `false` for plugins that were once cataloged but no longer appear in
  `reaper_list_installed_fx`. Keep the entry (don't delete) so a reinstall is instant.
- `source` — `model` (filled from your own knowledge) or `web` (researched via WebSearch).
- `drum_map` — **only for drum instruments (samplers/kits); this fixes the #1 drum bug: the
  composer writing GM note numbers that don't match where the kit's samples actually live.** It's
  a small **pointer**, not the map itself — the full note layout lives in a dedicated, hand-editable
  file owned by the `drum-maps` skill:
  - `mapping` — `gm` (matches `music-theory` §5 — many acoustic-kit samplers like MT Power Drum
    Kit and SSD5 Free are GM-ish), `fixed` (a known pad layout, e.g. Sitala's chromatic-from-36),
    `custom` (kit-specific layout from the docs), or `unknown` (couldn't determine).
  - `map_file` — relative path to the kit's map file, `drum-maps/<slug>.json` (see `drum-maps`).
  - `verified` — mirrors the file's flag: `false` from model/web knowledge, `true` once confirmed.

## Read-first protocol

On load, `Read` `~/.reaper-composer/vst-catalog.json`.
- **Missing** → first run; start from an empty catalog (`{ "schema_version": 1, "plugins": {} }`).
- **Present but unparseable** → treat as first-run (empty) rather than crashing the build; you
  may note to the user that the catalog was reset.

## Incremental update (the diff)

1. `reaper_list_installed_fx` with `response_format: "json"` → the live set of exact FX names.
2. Compute:
   - `to_research = live_names − catalog_keys` — installed but not yet cataloged.
   - `gone = catalog_keys − live_names` — cataloged but no longer installed → set their
     `installed: false` (do not delete or re-research).
   - Re-mark any returning plugin `installed: true`.
3. **Only research `to_research`. Never re-research an existing entry.**

## Researching a plugin — model-knowledge first

For each plugin in `to_research`:

- **Tier 1 — your own knowledge (no web call).** For any plugin you recognize (Vital, Serum,
  Surge XT, Sitala, TAL-NoiseMaker, OB-Xd, Dexed, Spitfire LABS, FabFilter Pro-Q, TDR Nova,
  Valhalla Supermassive, MT Power Drum Kit, SSD5 Free, Ample Bass/Guitar, Neural Amp Modeler,
  Ignite Emissary, …), fill the entry straight from knowledge. Set `source: "model"`. This is
  the common case — most installed plugins are well-known.
- **Tier 2 — web only for genuine unknowns.** If a name is obscure/boutique and you can't
  classify it confidently, do **one** `WebSearch` (developer + plugin name), and at most one
  `WebFetch` of the developer/product page. Extract kind/subtype/roles/genres/strengths. Set
  `source: "web"`. If even that is inconclusive, store a best-effort entry with a note and move
  on — don't loop.

For every entry, fill `roles`, `genres`, `strengths`, and a short `starting_sound` hint (which
params to reach for — you'll still confirm real param names later with `reaper_list_fx_params`).

**For any drum instrument (sampler/kit), also resolve its `drum_map`** — this is what stops the
composer from writing GM notes that miss the kit's actual samples. **Delegate to the `drum-maps`
skill**: run its resolve routine (read the kit's `drum-maps/<slug>.json` if it exists; else
research it — model knowledge first, then a focused web lookup of the kit's note mapping — and
write the file). Then store the small pointer here: `drum_map: { mapping, map_file, verified }`.
If the web lookup is inconclusive, the file is written `mapping: "unknown"` so the composer flags
it rather than guessing — don't assert kick/snare notes you're unsure of.

## Cost control — lazy by default

During a normal `vst-setup` run, **do not research the whole library.** Research only the
uncataloged plugins that plausibly serve the **roles the current plan needs** (prefilter
`to_research` by name/type — e.g. for a drum role, look at sampler/drum-named plugins first).
A typical song needs ~6–10 instrument roles, most already cataloged, so the common path is
cheap.

Guard the web tier with a soft cap of **~15 new web-researched plugins per run**. If the
backlog is larger, do the Tier-1 (model-knowledge) pass on what you can and tell the user to
run `/reaper-composer:catalog-vsts` for a full, deliberate sweep.

`/reaper-composer:catalog-vsts` is the **eager** entry point: it researches *all* of
`to_research`, not just the current song's roles.

## Write protocol

Read → merge new/updated entries in memory → `Write` the whole JSON back **once**, bumping
`scanned_at`. One write per scan. Never partial-write mid-research.

## Selection algorithm (how vst-setup uses the catalog)

For each role in the approved plan:
1. Query the catalog for installed entries whose `roles` (and ideally `genres`) match the role
   and the song's genre.
2. Rank by genre fit, then `strengths`. Pick the best **installed** match and load it by its
   `exact_fx_name`.
3. Use its `starting_sound` as the opening point for parameter setup. **For a drum instrument,
   resolve its map via `drum-maps` (read the pointed-to `map_file`) and pass the actual note layout
   into the track map** so the composer writes notes where the samples really live (a
   `mapping: "unknown"` map signals vst-setup to flag it / verify / prefer a known-mapped sampler).
4. **Only if the catalog has no suitable installed match**, fall back to the `recommended-vsts`
   skill (suggest a free plugin + the install → rescan loop). After a rescan + reinstall, the
   new plugin gets cataloged on the next diff.

This replaces blind name-matching with a real, growing knowledge base — and the more songs the
user makes, the more complete their catalog becomes.
