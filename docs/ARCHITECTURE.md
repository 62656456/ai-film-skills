# Architecture

## Repository layers

```text
skills/
  <skill-name>/
    SKILL.md                 required agent instructions
    agents/openai.yaml       UI metadata
    references/              selectively loaded knowledge
    scripts/                 deterministic helpers, when needed
    assets/                  output resources, when needed
  references/                shared contracts used by multiple Skills
experimental/
  <skill-name>/              isolated, never installed by default
docs/i18n/                   translated repository entry points
scripts/                     repository validation
```

## Runtime route

```text
user request
    ↓ semantic trigger
one primary Skill
    ↓ explicit handoff only when needed
second Skill with a different output contract
    ↓
visible deliverable
    ↓
structural, factual, visual, or runtime validation
```

Skills do not share authority merely because they are stored together. Story decisions belong to the directing layer; asset definitions belong to asset Skills; genre Skills supply observable visual parameters; production Skills cannot spend money or publish without the required approval gates.

## Version and evidence states

Structure, deployment, real-task evidence, and user acceptance are recorded separately. A valid folder can load while still producing poor work. An experimental package can contain substantial research while remaining unapproved. Repository labels must preserve those distinctions.
