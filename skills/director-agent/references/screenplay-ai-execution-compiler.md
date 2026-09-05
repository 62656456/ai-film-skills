# AI-Executable Screenplay Compiler

Use this reference only when the user explicitly needs an AI-video/AI-comic executable screenplay, prompt-ready action text, or repair of model-confusing subjects, actions, reactions, space, or props. It is a post-writing compiler. It does not define dramatic quality and must not replace `screenplay-writing-core.md` or `screenplay-state-engine.md`.

## 1. Preserve Two Layers

Keep two distinct artifacts or clearly separated sections:

1. **Readable screenplay master**: story causality, character objectives, relationship pressure, choices, costs, action, and natural dialogue for human reading.
2. **AI execution layer**: only the requested scenes or beats, rewritten at the granularity required to bind visible subjects, states, triggers, actions, reactions, space, props, and exit states.

The semantic facts must match. Different granularity is allowed; a changed event, motive, relationship, dialogue meaning, or result is not.

Do not claim that a script is dramatically strong merely because a model can execute it. Conversely, do not contaminate every readable screenplay with repeated names, exhaustive movement, or model-facing syntax.

## 2. Entry Gate

Run this compiler only when at least one is true:

- The user explicitly requests an AI-executable, AI-video, AI-comic, or generation-ready screenplay.
- A model has confused who acts, who speaks, who reacts, where an action happens, or who holds a prop.
- The user requests action text that can be compiled into image/video prompts or production storyboards.

Do not run it merely because AI may be used later. A pure screenplay request receives the readable screenplay first.

Before compilation, the story must already pass:

- current objective, obstacle, choice, and cost;
- causal and knowledge-state continuity;
- obvious-alternative test;
- dialogue purpose and natural-response pass;
- scene entry/exit state and payoff checks.

More execution detail cannot repair a weak premise, missing cause, false dilemma, or author-convenient character action.

## 3. Compile Visible State Changes

For each required beat, build this chain:

```text
explicit subject
+ visible current state
+ trigger or newly perceived stimulus
+ action start and direction
+ necessary process or interaction
+ observable result
+ consequential reaction or deliberate non-reaction
+ exit state of character / relationship / information / prop / space
```

This is a decision scaffold, not a sentence template. Include only fields needed to prevent a material ambiguity.

### Subject Binding

- In multi-character or dialogue-heavy execution text, repeat natural character names when a pronoun could attach to more than one subject.
- Bind each consequential action, line, look, handoff, and reaction to one explicit subject.
- Pronouns remain allowed when only one plausible subject exists and continuity is already stable.
- Do not use production asset IDs in user-facing prose unless the user explicitly asks for them.

### State Before Action

- Put a physical, emotional, or attentional state before the action it must shape.
- Put the perceived stimulus before the reaction it causes.
- Put the spatial anchor before movement through that space.
- Re-establish state after a meaningful posture, location, possession, injury, or relationship change; do not repeat unchanged labels mechanically.

### Action Path

Write enough start, path, interaction, and result to remove a consequential jump. Do not choreograph every joint or incidental step.

Use detail when it affects:

- identity or action ownership;
- physical possibility and object contact;
- screen direction or continuity;
- story cause and effect;
- a reaction the audience must read;
- the exit state required by the next beat.

Leave harmless variation open when several bodily realizations preserve the same meaning and continuity.

### Reaction Loop

Every important stimulus must receive a readable effect, but not every line needs a decorative nod, blink, or frown.

Valid reactions include:

- a changed action or tactic;
- a look, pause, withdrawal, approach, concealment, interruption, or object use;
- motivated silence, refusal to look, or continuation of an existing task;
- a relationship, information, power, or commitment change.

The reaction must follow from what the character perceived, wanted, feared, or protected. Do not insert generic micro-actions merely to keep the image moving.

### Space And Props

- Prefer observable relative anchors: in front of, three steps behind, at the table edge, through the visible doorway, on the character's right.
- Replace vague `there`, `behind`, `beside`, or `the two of them` when they could describe multiple positions or people.
- Track who holds, releases, transfers, opens, damages, wears, or leaves each consequential prop.
- Use exact distances, angles, and body mechanics only when story, safety, contact, or continuity requires them. Precision without function is noise.

### Dialogue And Punctuation

- Bind each spoken line to the named speaker when multiple speakers are present.
- Establish the immediate speaking condition or tactic when it changes delivery: testing, concealing, stalling, forcing, calming, or withdrawing.
- Use standard punctuation and quotation structure. Do not invent slashes, repeated symbols, or arbitrary marks as universal timing controls.
- Treat punctuation timing as model-dependent. If exact pause duration matters, specify it in the later production or sound layer and verify on the target system.

## 4. Sufficient But Not Overdense

The target is **sufficient but not overdense**: enough information to exclude a wrong subject, state, path, spatial relation, prop state, or result; no extra detail that freezes harmless performance variation or competes with the main action.

Reject both extremes:

- **Result-only shorthand**: `She gets up, crosses the room, drinks.` The causal and physical chain is underbound when intermediate state matters.
- **Joint-by-joint puppetry**: every elbow angle, foot placement, head degree, and breath is fixed without dramatic or continuity need.

Prefer intention-bearing physical behavior over emotional adjectives alone. `He is nervous` is weak; `He keeps the envelope under his palm while asking an unrelated question` joins state, protection, action, and subtext.

## 5. Model-Difficulty Adaptation Gate

Never delete or rewrite a consequential action merely because a model finds it difficult.

For each difficult action, classify its dramatic function:

1. **No consequential function**: it may be compressed, elided, or moved off-screen if entry and exit states remain clear.
2. **Function can survive a different visible action**: substitute only when motive, relationship, information, cost, and result remain equivalent.
3. **Action itself carries evidence, choice, contact, injury, reveal, or payoff**: preserve it. Split the action, change coverage, use an insert or reaction, establish start/end states, or mark the execution unresolved.

Disclose any adaptation that changes visible behavior. Do not silently rewrite story facts for model convenience.

## 6. Per-Scene Compilation Pass

For each requested scene:

1. Freeze the readable master and locked dialogue.
2. Mark the scene entry and exit states.
3. Identify the few visible changes the audience must understand.
4. Bind each change to an explicit subject and trigger.
5. Add only necessary action path, reaction, spatial, and prop information.
6. Remove ambiguous pronouns and vague spatial references.
7. Remove decorative micro-actions and unsupported precision.
8. Run the model-difficulty adaptation gate.
9. Recompare the execution layer with the readable master for semantic conservation.

Compile scene by scene or causal beat by causal beat. Do not ask a model to rewrite a full long screenplay in one uncontrolled pass.

## 7. Completion Gate

Before labeling the AI execution layer internally ready, verify:

- **Story preserved**: no changed event, motive, relationship, dialogue meaning, choice, cost, or result.
- **Subject binding**: each consequential action, line, and reaction has one reconstructable owner.
- **State before action**: required state, stimulus, and spatial anchors precede the behavior they shape.
- **Causal continuity**: no required physical or informational jump is hidden between start and result.
- **Reaction closure**: important stimuli create a readable effect; silence and non-response are intentional when used.
- **Space and props**: positions, entrances, holders, transfers, and exit states are traceable.
- **Sufficient but not overdense**: no ambiguity-causing omission and no purposeless body puppetry.
- **Punctuation**: standard, readable, and not misrepresented as a universal timing guarantee.
- **Adaptation honesty**: model-driven changes preserve dramatic function or are disclosed as unresolved.

Label the result honestly: `AI execution text internally checked` does not mean the target model followed it, the generated video works, or the user accepted the screenplay.
