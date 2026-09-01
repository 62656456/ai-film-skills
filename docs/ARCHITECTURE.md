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

experimental/
  <skill-name>/              isolated, never installed by default
docs/
  SKILL_DESIGN_SYSTEM.md     shared human-readable design and review logic
  skill-contracts.json       reviewed bilingual contract registry
  skills/INDEX.md            GitHub reading index for all 19 modules
  skills/en/                 19 generated English design guides
  skills/zh-CN/              19 generated Simplified Chinese design guides
  i18n/                      translated repository entry points
scripts/
  generate_skill_guides.py   deterministic design-guide generator
  validate_skill_docs.py     guide, source-link, and status validator
  validate_repository.py     portable repository validator
```

Each Skill carries its own runtime references. A shared `skills/references/` directory is deliberately forbidden because it would break standalone downloads.

## GitHub reading layer

The runtime and reading layers have different jobs:

| Layer | Authority | Purpose |
|---|---|---|
| `SKILL.md` plus local resources | Canonical runtime instruction | Tells a compatible Agent how to perform the bounded task |
| `docs/skill-contracts.json` | Reviewed human-documentation source | Records the bilingual purpose, principles, inputs, workflow, return paths, gates, outputs, boundaries, status, and host requirements |
| `docs/skills/{en,zh-CN}/` | Generated reading layer | Lets a person understand and compare every module directly on GitHub |
| `docs/SKILL_DESIGN_SYSTEM.md` | Shared design explanation | Defines the common directed-return loop and separates structural, runtime, real-task, and user-acceptance states |

The generated pages explain the runtime contract; they do not replace it. Every page links the exact `SKILL.md`, every packaged reference or helper, the standalone ZIP, installation instructions, and Agent compatibility guidance. Edit the reviewed contract registry or runtime source, regenerate the 38 pages, then run both validators; do not hand-edit generated guides as an independent source of truth.

## Runtime route

```text
user request
    ↓ semantic trigger
one primary Skill
    ↓ verify required input and authority
visible, judgeable draft
    ↓ module-specific review gates
fail ──→ return to the earliest broken decision and preserve approved constraints
pass ──→ record evidence and produce the named output
    ↓ explicit handoff only when needed
second Skill with a different output contract
```

Skills do not share authority merely because they are stored together. Story decisions belong to the directing layer; asset definitions belong to asset Skills; genre Skills supply observable visual parameters; production Skills cannot spend money or publish without the required approval gates.

## Version and evidence states

Structure, deployment, real-task evidence, and user acceptance are recorded separately. A valid folder can load while still producing poor work. An experimental package can contain substantial research while remaining unapproved. Repository labels must preserve those distinctions.

The common evidence ladder is:

1. structurally valid;
2. loadable or runnable in a compatible host;
3. validated on a real task with evidence;
4. explicitly accepted by the user.

A lower state must never be promoted to a higher state by documentation, packaging, generation, or internal review alone. Read [How every Skill is designed](SKILL_DESIGN_SYSTEM.md) and [all module design guides](skills/INDEX.md) for the complete public contract.
