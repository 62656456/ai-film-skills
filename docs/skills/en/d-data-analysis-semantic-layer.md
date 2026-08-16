# d-data-analysis-semantic-layer — approved knowledge writing

| Status | Deployed |
|---|---|
| Can deliver alone | Candidate review, validation, version/expiry planning, and a pending-write package; actual writing when the host capability and current approval exist. |
| Cannot claim alone | No current approval or no write capability means it cannot claim that the knowledge base was updated. |

[Runtime `SKILL.md`](../../../skills/d-data-analysis-semantic-layer/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-data-analysis-semantic-layer.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Validate, version, expire, preserve conflicts, and write approved analytical candidates into a semantic knowledge layer with a reconciled receipt.

<!-- contract:principles -->
## 2. Design principles

- The current conversation's explicit approval is the only write authority; old messages and approval-looking fields do not count.
- Validation, versioning, expiry, conflict, history, and write receipt remain separate facts.
- If the write capability is unavailable, produce a pending package and state that nothing was written.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

Candidate review, validation, version/expiry planning, and a pending-write package; actual writing when the host capability and current approval exist.

**Cannot claim alone:** No current approval or no write capability means it cannot claim that the knowledge base was updated.

<!-- contract:inputs -->
## 4. Inputs

- A formal report and candidate records that the user has already seen.
- Explicit current approval such as approval to absorb, update, or write the data knowledge layer.
- Source, data date, statistical period, platform, region, evidence grade, expiry, review date, status, version, limits, and monitoring fields.

<!-- contract:workflow -->
## 5. Workflow

1. Verify that the current user approval covers the exact candidate and action.
2. Read the semantic contract, evidence register, current layer, source inventory, and version/expiry rules.
3. Validate candidate JSON or JSONL and repair all errors without hiding conflicts or weak evidence.
4. Apply version, expiry, dispute, replacement, and history rules.
5. Write through the authorized capability or emit a pending-write package; then reconcile the receipt with actual state.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- No explicit current approval stops the workflow before any mutation.
- Validation errors return to the exact field; source conflicts remain disputed records rather than silent overwrites.
- Unavailable write capability returns a pending package, not a false completion claim.

<!-- contract:review -->
## 7. Review gates

- [ ] Every record contains the required conclusion, fact type, source, dates, period, platform, region, grade, expiry, status, version, limits, and indicators.
- [ ] Weak evidence enters only the waiting-for-validation area; expired or replaced records preserve history.
- [ ] The write receipt, version, review date, conflict state, and actual semantic layer agree.

<!-- contract:pass -->
## 8. Pass standard and states

- Candidate validation passes and the actual write or pending-write state is reported exactly.
- Only a reconciled write receipt proves an update; a valid package by itself does not.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- Lists of added, superseded, disputed, historicized, rejected, and unwritten records.
- A version and next-review receipt, or a clearly labeled pending-write package.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not trigger on analysis, reading, candidate generation, or historical approval.
- Do not delete history, silently overwrite conflicts, promote inference to official fact, or claim an unavailable write occurred.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Review and pending-package creation require file/Python capability. Actual writing additionally requires the installed semantic-layer workflow and explicit current user approval.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/d-data-analysis-semantic-layer/agents/openai.yaml)
- [`SKILL.md`](../../../skills/d-data-analysis-semantic-layer/SKILL.md)

**References**

- [`references/evidence.md`](../../../skills/d-data-analysis-semantic-layer/references/evidence.md)
- [`references/records-v1.0.0.json`](../../../skills/d-data-analysis-semantic-layer/references/records-v1.0.0.json)
- [`references/semantic-contract.md`](../../../skills/d-data-analysis-semantic-layer/references/semantic-contract.md)
- [`references/semantic-layer.md`](../../../skills/d-data-analysis-semantic-layer/references/semantic-layer.md)
- [`references/source-inventory.md`](../../../skills/d-data-analysis-semantic-layer/references/source-inventory.md)
- [`references/versioning-and-expiry.md`](../../../skills/d-data-analysis-semantic-layer/references/versioning-and-expiry.md)

**Deterministic helpers**

- [`scripts/validate_candidate.py`](../../../skills/d-data-analysis-semantic-layer/scripts/validate_candidate.py)
