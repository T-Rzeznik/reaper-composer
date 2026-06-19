# 🎛️ reaper-composer

**Generate complete, playable songs inside [Reaper](https://www.reaper.fm/) from a single plain-English request.**

`reaper-composer` is a [Claude Code](https://claude.com/claude-code) plugin that turns a prompt
like *"future bass, uplifting, in the style of Illenium"* into a fully arranged Reaper
project — tracks created, instruments and effects loaded, MIDI written, and automation drawn —
section by section, with you approving the creative direction along the way.

It drives the DAW through a companion MCP server,
**[reaper-mcp](https://github.com/t-rzeznik/reaper-mcp)**, which exposes ~55 tools for
controlling Reaper. This repo is the "brain" (musical knowledge + orchestration); reaper-mcp
is the "hands" (DAW control). **You need both.**

---

## ✨ What it does

**One command does the whole thing.** Run `/reaper-composer:compose` and it carries you from a
plain-English request to a finished song — brainstorming the idea if it's fuzzy, building the
session, writing the music, and offering a mix at the end. You never pick "skills" or chain
commands; the right knowledge loads itself as each stage needs it.

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

**It remembers, too.** The plugin builds a persistent catalog of *your* installed VSTs (what
each one is and what it's good for) so it picks better instruments over time, and it checkpoints
each song to disk — so after a `/clear` or the next day, re-running `compose` offers to **resume**
the in-progress song right where it left off instead of starting over.

**Don't have a genre in mind?** Still just run `/reaper-composer:compose` — describe the
*feeling* ("something dreamy but with a hard-hitting drop", a movie scene, two artists you want
to blend) and it automatically drops into a back-and-forth that turns the vibe into a concrete
brief before building. (There's also a dedicated `/reaper-composer:discover` if you specifically
want to brainstorm without committing to a build yet — but you don't need it.)

---

## 🏗️ How it's built

You drive **one command**; behind it, focused sub-agents run in a pipeline (three for composing,
plus an opt-in mix engineer), and all the musical knowledge lives in **skills** that load
themselves on demand. You never invoke a skill or chain agents by hand.

**The command you use:**

| Command | Role |
|---|---|
| `/reaper-composer:compose` (`commands/compose.md`) | **The one command.** Orchestrates the whole pipeline — auto-brainstorms fuzzy ideas, builds the session, writes the music, offers a mix at the end. |

**Optional shortcuts** — `compose` already covers all of these; reach for them only if you want
to run a piece on its own:

| Command | When you'd use it directly |
|---|---|
| `/reaper-composer:discover` (`commands/discover.md`) | Brainstorm a vibe into a brief *without* committing to a build yet. |
| `/reaper-composer:mix` (`commands/mix.md`) | Re-run the mix/balance pass on demand. |
| `/reaper-composer:catalog-vsts` (`commands/catalog-vsts.md`) | Eagerly research every installed plugin up front. |

**Under the hood** — agents and skills the plugin runs *for* you (you never call these directly):

| Piece | Role |
|---|---|
| `agents/arranger.md` | Turns intent into an approved song plan (no DAW access) |
| `agents/vst-setup.md` | Builds the Reaper session: tracks, instruments, FX, routing |
| `agents/composer.md` | Writes all MIDI, FX, and automation; auditions the song |
| `agents/mix-engineer.md` | Analyzes the master and balances levels/EQ/pan/sends (opt-in) |
| `skills/vision-discovery/` | Conversational discovery for fuzzy / genre-less / hybrid ideas |
| `skills/music-theory/` | Lookup tables: MIDI notes, scales, chords, timing/swing math, drum map |
| `skills/songwriting/` | Composition craft: voice leading, motif development, tension/release, counter-melody |
| `skills/groove/` | Humanization: velocity shaping, micro-timing, swing/feel so MIDI isn't robotic |
| `skills/mixing/` | How to read the analyze tools and translate metrics into mix fixes |
| `skills/recommended-vsts/` | Catalog of free VSTs by role; suggested when you lack one |
| `skills/vst-catalog/` | Persistent, researched catalog of *your* installed VSTs — drives plugin selection |
| `skills/drum-maps/` | Researches a drum VST's MIDI note layout (online if needed), saves a per-kit map file, verifies it |
| `skills/song-state/` | Checkpoints each song to disk so a later session can resume it |
| `skills/local-assets/` | Use your own folder of samples/MIDI — catalog, place, and trigger them |
| `skills/reaper-mcp-reference/` | The reaper-mcp tool contract + hard-won conventions |
| `skills/genre-*/` | Per-genre musicology (EDM, house, trap, metal, rock & roll) |
| `skills/genre-template/` | Copy-to-create scaffold for new genres |

**Design principle:** agents are general; genres are data. Every genre skill is just Markdown —
tempo/structure tables, drum patterns, synth archetypes, harmony, and signature production moves —
so the system grows by writing knowledge, not code. And because skills load only when a stage
needs them, the long list above costs you nothing — you only ever type `compose`.

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

That's it — `/reaper-composer:compose` is now available (along with the optional shortcut
commands and all the skills it loads automatically).

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

The **same command** handles everything else, too — you don't switch commands:

- **No genre in mind?** Just describe the feeling and it auto-brainstorms a brief first:
  `/reaper-composer:compose something cinematic and tense that erupts into a heavy drop`
- **Bring your own sounds?** Point it at a folder of samples or MIDI and it weaves them in:
  `/reaper-composer:compose trap, dark — use my samples in C:\Users\me\Samples\trap`
  (it catalogs the folder and drops loops/one-shots/`.mid` clips where they fit; ask and it'll
  route drum one-shots into a sampler for MIDI triggering instead)
- **Mix at the end?** When the song's done it *asks* if you want it balanced — just say yes.
- **Plugins?** It researches and remembers your VSTs automatically as songs need them.

### Optional shortcuts

Everything above runs from `compose`. These exist only if you want to trigger one piece on its
own — you never *need* them:

```bash
/reaper-composer:discover the energy of Daft Punk but moody, like a night drive   # brainstorm only, no build yet
/reaper-composer:mix too boomy, push the lead                                      # re-run the mix pass on demand
/reaper-composer:catalog-vsts                                                      # eagerly research every installed plugin up front
```

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
│   (this repo)        │       skills          │   (companion repo)    │   ~55 tools   │   (DAW)  │
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

- **Sounds are created as MIDI** — new parts are MIDI driving instrument plugins (the server
  can't record or synthesize audio). But it **can import your own files** — point it at a folder
  and it drops samples/loops and `.mid` clips in via `reaper_insert_media` (the `local-assets`
  skill).
- **Time is in seconds** — the composer converts bars/beats using the project tempo itself
  (the `music-theory` skill carries the exact formulas and note/chord tables).
- **FX are parameter-controlled** — no screenshot/vision; parameters are set by name/index,
  discovered at runtime.
- **Plugins must be installed** — agents match the plan to whatever `reaper_list_installed_fx`
  reports and substitute the closest available, reporting any swaps. When a role has no good
  fit (e.g. no real drum sampler), `vst-setup` recommends specific **free** VSTs to install
  (via the `recommended-vsts` skill) rather than forcing a wrong instrument onto it.
- **Notes are written in batches** — a whole part goes in via one `reaper_add_midi_notes` call
  (a companion change to reaper-mcp), not one note at a time.
- **Mixing has "ears"** — the analyze tools render the master and measure it (and can call an
  AI listener), which is how the mix engineer reasons about a result it can't literally hear.
- **It has memory** — JSON files persist context across runs: a machine-global **VST catalog**
  (`~/.reaper-composer/vst-catalog.json`, researched incrementally) so plugin picks improve over
  time, per-kit **drum maps** (`~/.reaper-composer/drum-maps/<kit>.json`) so the right samples
  fire instead of guessed General-MIDI notes (researched online once, then reused and
  hand-editable), and a per-project **song state**
  (`<project>/.reaper-composer/song-state.json`, beside the `.rpp`) holding the plan, track map,
  and per-section progress so an in-progress song can be resumed after `/clear` or the next day.
  All are local user data, never committed.

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
  catalog-vsts.md        /reaper-composer:catalog-vsts — eager full scan of installed plugins
agents/                  arranger · vst-setup · composer · mix-engineer
skills/
  vision-discovery/      conversational discovery for fuzzy / hybrid ideas
  music-theory/          MIDI notes, scales, chords, timing/swing, drum map
  songwriting/           composition craft: voice leading, motif development, tension, counter-melody
  groove/                humanization: velocity shaping, micro-timing, swing/feel
  mixing/                reading the analyze tools → mix fixes
  recommended-vsts/      free VSTs by role (drums, bass, synths, guitar, keys, FX)
  vst-catalog/           persistent catalog of your installed VSTs → plugin selection
  drum-maps/             per-kit drum note maps (researched online, saved & reused)
  song-state/            checkpoint a song to disk → resume across sessions
  local-assets/          use a folder of your own samples / MIDI
  reaper-mcp-reference/  the reaper-mcp tool contract + conventions
  genre-template/        scaffold for new genres
  genre-edm · genre-house · genre-trap · genre-metal · genre-rock-and-roll
```

---

*Built with [Claude Code](https://claude.com/claude-code). Pairs with
[reaper-mcp](https://github.com/t-rzeznik/reaper-mcp).*
