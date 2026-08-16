# d-official-market-analysis — source-backed media research

| Status | Deployed |
|---|---|
| Can deliver alone | A source plan, validated dataset, evidence table, analysis, report, and separately labeled knowledge candidate. |
| Cannot claim alone | Offline use cannot fabricate current market facts, and a completed report does not authorize semantic-layer writing. |

[Runtime `SKILL.md`](../../../skills/d-official-market-analysis/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-official-market-analysis.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Research film, short drama, animation, AI film, and adjacent media markets from current official and authoritative evidence for a defined decision.

<!-- contract:principles -->
## 2. Design principles

- State only what current, public, verifiable evidence supports; keep inference separate from official fact.
- Data date, statistical period, region, platform, definition, and source authority travel with every conclusion.
- A report may produce a knowledge candidate, but only explicit later approval can authorize semantic-layer writing.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A source plan, validated dataset, evidence table, analysis, report, and separately labeled knowledge candidate.

**Cannot claim alone:** Offline use cannot fabricate current market facts, and a completed report does not authorize semantic-layer writing.

<!-- contract:inputs -->
## 4. Inputs

- Research date, region, platform, content type, decision use, budget, team, and constraints.
- Definitions for metrics and comparisons, including what cannot be inferred from rankings or heat values.
- Access to current primary or authoritative sources; otherwise the task remains a framework and source-gap report.

<!-- contract:workflow -->
## 5. Workflow

1. Plan sources and open the actual primary or authoritative evidence.
2. Build a data contract, clean records, run quality checks, and preserve definitions and missingness.
3. Compare periods and segments, test counterexamples, and separate facts, calculations, inferences, and unknowns.
4. Write the fixed report sections with evidence tables and decision implications.
5. Create a knowledge candidate only; route any approved write through the separate semantic-layer Skill.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Missing current evidence returns to source collection; definition conflicts return to the data contract; validation errors return to cleaning or calculation.
- Warnings remain explicit evidence limits; they are not erased to force a strong conclusion.
- No explicit approval means no knowledge write, even when a candidate is complete.

<!-- contract:review -->
## 7. Review gates

- [ ] Sources are opened, authoritative for the claim, dated, and linked; inaccessible evidence is marked instead of reconstructed from memory.
- [ ] Metric definitions, cleaning, calculations, sample limits, counterevidence, time sensitivity, and unknowns are visible.
- [ ] Charts and conclusions do not turn heat, rank, marketing copy, or a single case into sales, plays, market size, or success probability.

<!-- contract:pass -->
## 8. Pass standard and states

- The report passes structural and evidence checks, and every conclusion is labeled by fact type and strength.
- Limited evidence is reported as limited; report completion does not mean the market conclusion is timeless or officially endorsed.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A source-backed market report with scope, methodology, evidence table, findings, counterevidence, implications, and limits.
- A separately labeled semantic-layer candidate, never an automatic write.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not use search snippets, marketing pages, unverifiable screenshots, or stale repository data as current official evidence.
- Do not convert inference into official fact or write to the semantic layer without explicit approval.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Current analysis requires web or connector access to primary sources plus Python/file capability for data validation. Offline use can design the research and list missing evidence, not fabricate current findings.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/d-official-market-analysis/agents/openai.yaml)
- [`SKILL.md`](../../../skills/d-official-market-analysis/SKILL.md)

**References**

- [`references/analysis-and-report.md`](../../../skills/d-official-market-analysis/references/analysis-and-report.md)
- [`references/connector-contract.md`](../../../skills/d-official-market-analysis/references/connector-contract.md)
- [`references/data-contract.md`](../../../skills/d-official-market-analysis/references/data-contract.md)
- [`references/evidence-and-sources.md`](../../../skills/d-official-market-analysis/references/evidence-and-sources.md)
- [`references/platform-metrics.md`](../../../skills/d-official-market-analysis/references/platform-metrics.md)

**Deterministic helpers**

- [`scripts/validate_dataset.py`](../../../skills/d-official-market-analysis/scripts/validate_dataset.py)
