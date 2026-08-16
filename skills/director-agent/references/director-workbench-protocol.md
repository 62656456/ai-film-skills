# Director Workbench Protocol

This protocol rewrites useful design patterns from the verified GitHub watchlist into a practical workbench for the user's `director-agent`.

Borrowed patterns:

- **ViMax**: role separation, long-script segmentation, director/screenwriter/producer/generator roles, shot-level planning, continuity through references.
- **VideoClaw**: visible staged production line from idea -> script -> character/scene -> storyboard -> reference images -> video -> post-production.
- **Storyboarder**: storyboard board workflow, Fountain/script-to-board thinking, animatic timing, fast iteration and export handoff.

This is not a claim that those projects are locally installed or fully adopted. It is a rewritten workflow logic.

## Contents

- Core Principle
- Workbench Rooms
- Default Output: Workbench Package
- Coverage Ledger And Project Card
- Director, Screenwriter, And Production Rooms
- Asset Bible, Scene Board, And Animatic Check
- Generation And Postproduction Handoff
- Usability Rules
- Anti-Overbuild Rule

## Core Principle

Never one-shot a film project, but do not force a fixed production pipeline onto pure screenplay writing. Choose the path by task:

```text
Pure script creation or repair:
Project facts when needed -> A3 Writer Room -> state/causality audit -> isolated Cold Read -> readable screenplay

Director design for an approved script:
Approved screenplay -> Director Room -> Asset Bible -> Scene Board

Production storyboard:
Approved screenplay + approved director design -> Asset Bible -> Scene Board -> Shot Board -> handoff
```

Do not send a screenplay with unresolved causal or dialogue blockers downstream to Director Room or Shot Board.

## Workbench Rooms

### 0. Coverage Ledger

Purpose: prevent skipped material.

Fields:

- Source units: acts/scenes/sequences/paragraphs.
- Covered now.
- Not covered.
- Continuation anchor.
- Assumptions.

### 1. Project Card

Purpose: define the whole creative object before details.

Fields:

- Title.
- Format: short film / short drama / motion comic / ad / scene test / trailer / full film segment.
- Duration target.
- Aspect ratio and platform.
- Genre and tonal promise.
- Audience endpoint.
- Logline.
- Core conflict.
- Source status: original / adaptation / user draft / historical / ASSUMED.
- Verification status if real facts are involved.

### 2. Director Room

Purpose: decide the governing creative logic.

Fields:

- Director's idea.
- Visual concept.
- Motif chain: establish -> vary -> pay off/break.
- Spatial power geometry.
- Information design: suspense / mystery / surprise.
- Anti-default decision.
- Sound idea.
- Time/edit rule.
- Style coordinate with source level: verified / inferred / ASSUMED.

### 3. Writer Room

Purpose: first tell a complete story through believable behavior and character-specific dialogue, then verify that it is playable and shootable.

Creation layer, in this order:

- Read `screenplay-writing-core.md` and the exact A3 cards routed for the task.
- Plain story: who wants what, why now, what they do, what it causes, how they change approach, what final choice occurs, and what it costs.
- Character behavior: knowledge, want, fear/protection, chosen action, obvious available alternative, reason for rejecting it, and resulting consequence.
- Scene action chain: immediate objective -> action -> resistance -> adaptation/refusal -> changed exit situation -> next necessity.
- Dialogue behavior: purpose, surface line, protected subtext, listener effect, character-specific voice, interruption/evasion/silence when motivated.
- Anti-AI pass using A3-18 and A3-19 when needed.
- Exact script draft or replacement passage when requested.

Verification layer, only after the creation layer exists:

- Single source of truth: facts, assumptions, world rules, character knowledge, relationship state, physical conditions.
- Story engine: concrete want, why now, active opposition, cost, current strategy, irreversible choice.
- Causal spine: prior condition -> character action/refusal -> result -> state change -> next necessity.
- Character state machines: goal, knowledge/belief, perceived threat/opportunity, power, tactic, tactic-shift trigger, boundary.
- Scene entrance and exit states.
- Dialogue response chains: stimulus -> perceived meaning -> objective -> tactic -> counter-tactic -> state delta.
- Information/prop lifecycle: establish -> change function or meaning -> payoff that changes a choice or result.
- Rewrite targets.

Use `screenplay-state-engine.md` for the verification layer only. Do not advance broken writing into visual design or a storyboard merely because all Writer Room fields are present, and do not call the story excellent because the verification fields pass.

### 4. Producer Constraint Room

Purpose: stop the design from becoming unusable.

Fields:

- Production constraints: AI-only / live-action / hybrid / budget / location / cast count.
- AI platform assumptions.
- Duration and shot-count range.
- Risk list: faces, hands, text, crowds, continuity, action density, lip sync.
- Required assets.
- Handoff format.

### 5. Asset Bible

Purpose: stabilize continuity before shot work.

Fields:

- Character anchors: appearance, costume, state, arc pressure.
- Scene anchors: location, time, geography, light source, color rules.
- Prop anchors: shape, material, state, continuity risk.
- Motif anchors: recurring object/image/sound/color.
- Reference plan: what needs reference image, style frame, or user approval.

Rule: no production storyboard without stable anchors unless marked `ASSUMED`.

### 6. Scene Board

Purpose: turn the script into scene-level playable blocks.

For each scene:

- Scene function.
- Direct cause from the previous scene.
- Entrance state: facts, knowledge, relationships, power, physical conditions.
- Objective/obstacle.
- Initial tactic and tactic-shift trigger.
- Turn and irreversible result.
- Exit state and direct trigger for the next scene.
- Power shift.
- Audience beat.
- Audience knowledge / character knowledge / withheld information.
- Visual strategy.
- Sound/time/edit strategy.
- Required assets.
- What must not be shown yet.

Hard gate: a scene may end unresolved, but it may not end unchanged. The next scene must inherit its exit state.

### 7. Shot Board / Animatic

Purpose: prepare for `ai-storyboard-director` or visual preproduction.

For each shot candidate:

- Board ID.
- Source unit covered.
- Duration estimate.
- Image sentence.
- Character/action.
- Camera/shot size.
- Sound cue.
- Cut motive.
- Continuity in/out.
- Reference need.
- Animatic note: hold / cut / bridge / pause / accelerate.

Storyboarder-inspired check:

- Can the boards play in order as an animatic?
- Is the emotional rhythm visible without prose explanation?
- Are any two adjacent boards redundant?
- Does any shot require a hidden cut inside one generated clip?

### 8. Generation Handoff

Purpose: make downstream production possible.

Fields:

- Approved director design.
- Locked anchors.
- Shot board range.
- Model/platform assumptions.
- Start/end frame requirements.
- Reference image list.
- Negative constraints.
- Dialogue/lip-sync status.
- `ai-storyboard-director` handoff prompt or constraints.

### 9. Post-Production Handoff

Purpose: prevent the work from stopping at raw shots.

Fields:

- Edit rhythm.
- Transitions.
- Sound/BGM direction.
- Color/LUT direction.
- Subtitle/dialogue treatment.
- Export aspect/duration.
- Review checklist.

## Default Output: Workbench Package

When the user asks to create a director Agent workflow, project workflow, or reusable production plan, output:

```markdown
# 导演工作台：<项目名>

## 0. 覆盖账本
| 单元 | 状态 | 说明 |

## 1. 项目卡
...

## 2. 导演室
...

## 3. 编剧室
...

## 4. 制片/约束室
...

## 5. 资产圣经
...

## 6. 场景与分镜板
...

## 7. Animatic 节奏检查
...

## 8. 生成与后期交接包
...

## 9. 未覆盖 / 待查证 / 下一步
```

## Usability Rules

- When the user requests a workbench, plan, or production package, each active room must output fields the user can edit.
- Do not hide requested planning decisions in prose; make them visible as cards, tables, anchors, or constraints.
- Keep assumptions visible.
- If only one scene is being handled and project continuity matters, use a lightweight version of the relevant room; otherwise deliver the requested scene directly.
- If the user wants pure writing and not production, use Writer Room only. Add Director Room only when the user also asks for interpretation, staging, performance, sound, edit, or visual design.
- For pure screenplay requests, keep internal state ledgers out of the delivered reading copy unless the user asks to inspect them.
- If the user wants full分镜, complete Project/Director/Asset/Scene/Shot cards first, then hand off to `ai-storyboard-director`.

## Anti-Overbuild Rule

Do not force the full workbench on tiny requests.

- One screenplay scene: Writer Room only; add project facts only when continuity depends on them.
- Rewrite one paragraph: Writer Room only unless the user explicitly asks for a director note.
- Full short film / short drama / sequence requested as pure writing: Writer Room + state audit + isolated cold read.
- Full production design for a short film / short drama / sequence: full workbench.
- Production分镜: full workbench through Shot Board, then AG-CLIP handoff.
