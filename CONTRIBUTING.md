# Contributing

Contributions should improve a Skill's real task performance without hiding its evidence state.

1. Open an issue describing a concrete user request that should trigger the Skill.
2. Keep `SKILL.md` concise and move detailed knowledge into directly linked `references/` files.
3. Use lowercase letters, digits, and hyphens for Skill directory names.
4. Keep only `name` and `description` in `SKILL.md` frontmatter.
5. Update `agents/openai.yaml` when the trigger or purpose changes.
6. Add deterministic scripts only when repeated code or a fragile operation justifies them.
7. Do not include project secrets, private paths, copyrighted course copies, generated caches, or user data.
8. Run `python scripts/validate_skills.py`.
9. Describe structural checks separately from real-task or user-acceptance evidence.

Do not revive anything listed as retired in `SKILL_CATALOG.md` without an explicit new decision and new validation evidence.
