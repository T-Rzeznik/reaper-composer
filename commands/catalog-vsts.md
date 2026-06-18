---
description: (Optional) Build or refresh the persistent VST catalog up front — scans every installed plugin, researches any not yet cataloged, and saves ~/.reaper-composer/vst-catalog.json. /reaper-composer:compose fills this catalog on its own as songs need plugins, so this is just an eager one-time scan after installing a batch of plugins.
---

You are running an **eager, full scan** of the user's installed plugins to build their durable
VST catalog. This is the deliberate "research everything now" pass that keeps `compose` fast —
during a normal build, `vst-setup` only catalogs the plugins the current song needs.

## What to do

1. Confirm Reaper is reachable: call `reaper_ping`. If it fails, tell the user to load the
   reaper-mcp bridge ReaScript in Reaper and stop.
2. Load the `vst-catalog` skill and follow it for the schema, storage location, and research
   tiers.
3. Run the **full diff**: read `~/.reaper-composer/vst-catalog.json` (or start empty),
   `reaper_list_installed_fx` (json), and research **all** uncataloged plugins — not just the
   current song's roles.
   - **Model-knowledge first** for recognized plugins (no web call); **one `WebSearch`** (plus at
     most one `WebFetch`) only for genuine unknowns. This keeps a large library cheap.
   - Mark any cataloged-but-missing plugins `installed: false` (keep the entry).
4. `Write` the merged catalog back in one pass (bump `scanned_at`).
5. **Report a summary**: X newly cataloged, Y total plugins known, Z marked uninstalled, and
   call out any plugins you couldn't classify confidently.

## Notes

- The catalog is machine-global and reused across all songs — run this once after installing new
  plugins, then forget about it.
- If the library is very large, this may take a while and use several web searches for obscure
  plugins; that's expected for the eager pass. Everyday composing doesn't need it — it fills the
  catalog lazily on its own.
