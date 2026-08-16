# Screenplay State And Causality Engine

Use this engine after the primary A3-based writing pass in `screenplay-writing-core.md`. It verifies continuity, causality, knowledge, strategy, and setup/payoff. It must not generate the premise by assembling ledgers, props, or checkpoints.

This is an audit contract, not a form that must be shown to the user. Keep the ledgers internal; deliver the script, rewrite, or diagnosis the user requested. Show a ledger only when it helps the user judge a disputed continuity decision.

## Contents

- Evidence Status And Honesty
- Mandatory Order
- Freeze The Single Source Of Truth
- Prove The Story Engine
- Build The Causal Spine
- Run Character State Machines
- Build Scene State Cards
- Prove The Silent Action Spine
- Build Dialogue Response Chains
- Track Information, Props, And Motifs
- Run The Independent Cold-Read Gate
- Mode-Specific Execution
- Completion And Status

## Evidence Status And Honesty

These rules are operational constraints distilled from cross-work screenplay reading and single-variable counterfactual tests. Treat them as strong working rules, not universal laws.

- Structural validation proves only that the Skill can load.
- An internal forward test proves only that one sample passed.
- Do not call the engine stable until different real tasks pass and the user accepts them.
- Do not preserve a rule merely because it is written here; revise it when a real failure falsifies it.

## Mandatory Order

Enter this engine only after the story can be retold in plain language and the character-action logic has passed the obvious-alternative test in `screenplay-writing-core.md`. Then audit in this order:

```text
plain-language story and A3 behavior/dialogue pass already complete
-> single source of truth
-> causal spine
-> character state machines
-> scene state cards
-> silent action spine
-> dialogue response chains
-> setup/payoff and knowledge audit
-> revised screenplay prose
-> independent cold-read audit
```

Do not start with polished dialogue, visual style, theme speeches, or shot design. If a downstream layer fails, return to the earliest broken upstream layer instead of adding exposition or decorative detail.

## 1. Freeze The Single Source Of Truth

Record only facts supported by the user's material or explicitly marked `ASSUMED`:

- World rules and physical constraints.
- Time, place, geography, travel, access, and available resources.
- Character identities, relationships, commitments, injuries, possessions, and prior actions.
- What each character knows, believes, suspects, hides, or misunderstands.
- User-locked events, exclusions, tone, format, duration, and ending conditions.

Hard gate:

- A fact may not change merely to enable a scene.
- A character may not use information they have not obtained.
- A missing fact must stay unknown or be labeled `ASSUMED`; do not silently complete it.
- A later reveal must be compatible with every earlier observable fact.
- Any consequential off-screen change must have a cause, actor or mechanism, time window, and textual evidence; otherwise keep the prior state.

## 2. Prove The Story Engine

Confirm the already designed story in this compact form:

```text
protagonist's concrete want
+ why action is required now
+ active opposition or constraint
+ cost of delay/failure/success
+ current strategy
+ irreversible choice the pressure is moving toward
```

Also define:

- The dramatic question the audience is following.
- The value or relationship the protagonist cannot preserve together with the want.
- The protagonist's default strategy or false solution.
- How that strategy first works, then creates a larger cost, then becomes unusable.

Hard gates:

- If the protagonist can do nothing and the main events still occur, return to the plain-language story before outlining.
- If the character ignores an available safer, cheaper, easier, or more direct action that would solve the problem, the story fails unless the text establishes why that option is unavailable, rejected, misunderstood, or more costly.

## 3. Build The Causal Spine

Represent every major beat as:

```text
prior condition
-> character action or deliberate refusal
-> immediate result
-> state change
-> newly forced, enabled, or blocked next action
```

Use coincidence only to create a problem, never to conveniently solve the central problem.

Every apparent success must update future conditions. It does not have to create disaster, but it must enable, force, block, price, or reframe a later option. A success that leaves all later choices unchanged is decorative rather than causal.

For each transition, ask:

1. Whose action made this possible or necessary?
2. What new fact, loss, deadline, obligation, or physical condition changed the option set?
3. Why does the next event happen now?
4. What would become impossible or unmotivated if the previous beat were deleted?

Hard gate: if two beats connect only through `and then`, time passage, a phone call, a sudden arrival, or author convenience, the chain fails. Add a real causal condition or remove the beat.

Counterfactual deletion test: remove one beat while holding everything else constant. If all later choices remain equally plausible, that beat is not carrying story causality.

## 4. Run Character State Machines

For every active character in a scene, track:

| Field | Required question |
|---|---|
| Current goal | What do they want from this moment or person? |
| Knowledge/belief | What do they know, suspect, or falsely believe now? |
| Perceived threat/opportunity | What meaning do they assign to the newest stimulus? |
| Relationship/power | What can they grant, withhold, expose, or destroy? |
| Current tactic | What are they doing to get the response they want? |
| Tactic-shift trigger | What new evidence, failure, cost, or deadline makes them change approach? |
| Boundary | What will they not yet do, and what could force them across it? |

Character voice follows from what a person notices, how they interpret it, what they protect, and how they attack or defend. Vocabulary, catchphrases, and sentence length are secondary.

Hard gates:

- No strategy change without a new stimulus, failed tactic, changed cost, or changed option set.
- No sudden stupidity, cruelty, courage, confession, or competence merely because the plot needs it.
- A wound, flaw, or backstory detail is valid only if it causes an observable decision under pressure.
- Do not defend an implausible action by labeling it a flaw after the fact. The text must establish the fear, belief, protection behavior, or constraint that makes the action credible in the moment.

## 5. Build Scene State Cards

For every scene, create this compact internal card:

```text
Scene ID / time / place
Entry state: facts, knowledge, relationships, power, physical conditions, locations/holders of causal props
Immediate objective:
Obstacle/opposition:
Initial tactic:
New stimulus or pressure:
Tactic shift:
Turn:
Irreversible result:
Exit state:
Direct trigger for the next scene:
Audience knows / character knows / withheld:
```

At least one consequential state must change: goal, knowledge, belief, relationship, power, commitment, physical condition, resource, option, deadline, or cost.

Hard gates:

- The next scene must inherit the previous exit state. Do not reset characters to a convenient default.
- If the scene can be deleted without changing any later decision, merge it, rebuild it, or remove it.
- Enter late and leave after the consequential change, not after every topic has been discussed.
- A scene may end unresolved, but it may not end unchanged.

## 6. Prove The Silent Action Spine

Before polishing dialogue, summarize the scene through actions, refusals, objects, spatial changes, discoveries, and consequences.

This does not mean every scene should be silent. Negotiation, interrogation, seduction, testimony, and confession may use speech as the principal action. The test is whether the scene still has an action-and-state spine without explanatory dialogue.

Hard gate: if dialogue is carrying facts, motives, emotions, and theme that produce no immediate choice or reaction, repair the scene action before rewriting the lines.

## 7. Build Dialogue Response Chains

Treat dialogue as action, not alternating statements. For every consequential line or dialogue beat, identify:

```text
stimulus: words / action / silence / object / environmental change
-> perceived meaning, threat, or opportunity
-> speaker objective: what they want the other person to do, believe, reveal, or stop
-> tactic: ask / test / soothe / redefine / evade / shame / threaten / bargain / stall / expose / withdraw
-> listener reaction or counter-tactic
-> state delta: information / power / relationship / commitment / next action
```

A character may evade the literal question only when the evasion is a motivated tactic. The other character must be able to notice, exploit, reject, or be affected by that evasion.

Hard gates:

- Every consequential line must answer a prior stimulus, including a meaningful silence or action.
- A line that has no trigger, objective, tactic, or effect is deleted unless it is essential rhythm with a clear listener effect.
- Two consecutive uses of the same tactic with no changed response require escalation, retreat, reframing, or deletion.
- Exposition is allowed only when it changes the listener's decision, leverage, or interpretation in the current scene.
- Do not give every character the same wit, abstraction level, metaphor density, or explanatory clarity.

Escalation should normally move through earned layers:

```text
specific fact
-> dispute over meaning
-> threat to relationship, status, or identity
-> costly statement or action that cannot be taken back
```

Do not jump directly from a minor disagreement to total humiliation, violence, confession, or thematic declaration without pressure and prior history capable of carrying the jump.

## 8. Track Information, Props, And Motifs

Use a lifecycle ledger:

| Element | Establish | Function/meaning changes | Payoff | Choice or result changed |
|---|---|---|---|---|

An effective payoff does more than repeat an element. It changes function, meaning, power, or physical possibility.

Hard gates:

- A climax solution may not depend on a capability, object, rule, or fact introduced only when needed.
- For every sensory clue, track the physical source, path to the perceiver, and location at the moment it is noticed. A later inference may not silently relocate a sound, image, signal, smell, or object.
- For every powered, damaged, opened, or disassembled device, preserve its power and assembly state. It may not produce a later display, sound, transmission, or action unless reconnection or an alternate source is established on the page.
- For digital material, show or establish the source device, transfer/import action, destination, and resulting file or output. Playing a recording near another device does not silently move the data.
- A twist must explain or reclassify earlier evidence, change current power, and constrain later choices.
- A symbol that never affects action remains decoration; do not treat it as causal proof.
- A repeated object is not a payoff unless its later use changes a choice or result.

## 9. Run The Independent Cold-Read Gate

Use `screenplay-cold-read-protocol.md` with a fresh reader. Give that reader only the raw screenplay, the user's locked constraints, and necessary format information. Do not give them this engine's ledgers, intended meaning, suspected bugs, or expected answer.

The writing agent's own review is `SELF-AUDIT ONLY`; it cannot be labeled independent evidence. Route every cold-read failure to the earliest broken layer, rewrite there, and submit a clean text for a new read.

## 10. Mode-Specific Execution

### Script Creation

1. Confirm that `screenplay-writing-core.md` and its routed A3 cards were actually read and applied.
2. Audit facts and assumptions.
3. Audit the causal spine through the requested scope.
4. Audit character knowledge, options, behavior, and scene exit states.
5. Audit consequential dialogue response chains without forcing literal, over-complete replies.
6. Audit setup/payoff and ending conditions.
7. Revise the requested screenplay text at the earliest broken layer.
8. Run a cold-read audit before delivery.

Do not expose all internal ledgers unless the user asks. Lead with the usable script or requested creative artifact.

### Script Diagnosis

1. Identify the earliest upstream break, not the largest number of symptoms.
2. Cite the exact scene, transition, action, or line where continuity becomes unreconstructable.
3. Explain the missing cause or state inheritance.
4. Repair the upstream layer.
5. Provide directly replaceable text when the user asked for revision.
6. Recheck downstream scenes affected by the repair.

Do not line-polish dialogue while its scene objective, causal trigger, or character knowledge is broken.

### Dialogue Repair

1. Freeze what each character knows and wants.
2. Map the existing stimulus-response chain.
3. Mark random topic changes, repeated tactics, author exposition, and voice convergence.
4. Repair the scene action or strategy ladder first.
5. Rewrite only after the dramatic chain is stable.

## Completion And Status

Before claiming internal completion, verify:

- Every scene has a traceable prior trigger and consequential exit state.
- Every later scene inherits changed facts, knowledge, relationships, and physical conditions.
- Every strategy shift has a new stimulus or failed tactic.
- Every consequential dialogue beat has a response chain.
- Every climax mechanism was established earlier and requires protagonist action.
- A cold reader can reconstruct the chain without author explanation.
- Assumptions and unresolved facts remain visible.

Label validation honestly:

- `structure valid`: files and frontmatter load.
- `internal forward test passed`: one isolated task produced a reconstructable result.
- `delivered for user review`: the user can judge the actual script.
- `user accepted`: only after explicit acceptance.
- `stable in practice`: only after repeated different real tasks are accepted.
