# Research And Update Protocol

This protocol prevents the Agent from relying on stale notes or invented film knowledge.

## Contents

- When To Verify Online
- Source Priority
- Evidence Tiers
- How To Use Research
- Output Citation Behavior
- Updating The Skill
- User Fit Check
- Research Stop Rule

## When To Verify Online

Use web verification when the task depends on:

- A real director, cinematographer, editor, actor, film, movement, school, textbook, interview, or historical production fact.
- A film-theory claim not already supported in `verified-director-logic.md`.
- Current AI video model/platform capability, generation limits, prompt behavior, or production workflow.
- User asks for "最新", "查证", "真实", "教材", "教科书", "大师方法", "全球导演", "不要臆想".
- The bundled references and newly verified public evidence disagree or feel incomplete.

## Source Priority

Prefer:

1. Primary sources: books, publisher pages, official interviews, director/cinematographer/editor interviews, museum/academy/BFI/Criterion/ASC/BSC resources.
2. University/film-school resources and syllabi.
3. Reputable film journals, established criticism, major trade publications.
4. Secondary explainers only as support, not as the sole basis for a claim.

Avoid using social posts, marketing pages, unsourced blogs, and AI-generated summaries as load-bearing evidence.

## Evidence Tiers

Label internally:

- **A**: primary/official/source text.
- **B**: reputable educational or institutional secondary source.
- **C**: useful but non-authoritative explanation.
- **D**: unsupported; do not use as fact.

Only A/B evidence should support claims about real directors, film history, or named methods.

## How To Use Research

Research must become a decision rule, not trivia.

Bad:

```text
Hitchcock was good at suspense, so make it suspenseful.
```

Usable:

```text
Information rule: let the audience see the danger before C1 does; keep C1's eyeline away from it for two beats; cut to C2 only after the sound cue.
```

Every researched item should be converted into:

- A director decision rule.
- A concrete action/image/sound/edit/time choice.
- A limitation or misuse warning.

## Output Citation Behavior

When research materially shapes the answer, include a compact `查证依据` section with links. Keep it short:

```markdown
## 查证依据
- Source: <link> — used for <specific rule>
- Source: <link> — used for <specific rule>
```

Do not flood the answer with citations when the user asked for a practical script or director plan. Cite only the important basis.

## Updating The Skill

Research never authorizes a file change by itself. Rewrite this Skill only when the user explicitly authorizes an update to this package and its scope in the current task.

The following are candidate signals, not independent permission to write:

- A repeated task reveals a potentially stable new rule.
- A verified correction exposes a wrong or weak bundled rule.
- The user states a personal preference that may deserve a private/local overlay.

Report these as proposed changes first. Do not modify files, installation copies, Git history, releases, or public documentation until the user authorizes the exact target and scope. A personal preference must not enter a public package merely because it should persist locally; generalize it only with explicit approval, remove private details, and keep local-only preferences out of the public runtime.

When updating:

- Add concise decision rules, not long articles.
- Keep detailed source notes in references, not the main `SKILL.md`.
- Preserve the anti-laziness contract.
- Mark user-specific preferences as user preference, not universal film law.
- Treat repository commit, push, release, installation sync, and other external mutations as separately permissioned actions; authorization to research or propose an update does not authorize them.

## User Fit Check

The Agent cannot guarantee in advance that every output matches the user's taste. It must instead use a feedback loop:

1. Produce a usable version.
2. Ask or infer what the user rejects.
3. Convert rejection into a rule.
4. Update future outputs or skill references when requested.

User correction format:

```text
用户不想要：<bad pattern>
以后必须：<replacement rule>
适用范围：<script / storyboard / director treatment / all>
```

## Research Stop Rule

Do not research forever. Stop when you have enough evidence to make the next useful decision.

If evidence remains incomplete:

- Say what is verified.
- Say what is uncertain.
- Give a conservative usable plan.
- Mark the uncertain claim `待查证`.
