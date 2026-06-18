# 🎛️ reaper-composer

**Generate complete, playable songs inside [Reaper](https://www.reaper.fm/) from a single plain-English request.**

`reaper-composer` is a [Claude Code](https://claude.com/claude-code) plugin that turns a prompt
like *"future bass, uplifting, in the style of Illenium"* into a fully arranged Reaper
project — tracks created, instruments and effects loaded, MIDI written, and automation drawn —
section by section, with you approving the creative direction along the way.

It drives the DAW through a companion MCP server,
**[reaper-mcp](https://github.com/t-rzeznik/reaper-mcp)**, which exposes ~54 tools for
controlling Reaper. This repo is the "brain" (musical knowledge + orchestration); reaper-mcp
is the "hands" (DAW control). **You need both.**

---

## ✨ What it does

```
You:  /reaper-composer:compose deep house, late-night rooftop vibe, ~124 BPM

  ⓪ Discovery    → (only if your idea is fuzzy or genre-less) a back-and-forth
                   conversation that turns a vibe into a concrete creative brief
  ① Arranger     → drafts a section-by-section plan (structure, key, tempo,
                   instrumentation) and shows it to you for approval
  ② VST Setup    → creates & names tracks, loads the right synths/FX, dials in
                   starting sounds and routing
  ③ Composer     → writes MIDI, FX moves, and automation section by section,
                   streaming progress, and auditions the result

  → A finished, playable Reaper project. (Export to audio only if you ask.)

  ④ Mix (opt-in) → /reaper-composer:mix — analyzes the master (loudness, headroom,
                   tonal balance, stereo) and applies level/EQ/pan/send fixes
```

You stay in control: the arranger pauses for your sign-off before anything touches Reaper,
nothing is rendered/bounced to a file unless you explicitly ask, and the mix pass only runs
when you invoke it.

**Don't have a genre in mind?** Start with `/reaper-composer:discover` instead — just describe
the *feeling* ("something dreamy but with a hard-hitting drop", a movie scene, two artists you
want to blend). It conversates with you, translating vague language into musical decisions and
even blending genres, until your idea is concrete — then offers to build it. (`compose` also
falls back to this automatically when a request comes in fuzzy.)

---

## 🏗️ How it's built

Focused sub-agents in a pipeline (three for composing, plus an opt-in mix engineer), with all
genre knowledge factored out into reusable **skills** — so the agents stay genre-agnostic and
adding a new genre never touches agent code.

| Piece | Role |
|---|---|
| `commands/compose.md` | `/reaper-composer:compose` — the orchestrator that runs the pipeline |
| `commands/discover.md` | `/reaper-composer:discover` — brainstorm a vibe into a brief, then build |
| `commands/mix.md` | `/reaper-composer:mix` — opt-in mix/balance pass on the current project |
| `agents/arranger.md` | Turns intent into an approved song plan (no DAW access) |
| `agents/vst-setup.md` | Builds the Reaper session: tracks, instruments, FX, routing |
| `agents/composer.md` | Writes all MIDI, FX, and automation; auditions the song |
| `agents/mix-engineer.md` | Analyzes the master and balances levels/EQ/pan/sends (opt-in) |
| `skills/vision-discovery/` | Conversational discovery for fuzzy / genre-less / hybrid ideas |
| `skills/music-theory/` | Lookup tables: MIDI notes, scales, chords, timing/swing math, drum map |
| `skills/mixing/` | How to read the analyze tools and translate metrics into mix fixes |
| `skills/reaper-mcp-reference/` | The reaper-mcp tool contract + hard-won conventions |
| `skills/genre-*/` | Per-genre musicology (EDM, house, trap, metal, rock & roll) |
| `skills/genre-template/` | Copy-to-create scaffold for new genres |

**Design principle:** agents are general; genres are data. Every genre skill is just Markdown —
tempo/structure tables, drum patterns, synth archetypes, harmony, and signature production moves —
so the system grows by writing knowledge, not code.

---

## 🚀 Quick setup

You're wiring together two pieces: the **reaper-mcp server** (controls Reaper) and **this
plugin** (tells it what to play).

### 1. Set up Reaper + reaper-mcp (the "hands")

Follow the [reaper-mcp README](https://github.com/t-rzeznik/reaper-mcp), which covers:

1. Install [reaper-mcp](https://github.com/t-rzeznik/reaper-mcp) (Python MCP server) and add it
   to your Claude Code MCP config.
2. Load the bridge ReaScript inside Reaper (**Actions → Show action list → ReaScript: Load**).
   ⚠️ It must be re-loaded each time you restart Reaper (or set it as a startup action via SWS).
3. Confirm the link: in Claude Code, the **`reaper_ping`** tool should return Reaper's version.

> The plugin can't control anything until `reaper_ping` succeeds — set this up first.

### 2. Install this plugin (the "brain")

In Claude Code:

```bash
/plugin marketplace add t-rzeznik/reaper-composer
/plugin install reaper-composer@reaper-composer
```

That's it — the `/reaper-composer:compose` and `/reaper-composer:discover` commands and all
skills are now available.

**Developing locally instead?** Point Claude Code straight at a clone:

```bash
claude --plugin-dir /path/to/reaper-composer
```

(Use `/reload-plugins` to pick up edits without restarting.)

---

## 🎚️ Usage

With Reaper open and `reaper_ping` working, just describe the song:

```bash
/reaper-composer:compose <genre>, <style / vibe / artist reference>
```

Examples:

```bash
/reaper-composer:compose future bass, uplifting, in the style of Illenium
/reaper-composer:compose tech house, dark and driving, 126 BPM
/reaper-composer:compose metalcore, breakdown-heavy, drop C tuning
/reaper-composer:compose 50s rock and roll, Chuck Berry energy, key of A
/reaper-composer:compose trap, moody melodic, sliding 808s
```

Then: review the plan the arranger proposes → approve or ask for tweaks → watch it build the
song in Reaper. Want a file at the end? Say *"render it to WAV"* — otherwise it leaves the
finished project open for you to play and edit.

**Or start from a vibe, not a genre:**

```bash
/reaper-composer:discover something cinematic and tense that erupts into a heavy drop
/reaper-composer:discover the energy of Daft Punk but moody, like a night drive
/reaper-composer:discover                # no idea yet? just run it and start talking
```

This opens a conversation that shapes your idea into a concrete brief, then offers to build it.

**Polish the mix (optional):**

```bash
/reaper-composer:mix                       # balance the current project
/reaper-composer:mix too boomy, push the lead
```

Analyzes the master (loudness, headroom, tonal balance, stereo) and applies level/EQ/pan/send
fixes. It renders a temp file for analysis only — never an export — and falls back to plain DSP
metrics if the optional AI-listening layer isn't configured.

---

## 🎵 Supported genres & skills

Out of the box: **EDM, house, trap, metal, rock & roll.** Each genre skill encodes real
musicological conventions (subgenre tempo/key tables, drum programming, synth/amp archetypes,
harmony, and the production moves that define the style).

Skills are loaded automatically based on your request — you don't invoke them by hand; the
agents pull in the matching genre skill and the shared `reaper-mcp-reference` skill as needed.
Anything outside the supported list still works, falling back to general knowledge with the
gap flagged.

### Add your own genre

No code required:

```bash
cp -r skills/genre-template skills/genre-<your-genre>
# edit skills/genre-<your-genre>/SKILL.md: set the name/description frontmatter
# and fill in the tempo table, drums, instruments, harmony, and production moves
```

The agents pick it up automatically.

---

## 🧩 The two-repo system

```
┌─────────────────────┐     orchestrates      ┌──────────────────────┐   MCP / TCP   ┌──────────┐
│   reaper-composer    │ ───── agents + ─────▶ │     reaper-mcp        │ ───────────▶ │  Reaper  │
│   (this repo)        │       skills          │   (companion repo)    │   ~54 tools   │   (DAW)  │
│   musical brain      │ ◀──── tool calls ──── │   DAW control layer   │ ◀─────────── │          │
└─────────────────────┘                       └──────────────────────┘               └──────────┘
```

- **[reaper-composer](https://github.com/t-rzeznik/reaper-composer)** (this repo) — the agents,
  skills, and orchestration. Decides *what* to play.
- **[reaper-mcp](https://github.com/t-rzeznik/reaper-mcp)** — the MCP server + in-Reaper bridge.
  Knows *how* to make Reaper do it.

---

## ⚙️ Design constraints (and why they're interesting)

The plugin's behavior is shaped by what the reaper-mcp tool surface actually supports — the
agents are written to work *with* these, not pretend they don't exist:

- **MIDI-only** — songs are built from instrument plugins; there's no audio/sample import.
- **Time is in seconds** — the composer converts bars/beats using the project tempo itself
  (the `music-theory` skill carries the exact formulas and note/chord tables).
- **FX are parameter-controlled** — no screenshot/vision; parameters are set by name/index,
  discovered at runtime.
- **Plugins must be installed** — agents match the plan to whatever `reaper_list_installed_fx`
  reports and substitute the closest available, reporting any swaps.
- **Notes are written in batches** — a whole part goes in via one `reaper_add_midi_notes` call
  (a companion change to reaper-mcp), not one note at a time.
- **Mixing has "ears"** — the analyze tools render the master and measure it (and can call an
  AI listener), which is how the mix engineer reasons about a result it can't literally hear.

---

## 📂 Repo layout

```
.claude-plugin/
  plugin.json            plugin manifest
  marketplace.json       makes the repo installable via /plugin
commands/
  compose.md             /reaper-composer:compose — genre + style → song
  discover.md            /reaper-composer:discover — brainstorm a vibe → song
  mix.md                 /reaper-composer:mix — opt-in mix/balance pass
agents/                  arranger · vst-setup · composer · mix-engineer
skills/
  vision-discovery/      conversational discovery for fuzzy / hybrid ideas
  music-theory/          MIDI notes, scales, chords, timing/swing, drum map
  mixing/                reading the analyze tools → mix fixes
  reaper-mcp-reference/  the reaper-mcp tool contract + conventions
  genre-template/        scaffold for new genres
  genre-edm · genre-house · genre-trap · genre-metal · genre-rock-and-roll
```

---

*Built with [Claude Code](https://claude.com/claude-code). Pairs with
[reaper-mcp](https://github.com/t-rzeznik/reaper-mcp).*
