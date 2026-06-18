---
name: local-assets
description: Use a user-provided folder of samples and MIDI files in the song. Scans the folder, catalogs audio (one-shots, loops, risers, vocal chops) vs MIDI clips, then places audio on the timeline with reaper_insert_media, routes drum one-shots into a sampler for MIDI triggering, and imports .mid files as clips. Load whenever the user points at a folder of their own sounds ("use the samples in C:\...", "there's MIDI in this folder").
---

# Using a local folder of samples / MIDI

When the user points at a folder, you can pull their own sounds into the song. You have two
capabilities here:

- **Read the folder** with your normal filesystem tools (`Glob`, `Read`) — the project runs on
  the same machine as Reaper, so a path the user gives you is readable by both.
- **Place files** with `reaper_insert_media(track_index, file_path, start_sec)` — imports an
  audio file as an audio item, or a `.mid` file as a MIDI clip, at a chosen time. Pass an
  **absolute path**.

## Step 1 — scan and catalog

1. Confirm the absolute folder path with the user.
2. `Glob` for the relevant types: audio (`**/*.{wav,aiff,aif,flac,mp3,ogg}`) and MIDI
   (`**/*.{mid,midi}`).
3. Classify each file from its **name** (and subfolder) into roles — this is heuristic but
   usually reliable:
   - drums/one-shots: `kick`, `snare`, `clap`, `hat`/`hh`, `808`, `tom`, `crash`, `ride`, `perc`
   - loops: `loop`, `groove`, `beat`, `drumloop` (often tagged with BPM, e.g. `_128_`)
   - tonal: `bass`, `chord`, `melody`, `lead`, `pluck`, `pad`, `key`
   - transitions/fx: `riser`, `uplifter`, `downlifter`, `impact`, `boom`, `sweep`, `fx`
   - vocals: `vox`, `vocal`, `chop`, `acapella`, `phrase`
   - MIDI: `.mid` files — chord progressions, melodies, drum patterns, basslines
4. Note any **BPM** (`120`, `_128_`, `140bpm`) and **key** (`Cmin`, `F#`, `Amaj`) tags in
   filenames — they tell you what fits the project tempo/key.
5. Present a short catalog and ask how to use it (or map it to the arrangement yourself and
   confirm). Don't silently dump everything in.

## Step 2 — use the files

### Audio loops (drum loops, melodic loops)
Place at the start second of each section they belong to: `reaper_insert_media(track, path,
section_start_sec)`. Use the `music-theory` bar grid so the loop lands on the downbeat.
- **Tempo caveat:** Reaper does NOT time-stretch an inserted loop to the project tempo unless
  the item is set to stretch. If a loop's tagged BPM differs from the project tempo, warn the
  user it may not line up, and prefer loops matching (or close to) the project BPM. Honest is
  better than silently-out-of-time.

### Drum / instrument one-shots → sampler (preferred for drums)
For programmable drums, route one-shots into a sampler so the composer can write patterns:
1. Set up a sampler track (see `recommended-vsts` — **Sitala** is the easy pick) via `vst-setup`.
2. **Important limitation:** the MCP can't load a file into a sampler's pads automatically
   (there's no file-path parameter for that). So tell the user which one-shots to drag onto
   which pads in the sampler, then the composer triggers them with MIDI (`add_midi_notes`)
   using the genre's drum patterns.
- If the user would rather not map a sampler, fall back to **dropping each one-shot as an audio
  item** at its hit time with `reaper_insert_media` — simpler, but not pattern-editable.

### One-off audio (risers, impacts, vocal chops, FX)
Drop directly as audio items with `reaper_insert_media` at the exact moment they hit (e.g. a
riser across the last bars of a build, an impact on a drop's downbeat).

### MIDI files (.mid)
- **Preserve a performance:** `reaper_insert_media(track, path, section_start_sec)` imports the
  `.mid` as a MIDI clip intact on an instrument track — best when the user wants *that* exact
  part. Make sure the track already has an instrument loaded (via `vst-setup`).
- **Adapt it instead:** if they want it transposed/retimed/reworked, `Read` the catalog context,
  decide the changes, and write fresh notes with `reaper_add_midi_notes` (using `music-theory`
  for transposition) rather than importing.

## Step 3 — report
Tell the user exactly what you placed where (file → track → section/time), what you routed to a
sampler for them to map, and flag anything skipped (wrong BPM, unsupported format, ambiguous).

This folder is a *source of material*, not a replacement for the arrangement — fit the user's
sounds into the plan from the `arranger`, don't let a pile of samples dictate the song.
