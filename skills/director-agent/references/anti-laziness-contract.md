# Anti-Laziness Contract

This file exists because director work fails when the agent substitutes confident summary for actual coverage.

## Contents

- Definition Of Lazy Failure
- Mandatory Coverage Ledger
- Unit Completion Standard
- Continuation Rules
- Anti-Generic Language Filter
- Final Self-Check

## Definition Of Lazy Failure

Lazy failure includes:

- Giving general principles instead of applying them to the user's material.
- Covering only the beginning of a long script and implying the whole script was handled.
- Compressing every scene into one-line advice without scene function, character pressure, and visual logic.
- Saying "make it more cinematic" without camera, space, sound, action, or edit decisions.
- Inventing facts to avoid research or assumption labeling.
- Dropping dialogue, scenes, characters, constraints, or continuity.
- Treating adjacent scenes as causal merely because one follows the other.
- Letting characters use knowledge they never obtained or reset relationships after a scene change.
- Keeping dialogue that does not respond to a prior stimulus or alter the listener's next move.
- Calling a repeated prop, symbol, or late convenience a payoff without a changed function or result.
- Ending without a continuation anchor when the task is incomplete.

## Mandatory Coverage Ledger

For large tasks, create a ledger:

```text
Coverage ledger:
- Total units: <N>
- Covered now: <unit ids>
- Not yet covered: <unit ids>
- Continuation anchor: ▶ CONTINUE FROM: <next unit>
```

Units may be acts, scenes, sequences, paragraphs, source segments, or user-provided numbered sections. Pick the smallest unit that prevents silent skipping.

## Unit Completion Standard

Every unit must identify:

- Source material covered.
- Scene/story function.
- Character objective and obstacle.
- Pressure or conflict movement.
- Assumptions and unresolved facts.

For script creation, revision, diagnosis, or dialogue work, require:

- A plain-language retell of who wants what, why now, what they do, what it causes, what final choice occurs, and what it costs.
- Actual reading of the routed A3 knowledge cards; a path, summary, or state ledger does not count as knowledge use.
- An obvious-alternative test for every central action: why does the character not use the safer, cheaper, easier, or more direct option?
- Direct cause inherited from the previous unit.
- Entrance facts, knowledge, relationships, power, and physical conditions.
- Character stimulus, tactic, and tactic-shift trigger.
- Consequential exit state and direct trigger for the next unit.
- Dialogue response chain for every consequential exchange.
- Character-specific dialogue purpose and voice; do not equate clear dialogue with complete, symmetrical answers.
- Setup/payoff lifecycle for any climax mechanism, reveal, or recurring object.

If the plain story, character action, obvious-alternative, or dialogue-purpose checks fail, return to `screenplay-writing-core.md` and the routed A3 card. Use `screenplay-state-engine.md` only for a continuity, knowledge, causality, or setup/payoff failure. Do not compensate with visual polish or explanation.

For director analysis or pre-storyboard work, require:

- Audience endpoint.
- Visual concept or image strategy.
- Performance action verb.
- Sound/time/edit decision.

For storyboard-prep, also include:

- Motif or physical carrier.
- Spatial power geometry.
- Anti-default choice.
- Handoff constraints for `ai-storyboard-director`.

## Continuation Rules

When incomplete:

- Stop only after finishing the current unit.
- Emit exactly one visible continuation anchor:
  `▶ CONTINUE FROM: <unit-id> <short label>`.
- Preserve all numbering, labels, assumptions, motifs, and character names.
- Start the next answer by reading the anchor and continuing, not restarting.

## Anti-Generic Language Filter

These phrases are banned unless immediately converted to concrete execution:

- cinematic
- more tension
- stronger conflict
- richer emotion
- director thinking
- visual impact
- advanced lens language
- more artistic
- deeper theme

Conversion examples:

- "more tension" -> "delay the reveal for two beats; keep the object off-screen; let the sound arrive before the image."
- "stronger conflict" -> "force C1 to choose between protecting C2 and exposing the lie."
- "cinematic" -> "hold a 7s locked medium shot while C1 fails to answer; cut only when C2 looks at the unopened door."

## Final Self-Check

Before responding, ask:

1. Did I handle the user's actual material, not just the category?
2. Did I mark assumptions?
3. Did every recommendation produce an action, image, sound, edit, or structural change?
4. Did I avoid unsupported film-history claims?
5. If incomplete, did I provide a ledger and continuation anchor?
6. Can a cold reader reconstruct why every covered scene follows from the previous state?
7. Can a cold reader identify what every consequential line is responding to?
8. Did any climax solution, reveal, or character turn appear only when the author needed it?
9. Can a normal reader retell the story without seeing internal ledgers?
10. Did any central action happen only because the character ignored an obvious available alternative?
11. With speaker labels hidden, do the important characters still sound and behave differently?
12. Did I test ordinary social routes such as asking, calling, negotiating, delaying, cancelling, reporting, or accepting a smaller loss instead of assuming they do not exist?
13. Can every consequential supporting character be replaced by a rule, timer, or conscience speech without changing the story? If yes, the character is not finished.
