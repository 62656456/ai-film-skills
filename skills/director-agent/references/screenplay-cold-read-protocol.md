# Screenplay Cold-Read Protocol

Use this protocol to audit a screenplay, scene, or dialogue passage independently from the writer's intentions. It tests whether the story can be retold clearly, the actions are believable given available alternatives, the characters and dialogue feel distinct, and the causality, state, and payoff are reconstructable from the text itself.

This protocol does not write or revise the screenplay. Return failures to the writer at the earliest broken layer.

## Contents

- Independence Contract
- Audit Tasks
- Failure Levels
- Required Output
- Return Layers
- Pass Standard

## Independence Contract

Give the cold reader only:

- The raw screenplay or requested source range.
- The user's locked facts and explicit constraints.
- Necessary format, duration, and genre information.

Do not give the cold reader:

- The writer's causal spine or scene-state ledgers.
- Intended theme, subtext, emotional explanation, or character rationale.
- The writer's suspected bugs, proposed repair, or expected answer.
- A summary that resolves gaps not resolved by the screenplay.

Evidence labels:

- `INDEPENDENT COLD READ`: a fresh reader without the writer's rationale performed the audit.
- `PARTIAL ISOLATION`: the reader had some prior project context; disclose the contamination risk.
- `SELF-AUDIT ONLY`: the writer reviewed their own text; never present this as independent proof.

## Audit Tasks

### 0. Retell The Story Plainly

Before using tables, retell the covered story in ordinary language:

```text
who wants what
-> why they act now
-> what they do
-> what blocks or changes them
-> what they do next
-> what final choice/result occurs
-> what it costs
```

If this cannot be done without the writer's explanation, mark the earliest unclear link. A list of props, scene functions, or themes is not a story retell.

Audit the opening separately. After only the first 30--60 seconds or first 200--300 Chinese characters, state the current place, whose immediate problem is being followed, what they are trying to do now, and the first resistance. If several unexplained names, roles, props, or rules arrive before those answers are available, flag the earliest overload. An unexplained mystery is allowed; an unreadable basic situation is not.

### 1. Reconstruct The Observable Story

Without guessing author intent, write the event chain supported by the text:

```text
prior condition
-> character action or refusal
-> immediate result
-> state change
-> next action made necessary, possible, or impossible
```

Mark any transition that requires `probably`, `perhaps`, missing off-screen action, or an unstated new fact.

### 2. Reconstruct Scene State

For every covered scene, infer only from the text:

- Entry facts and physical conditions.
- What each active character knows, believes, suspects, or hides.
- Relationship and power state.
- Immediate objective and obstacle.
- Initial tactic and any tactic shift.
- Consequential exit state.
- Direct trigger inherited by the next scene.

Flag characters who know information they never acquired, forget information without cause, reset a relationship, change possession/location without evidence, or act as if a prior consequence did not occur.

### 3. Reconstruct Character Strategy

For every important behavioral turn, identify:

```text
new stimulus or failed tactic
-> perceived threat/opportunity
-> new strategy
-> cost or result
```

Flag a turn when the text supplies no new stimulus, changed cost, deadline, evidence, failure, or option constraint.

For every central action, name the most obvious safer, cheaper, easier, or more direct alternative visible to the character. Scan both physical and social/institutional routes: ask, disclose, call, negotiate, substitute, delay, cancel, report, leave, or accept a smaller loss. If the text does not show the attempt changing the situation or establish why the character rejects or cannot use the option, flag author convenience. Do not excuse it merely by calling the character irrational or by treating an ordinary rule as proof that emergency negotiation cannot occur.

For each consequential supporting character, run a replacement test: if a rule, warning, timer, or conscience speech can replace the person without materially changing choices or relationships, flag functional characterization. Check whether the character has an independent stake, makes a credible self-protective mistake or compromise, and changes judgment when new evidence arrives.

### 4. Reconstruct Dialogue Response

Audit consequential dialogue beats, not every filler syllable.

For each beat, identify:

- The prior words, action, silence, object, or environmental change being answered.
- What the speaker appears to have heard or inferred.
- What response the speaker is trying to produce.
- The tactic used.
- The listener's reaction or counter-tactic.
- The resulting information, relationship, power, commitment, or action change.

Literal non-response is not automatically a failure. It passes when the evasion, interruption, silence, misunderstanding, or topic shift is a motivated tactic and has a traceable effect. It fails when the reader must invent a hidden motive to connect unrelated lines.

Do not require every line to advance the main plot. Require every consequential beat to belong to a current objective, defense, test, relationship negotiation, or strategy change.

Also check:

- Can the speakers be distinguished with labels hidden?
- Do they hear, notice, protect, evade, and attack differently?
- Are they allowed to interrupt, repeat, misunderstand, answer indirectly, or leave words unfinished when pressure makes that credible?
- Is a line present mainly so the writer can explain the plot, motive, or theme?
- Is the conversation unnaturally symmetrical, with both people equally concise and logically complete?
- Does the reply sound like something this person would say now, or like the shortest sentence the writer needs to prove the scene?
- Does one line unnaturally package a conclusion, background fact, motive, and justification that a pressured person would not volunteer together?
- When read aloud or paraphrased in everyday speech, does the exchange still sound speakable without adding invented stutters or filler?
- Do not excuse crafted wording merely because its tactic and listener effect are traceable. If an everyday paraphrase preserves the same action while the written line mainly packages a clue, setup, or payoff, count it as writer-shaped. In a sample of three minutes or less, two such consequential lines are sustained compression, not a minor aesthetic note.

### 5. Reconstruct Setup And Payoff

For every climax mechanism, reveal, recurring object, information rule, or motif, locate:

```text
establishment
-> changed function or meaning
-> payoff
-> choice, power, physical possibility, or result changed
```

Flag:

- A capability, object, rule, or fact introduced only when the climax needs it.
- A repeated element that never changes a choice or result.
- A twist that adds new information but does not explain earlier anomalies.
- A payoff whose required location, holder, knowledge, or physical state was not preserved.

### 6. Run Deletion And Counterfactual Tests

Use targeted tests rather than rewriting the whole story:

- Delete one scene: do later decisions remain equally plausible?
- Remove one setup: does the payoff still work unchanged?
- Hold facts constant but remove the stated trigger: does the character still change strategy for no reason?
- Replace a line with a neutral acknowledgement: does the later escalation lose its ignition?

A successful counterfactual explains what causal work the element performs. Do not call an element essential merely because the result feels less stylish without it.

### 7. Record Reader Response Without Turning Taste Into Proof

Answer briefly from the raw text:

- At what point did the main story become clear?
- At what point, if any, did attention drop because the goal or action was unclear?
- Which major action felt least believable, and what obvious alternative caused the doubt?
- Which consequential line sounded most like the writer speaking instead of the character?
- Could the speakers be distinguished without labels?
- When did the ending become predictable, and did the remaining scenes add a new cost, meaning, or choice?
- What concrete human consequence remains after the ending?

These answers do not prove universal taste. They prevent a logic-only PASS from being misreported as an excellent screenplay.

## Failure Levels

### BLOCKER

- Fact or world-rule contradiction.
- Character uses knowledge they never obtained.
- Major event or turn has no prior condition and no motivated action.
- Character changes strategy without a stimulus, failure, cost, or option change.
- Climax solution depends on an unestablished convenience.
- A required scene transition cannot be reconstructed from the text.
- The central conflict exists only because a character ignores an obvious available solution, with no established reason.

### MAJOR

- The opening withholds the basic situation so long that a reader cannot identify whose immediate problem, action, and resistance they are following.
- Dialogue response chain breaks at a consequential turn.
- The next scene ignores the previous exit state.
- Relationship or power changes without observable action or evidence.
- Setup repeats but does not change function or result.
- A scene is removable without changing later decisions.
- Important characters use interchangeable voices or every major exchange reads as complete logical debate rather than behavior.
- Consequential dialogue repeatedly sounds like compressed screenplay explanation rather than speakable human response.
- The ending resolves the mechanism but carries no established character choice or concrete cost.

### AESTHETIC

- Rhythm, compression, wording, tone, humor, metaphor, or taste preferences after logic remains reconstructable.

Do not mix aesthetic dislike with causal failure. Do not downgrade a blocker because the intended meaning is attractive.

## Required Output

```markdown
# Cold-Read Verdict
- Evidence label: INDEPENDENT COLD READ / PARTIAL ISOLATION / SELF-AUDIT ONLY
- Scope read:
- Logic verdict: PASS / FAIL
- Story verdict: PASS / WEAK / FAIL
- User/aesthetic status: NOT ASSESSED / DELIVERED FOR REVIEW / USER ACCEPTED

## Reconstructed Causal Chain
...

## Plain-Story Retell
...

## Obvious Alternative Test
...

## Blocking Failures
| Anchor | What the text establishes | Missing or contradictory link | Downstream damage | Return layer |

## Major Failures
| Anchor | Broken response/state/payoff | Why a cold reader cannot reconstruct it | Return layer |

## Character Knowledge And Strategy Map
...

## Dialogue Breaks
...

## Character Voice And Reader Response
...

## Setup/Payoff Map
...

## Aesthetic Notes Kept Separate
...

## Uncertain Because The Text Is Ambiguous
...
```

Every failure must cite a scene, action, or dialogue anchor. Generic statements such as `logic is weak`, `dialogue is unnatural`, or `motivation needs strengthening` are invalid.

## Return Layers

Route each failure to one owner:

```text
world/knowledge contradiction -> single source of truth
unmotivated event -> causal spine
unmotivated behavior -> character state machine
unchanged/reset scene -> scene state card
non-responsive dialogue -> dialogue response chain
convenient climax/twist -> information and prop lifecycle
```

The auditor does not patch an upstream break with line polish. The writer repairs the named layer and submits a clean text for a new cold read.

If independent readers disagree on `LOGIC` or `STORY`, do not select the favorable verdict. Status remains unresolved; preserve both reports, repair any exact text-anchored blocker or major failure either reader can substantiate, and submit a clean draft to a new reader.

## Pass Standard

Report two separate verdicts:

- `LOGIC PASS / FAIL`: continuity, knowledge, causality, strategy triggers, and setup/payoff.
- `STORY PASS / WEAK / FAIL`: plain retell, believable action choice, concrete cost, character distinction, dialogue behavior, and reader response.

`LOGIC PASS` means, within the audited scope:

- No blocker remains.
- Every consequential scene transition is reconstructable.
- Character knowledge and strategy changes are traceable.
- Consequential dialogue beats have motivated response chains.
- Climax mechanisms and major payoffs have preserved setup conditions.

`STORY PASS` additionally requires a reconstructable opening situation, no major obvious-alternative failure, no interchangeable central voices, no sustained writerly dialogue compression, a clear chain of human actions, and an ending produced by a costly choice. A pass still does not prove universal excellence or that the user will like it. Only an explicit user judgment may set `User/aesthetic status: USER ACCEPTED`; an auditor must never infer it.
