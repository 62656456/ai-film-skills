# Installation

Choose the source or archive snapshot first, then install one complete Skill folder. The [catalog](../SKILL_CATALOG.md) and [workflow](WORKFLOW.md) explain which module owns the requested outcome.

## Choose a snapshot

| Distribution | What it contains | How to use it |
|---|---|---|
| Current source tree | Storyboard Director 5.6, the updated visual contracts and 20 modules: 18 regular plus 2 experimental | Clone or download the intended source ref and use the local installer |
| [Published v1.3.0](https://github.com/62656456/ai-film-skills/releases/tag/v1.3.0) | Historical snapshot with Storyboard Director 5.4.4 and the older 19-module inventory | Use when deliberately reproducing that release; its ZIP does not track current source |
| Separately labeled 5.6 standalone Preview | An independently labeled preview artifact with its own manifest | Read that artifact's label and scope; do not treat it as a new complete-studio release |

A source update or local ZIP build is not a GitHub Release publication. The new whitebox package has no v1.3.0 release asset. Do not infer an archive version from the word `latest`.

## Install from a clone

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
git log -1 --oneline
python scripts/install_skill.py --list
python scripts/install_skill.py ai-storyboard-director --platform codex
```

The installer reads the files in your actual checkout. Inspect its `SKILL.md` version before installation; cloning a public default branch does not fetch unpublished local changes. Select an explicitly intended branch, tag or commit before running the installer when reproducing a particular snapshot.

Supported installer targets include `codex`, `claude-code`, `trae` and `codebuddy`. For a project-specific destination:

```bash
python scripts/install_skill.py ai-storyboard-director --target /path/to/project/.agents/skills
```

The installer refuses to overwrite an existing installation unless `--force` is explicitly supplied. Keep the prior known version before replacing it. A complete Skill folder includes all its referenced files; copying `SKILL.md` alone is insufficient.

## Experimental packages

Both experiments remain outside the normal complete-studio archive and require an explicit choice:

```bash
python scripts/install_skill.py hard-sci-fi-visual-director --platform codex --experimental
python scripts/install_skill.py whitebox-previs-executor --platform codex --experimental
```

Hard-science-fiction has user-accepted image examples but is still distributed as an experiment. Whitebox requires a compatible Python/Blender/media runtime; the Skill does not bundle Blender or install it silently. Its implemented humanoid/basic-camera route and individually qualified action profiles do not provide arbitrary complete fight choreography. Unsupported proxies or unpassed actions must remain blocked or diagnostic.

The external [xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director) is linked for workflow completeness only. It is not copied into this repository or any archive; follow its upstream terms independently.

## Published ZIPs and complete studio

The [v1.3.0 assets](https://github.com/62656456/ai-film-skills/releases/tag/v1.3.0) contain individual module ZIPs and `open-film-skills-complete.zip`. These are old snapshots. Current source builds contain 18 regular modules in the complete archive; the 2 experiments are separate opt-in ZIPs. Inspect the build manifest's source ref and hashes.

For manual installation, copy each selected complete module folder into the host's documented Skill location. An upload-based host may accept the standalone ZIP. Native paths and the difference between instruction reading and native activation are described in [Compatibility](COMPATIBILITY.md).

## Optional Skills CLI route

The open [Skills CLI](https://github.com/vercel-labs/skills) can discover a public repository:

```bash
npx --yes skills@latest add 62656456/ai-film-skills --list
npx --yes skills@latest add 62656456/ai-film-skills --skill ai-storyboard-director --agent codex --copy --yes
```

The recorded CLI 1.5.23 verification covered the older 18-regular-module discovery and six-file 5.4.4 copy. It is historical evidence, not a fresh 5.6/20-module host test. See [CLI evidence](../examples/skills-cli-install-verification.md) and [historical directory-index evidence](../examples/skills-sh-index-verification.md). Installation counts include maintainer tests and are not distinct external-user adoption.

## Verify the result

Check the installed version, every local reference, and any required runtime tool. Then run a small task with the actual host. File equality, host routing, text output, real media and user acceptance remain separate checks. Storyboard 5.6 can answer a one-shot text question without a project directory; claiming saved/restored project decisions requires actual file operations in the supplied work directory. Generated image examples do not prove video-model execution.
