# Contributing

Contributions should improve a Skill's real-task performance without hiding its evidence state or tying the canonical package to one Agent host.

1. Open an issue describing a concrete user request that should trigger the Skill.
2. Keep `SKILL.md` concise and move detailed knowledge into directly linked `references/` files.
3. Use lowercase letters, digits, and hyphens for Skill directory names.
4. Keep only the portable `name` and `description` fields in `SKILL.md` frontmatter.
5. Keep every required script, reference, template, and asset inside the same Skill folder.
6. Treat `agents/openai.yaml` as optional Codex presentation metadata. Other hosts must be able to ignore it without losing the Skill workflow.
7. Do not add Claude-, TRAE-, CodeBuddy-, WorkBuddy-, or Codex-only instructions to the canonical body unless the workflow truly requires that host; document host adapters separately.
8. Add deterministic scripts only when repeated code or a fragile operation justifies them.
9. Do not include project secrets, private paths, copyrighted course copies, generated caches, or user data.
10. Run `python scripts/validate_repository.py` and `python scripts/build_skill_packages.py --output dist/skills`.
11. Smoke-install at least one affected module with `scripts/install_skill.py` into a temporary target.
12. Describe structural checks separately from real-task, host-runtime, and user-acceptance evidence.

When adding a host, link its official documentation and classify it as one of:

- native Skill discovery;
- official local-package import;
- instructions-only fallback.

Do not describe an instructions-only fallback as native integration. Do not revive anything listed as retired in `SKILL_CATALOG.md` without an explicit new decision and new validation evidence.

Use [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions), [GitHub Issues](https://github.com/62656456/ai-film-skills/issues), or [haldissita@gmail.com](mailto:haldissita@gmail.com) for proposals.
