---
name: vision-discovery
description: Conversational discovery for when the user has a musical vision but can't name a single genre — vague/emotional descriptions ("dreamy but aggressive"), cross-genre or hybrid ideas, references that span styles, or "I'm not sure what genre this is, grill me / help me figure it out". Drives a collaborative back-and-forth until the vision is concrete enough to arrange, then produces a creative brief and maps it to one or more genre skills. Use BEFORE the arranger whenever the genre/style isn't already clear.
---

# Vision discovery

Use this when the user knows the *feeling* they want but not the *label*. Your job is to
converse with them — back and forth, as many turns as it takes — until you can describe their
song concretely, then hand a clear creative brief to the `arranger`.

This is **collaboration, not interrogation**. You are helping them discover and articulate
what they already feel. Reflect, suggest, and translate — don't fire a questionnaire.

## How to run the conversation

1. **Start from whatever they gave you** — a mood, a movie scene, a color, an artist, a
   half-formed idea. Acknowledge it and reflect back what you heard in musical terms.
2. **Ask one or two focused questions at a time**, then listen. Never dump a list of ten
   questions. Each answer should sharpen your mental model and inform the next question.
3. **Translate vague language into musical parameters.** "Dreamy" → pads, reverb, slower
   tempo, major 7ths. "Gritty" → distortion, lower tuning, aggressive drums. "Nostalgic" →
   era/production aesthetic. Say your interpretation out loud so they can correct it.
4. **Offer concrete A/B choices** to triangulate fast: "More four-on-the-floor and danceable,
   or half-time and heavy?", "Warm and analog, or bright and digital?", "Vocal-led or
   instrumental?". Choosing is easier than describing.
5. **Use reference anchors.** Ask for 1–3 songs/artists that feel close — even "the energy of
   X but the mood of Y". References collapse ambiguity instantly. If they can't name any,
   propose some and let them react.
6. **Reflect back periodically.** Summarize the emerging picture in a sentence or two and ask
   "is this the direction?" Adjust until they say yes.

## What you need to pin down (the target)

Keep going until you can confidently state all of these:

- **Mood / emotional arc** — and how it should change across the song (build? release? steady?)
- **Energy level** and **tempo feel** (fast/driving vs. slow/heavy vs. mid/groovy)
- **Era / production aesthetic** (vintage, modern, lo-fi, polished, cinematic…)
- **Instrumentation must-haves** (the sounds they specifically want — and any hard NOs)
- **Vocal or instrumental** (this plugin writes instrumental/MIDI, but vocal-style phrasing
  and arrangement differ — know which they imagine)
- **Structure shape** (looping/hypnotic, verse-chorus, big-build-and-drop, through-composed)
- **2–3 reference anchors**

## Mapping the vision to genre skills

Once the picture is clear, route it to the genre layer:

- **Closest single genre** → load that genre skill (e.g. `genre-house`) and proceed.
- **Hybrid** → load **two** genre skills and tell the arranger how to blend them, concretely:
  which element comes from where (e.g. "trap-style 808s + half-time drums from `genre-trap`,
  but the euphoric supersaw drop and chord work from `genre-edm`"). Name the donor genre for
  each major element.
- **No good fit** → build the brief from first principles using the dimensions above, and tell
  the arranger no genre skill applies so it works from the brief directly (flag the gap).

Lean on the genre skills' tempo/structure tables as a vocabulary to triangulate against, even
mid-conversation ("that energy at ~150 BPM half-time lands in trap territory — sound right?").

## Convergence test (when you're done)

You're done when you can play back, and the user confirms: *tempo range, mood/key direction,
structure shape, the key instrumentation roles, and 2–3 reference anchors.* If you can't state
all of those, keep talking. Don't rush to the arranger with a fuzzy picture — the whole point
of this skill is to remove the fuzz.

## Output → hand off to the arranger

Produce a short **creative brief**:

- one-line concept
- mood/energy + emotional arc
- tempo feel + rough BPM
- production aesthetic / era
- instrumentation must-haves and hard NOs
- structure shape
- reference anchors
- **genre routing**: which genre skill(s) the arranger should load, and — if hybrid — which
  elements come from which genre

Then invoke the `arranger` with this brief in place of a raw "genre + style". The arranger
turns it into the full section-by-section plan for your approval.
