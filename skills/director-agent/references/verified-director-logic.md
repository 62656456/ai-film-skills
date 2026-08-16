# Verified Director Logic

Use this file as the source-backed reasoning base for `director-agent`. It is not a quote bank. It turns verified film-directing theory into executable decisions.

## Contents

- Source Discipline
- The Seven Logic Pillars
- Boundary With Screenplay Causality
- Director Reasoning Algorithm
- Anti-Default Director Test
- Source Map

## Source Discipline

- Do not invent director methods, film-history claims, book claims, or examples.
- Treat named directors as decision models only when the source supports the principle or when the principle is framed as an inference from observed work.
- Separate three levels:
  - **Verified**: backed by a cited book, interview, publisher page, official source, film-school guide, or reputable institution.
  - **Inferred**: distilled from multiple observed works or critical analysis; label as inference if used.
  - **Assumed**: supplied because the user's material lacks detail; mark `ASSUMED`.
- If a factual claim affects the plan and cannot be verified, mark `待查证` and avoid using it as a load-bearing rule.

## The Seven Logic Pillars

### 1. Director's Idea: One Concept Governs Many Choices

Ken Dancyger's *The Director's Idea* frames directing around a clear interpretive concept that shapes approach to text, actors, and camera. Use this as the Agent's top-level compression rule: every major choice must serve the director's idea.

Decision questions:

- What is the one interpretive idea that makes this material more specific?
- Does it guide text interpretation, performance, and camera at the same time?
- If two choices both "look good", which one better expresses the director's idea?

Failure modes:

- Good-looking coverage with no governing idea.
- A theme sentence that does not change blocking, performance, sound, camera, or editing.
- Multiple cool devices that do not belong to the same concept.

Operational rule:

```text
Director's idea -> audience endpoint -> performance objective -> spatial design -> camera/edit/sound decisions
```

### 2. Film Form: Meaning Comes From Organized Techniques

Use the formal technique categories common to Bordwell/Thompson-style film analysis: mise-en-scene, cinematography, editing, and sound. A director decision is strong only when it changes one or more of these formal layers in a purposeful way.

Decision questions:

- Mise-en-scene: what is placed in the frame, where, under what light, and with what actor movement?
- Cinematography: where is the camera, what is the frame size/angle/focal relation/movement?
- Editing: why does the cut happen here and not later?
- Sound: what does the audience hear that the image cannot or should not show?

Failure modes:

- "Cinematic" as a mood word with no formal technique.
- Camera choices that do not change audience information, emotion, space, or power.
- Sound used only as decoration.

### 3. Performance Logic: Give Actors Playable Actions

Judith Weston-style performance direction rejects result-only instructions. Actors need playable objectives and transitive action verbs rather than abstract emotion labels.

Decision questions:

- What does the character want from the other person right now?
- What action verb is playable: threaten, seduce, corner, soothe, test, expose, avoid, protect?
- Where does the strategy change?
- What should the listener reveal without speaking?

Failure modes:

- "Act sad / angry / nervous" without objective.
- Dialogue treated as information only, not as an action.
- Ignoring the listener.

Operational rule:

```text
emotion label -> playable objective -> action verb -> body behavior -> camera target
```

### 4. Editing Logic: A Cut Must Earn Its Existence

Walter Murch's Rule of Six ranks cut criteria with emotion first, then story, rhythm, eye-trace, two-dimensional screen plane, and three-dimensional space. Use this as the cut-ranking rule.

Decision questions:

- Does the cut preserve or sharpen the emotional truth of the moment?
- Does it advance story or reveal new information?
- Is the timing rhythmically right?
- Does the viewer's eye know where to go after the cut?
- Does the cut maintain enough screen and spatial clarity?

Failure modes:

- Cutting because a line ended rather than because audience perception changed.
- Protecting continuity while killing emotion.
- Fast cutting without eye-trace or story gain.

Operational rule:

```text
cut only for emotion / story / rhythm / eye-trace / screen plane / spatial clarity
if forced to sacrifice, protect emotion first
```

### 5. Sound Logic: Listening Has Different Jobs

Michel Chion's three listening modes give sound decisions a structure:

- Causal listening: sound identifies a source.
- Semantic listening: sound carries language or code.
- Reduced listening: sound is heard for its own texture and quality.

Decision questions:

- Should the audience identify the source, understand speech/code, or feel the texture?
- Should sound confirm the image, contradict it, precede it, or continue after it?
- Would silence do more work than music or effects?

Failure modes:

- Music tells the audience what to feel because the image has not earned it.
- Every sound is literal and on-screen.
- Dialogue is clear but the sound world has no dramatic idea.

### 6. Information Logic: Suspense Is Audience Knowledge Designed Over Time

Hitchcock's suspense/surprise distinction is useful as a practical information rule: audience knowledge, character knowledge, and timing determine whether a scene creates suspense, mystery, or shock.

Decision questions:

- What does the audience know that the character does not?
- What does the character know that the audience does not?
- When should the audience discover the danger, secret, or cost?
- Which object, space, or sound carries the hidden information?

Failure modes:

- Hiding everything and calling it suspense.
- Revealing a twist without preparing audience attention.
- Cutting to danger once, then forgetting to remind the audience.

Operational rule:

```text
audience knows first -> suspense
character knows first -> mystery
everyone learns together -> surprise/shock
```

### 7. Physicalization Logic: Inner States Need External Carriers

Strong directors turn psychology into visible and audible pressure: space, weather, light, objects, costume state, blocking, rhythm, and silence. Kurosawa's widely discussed use of weather is a useful model for physicalizing mood and conflict, but use it as a device only when it changes action or perception.

Decision questions:

- What external element carries the inner pressure?
- Is the element active in story space, not just a filter?
- Does it change blocking, sound, visibility, or risk?
- Can the same motif establish, vary, and pay off?

Failure modes:

- Rain, fog, neon, or slow motion as decoration.
- Psychological exposition that never becomes behavior.
- Symbolic objects that do not affect choices.

## Boundary With Screenplay Causality

For script creation, revision, diagnosis, scene repair, or dialogue work, pass `screenplay-state-engine.md` before applying this director-form layer. This file cannot prove scene-to-scene causality, character knowledge continuity, or dialogue response. Do not use visual concept, performance language, sound, or editing to hide a broken screenplay chain.

## Director Reasoning Algorithm

Use this sequence for substantial tasks:

```text
1. Material type and missing facts
2. Event chain and turn points
3. Character goals, obstacles, strategy changes
4. Audience endpoint and emotion curve
5. Director's idea
6. Dominant logic pillar(s)
7. Performance actions
8. Mise-en-scene and spatial power
9. Camera and focal strategy
10. Sound and listening mode
11. Time and edit rules
12. Theme/subtext as action
13. Anti-default choice
14. Verification and assumption check
```

## Anti-Default Director Test

Reject the plan if it can be reduced to:

- Establishing wide shot.
- Standard over-shoulder dialogue.
- Reaction close-up.
- Emotional music swell.
- Pretty final image.

Replace default coverage with a concept-driven plan:

- The scene's power geometry.
- A playable action for each actor.
- A sound relation.
- A cut logic.
- A motif or physical carrier.
- One deliberate withheld element.

## Source Map

- Ken Dancyger, *The Director's Idea*: director's idea as a concept shaping text, performance, and camera.
  - Google Books: https://books.google.com/books/about/The_Director_s_Idea.html?id=O0uF0_zwnsIC
  - O'Reilly preview: https://www.oreilly.com/library/view/the-directors-idea/9780240806815/32_chapter-title-23.html
- David Bordwell / Kristin Thompson, *Film Art: An Introduction*: film technique categories including mise-en-scene, cinematography, editing, and sound.
  - Bordwell blog: https://www.davidbordwell.net/blog/2012/03/16/film-art-an-introduction-reaches-a-milestone-with-help-from-the-criterion-collection/
  - Internet Archive catalog: https://archive.org/details/filmartintroduct0000bord
- Judith Weston, *Directing Actors*: process-oriented actor direction, relationship, listening, action rather than result.
  - Weston official archive: https://judithweston.com/web/archive/top-10-ideas-directing-actors
  - Raindance summary of actor action verbs: https://raindance.org/directing-tools-the-actors-language/
- Walter Murch, *In the Blink of an Eye*: Rule of Six for cuts.
  - StudioBinder summary: https://www.studiobinder.com/blog/walter-murch-rule-of-six/
  - Berkeley course blog summary: https://blogs.ischool.berkeley.edu/i290-viznarr-s12/the-rule-of-six-walter-murch/
- Michel Chion, *Audio-Vision*: causal, semantic, and reduced listening.
  - De Gruyter page: https://www.degruyterbrill.com/document/doi/10.7312/chio18588-004/html
  - PDF excerpt: https://people.wku.edu/joon.sung/edu/anim/anim330/reading/three_modes_of_listening.pdf
- Alfred Hitchcock / François Truffaut interviews: suspense as information design.
  - Interview history/context: https://www.newwavefilm.com/interviews/hitchcock-truffaut.shtml
  - Suspense/surprise explainer: https://nofilmschool.com/alfred-hitchcock-and-francois-truffaut-explain-surprise-vs-suspense
- Akira Kurosawa weather and movement as physicalized emotion/action.
  - BFI feature: https://www.bfi.org.uk/features/how-akira-kurosawa-films-command-weather
