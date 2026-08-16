# Contributing

Contributions should improve a Skill's real-task performance without hiding its evidence state, breaking its standalone package, or tying the canonical workflow to one Agent host.

## Change the runtime contract

1. Open an issue describing a concrete user request that should trigger the Skill and the visible result that should pass.
2. Keep `SKILL.md` concise and move detailed knowledge into directly linked `references/` files.
3. Use lowercase letters, digits, and hyphens for Skill directory names.
4. Keep only the portable `name` and `description` fields in `SKILL.md` frontmatter.
5. Keep every required script, reference, template, and asset inside the same Skill folder. A shared runtime `skills/references/` directory is forbidden.
6. Treat `agents/openai.yaml` as optional Codex presentation metadata. Other hosts must be able to ignore it without losing the Skill workflow.
7. Do not add Claude-, TRAE-, CodeBuddy-, WorkBuddy-, or Codex-only instructions to the canonical body unless the workflow truly requires that host; document host adapters separately.
8. Add deterministic scripts only when repeated code or a fragile operation justifies them, then run the script on a representative case.
9. Do not add `README.md`, `INSTALLATION_GUIDE.md`, `CHANGELOG.md`, or other human-facing auxiliary files inside an individual Skill folder. Human documentation belongs in the generated repository-level design guides.
10. Do not include project secrets, private paths, copyrighted course copies, generated caches, personal project records, company or client work, or user data.

## Keep the GitHub reading guide in sync

Every module has one English and one Simplified Chinese human-readable guide. These 38 pages explain the runtime contract; they do not replace it.

1. Read [How every Skill is designed](docs/SKILL_DESIGN_SYSTEM.md).
2. Update the relevant reviewed entry in `docs/skill-contracts.json` whenever a runtime change affects purpose, principles, standalone scope, inputs, workflow, return path, review gates, pass standard, outputs, boundaries, status, or host requirements.
3. Run:

   ```bash
   python scripts/generate_skill_guides.py
   python scripts/validate_skill_docs.py
   python scripts/validate_repository.py
   ```

4. Do not hand-edit a generated file under `docs/skills/en/` or `docs/skills/zh-CN/` as an independent source of truth. Change the reviewed registry or generator, then regenerate both languages.
5. Keep the module's design-guide name as the human GitHub entrance while preserving direct links to its runtime `SKILL.md` and standalone ZIP.
6. A failed check must return to a named earlier decision, and a pass standard must name observable evidence. “Optimized,” “professional,” or “cinematic” is not evidence by itself.

## Validate packaging and evidence

1. Build deterministic packages:

   ```bash
   python scripts/build_skill_packages.py --include-experimental --output dist/skills
   ```

2. Smoke-install at least one affected module with `scripts/install_skill.py` into a temporary target.
3. Describe structural checks separately from real-task, host-runtime, and user-acceptance evidence.
4. Do not call a module practice-validated without accepted evidence from three different real tasks.
5. Keep experimental modules explicitly experimental; packaging, generated guides, or an internal review cannot promote them.

When adding a host, link its official documentation and classify it as one of:

- native Skill discovery;
- official local-package import;
- instructions-only fallback.

Do not describe an instructions-only fallback as native integration. Do not revive anything listed as retired in [SKILL_CATALOG.md](SKILL_CATALOG.md) without an explicit new decision and new validation evidence.

Use [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions), [GitHub Issues](https://github.com/62656456/ai-film-skills/issues), or [haldissita@gmail.com](mailto:haldissita@gmail.com) for proposals.
