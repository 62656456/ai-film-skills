# 2026-10-09 review closure and v1.4.0 maintenance

This audit covers all 33 inline Codex review comments visible at the maintenance freeze, against source commit `11ad3a8fa5fe18b00087cdfa08300bc7689dcb9b`. Twenty-three issues remained applicable and are corrected in this maintenance change; seven were already resolved; one obsolete rollback mechanism is not restored; two concern the superseded 5.6 preview branch. Comment status on an old PR is not a current-source defect count.

Current source: Storyboard Director A5.7.2. Distribution: v1.4.0, 21 individual Skill packages and one complete archive containing the 18 regular packages. Experimental packages remain opt-in. Existing media and frozen study archives retain their bytes and evidence state; the current B5.7.1-jev study package is not relabeled as A5.7.2.

| Review | Maintenance disposition | Scope |
|---|---|---|
| [PR 1 / 3792075589](https://github.com/62656456/ai-film-skills/pull/1#discussion_r3792075589) | Already resolved | Current implementation already addresses the original report. |
| [PR 1 / 3792075593](https://github.com/62656456/ai-film-skills/pull/1#discussion_r3792075593) | Already resolved | Current implementation already addresses the original report. |
| [PR 1 / 3792075595](https://github.com/62656456/ai-film-skills/pull/1#discussion_r3792075595) | Already resolved | Current implementation already addresses the original report. |
| [PR 1 / 3792075597](https://github.com/62656456/ai-film-skills/pull/1#discussion_r3792075597) | Already resolved | Current implementation already addresses the original report. |
| [PR 1 / 3792075599](https://github.com/62656456/ai-film-skills/pull/1#discussion_r3792075599) | Already resolved | Current implementation already addresses the original report. |
| [PR 2 / 3792198306](https://github.com/62656456/ai-film-skills/pull/2#discussion_r3792198306) | Already resolved | Current implementation already addresses the original report. |
| [PR 3 / 3849428954](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428954) | Corrected | Qualitative records accept an empty metric name; numeric values still require one. |
| [PR 3 / 3849428960](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428960) | Obsolete mechanism | Do not restore removed runtime rollback dependencies. |
| [PR 3 / 3849428968](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428968) | Corrected | Package and installer use a reviewed distribution file set and exclude local secrets and outputs. |
| [PR 3 / 3849428971](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428971) | Corrected | Unhashable YAML keys become normal constructor validation errors. |
| [PR 3 / 3849428975](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428975) | Corrected | D-07 human-readable and structured records all remain due for recheck. |
| [PR 3 / 3849428976](https://github.com/62656456/ai-film-skills/pull/3#discussion_r3849428976) | Corrected | Successful installation/package publication is separate from leftover-backup cleanup warnings. |
| [PR 4 / 3900452191](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452191) | Corrected | Unknown direct Skill calls are checked beyond the -skill suffix. |
| [PR 4 / 3900452200](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452200) | Corrected | Current catalog and entrance counts match 18 regular + 3 experimental = 21. |
| [PR 4 / 3900452204](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452204) | Corrected | Shell runtime references are checked transitively. |
| [PR 4 / 3900452209](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452209) | Corrected | Negation is scoped to the dependency action. |
| [PR 4 / 3900452216](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452216) | Already resolved | Current implementation already addresses the original report. |
| [PR 4 / 3900452220](https://github.com/62656456/ai-film-skills/pull/4#discussion_r3900452220) | Corrected | Every explicitly requested root must contain an actual Skill. |
| [PR 5 / 3900523657](https://github.com/62656456/ai-film-skills/pull/5#discussion_r3900523657) | Corrected | Pillow 12.3.0 is declared and exercised. |
| [PR 5 / 3900523666](https://github.com/62656456/ai-film-skills/pull/5#discussion_r3900523666) | Corrected | DejaVu Sans 2.37 fonts and license are pinned; old PNGs are preserved. |
| [PR 5 / 3900523668](https://github.com/62656456/ai-film-skills/pull/5#discussion_r3900523668) | Corrected | All current multilingual entry points validate derived counts; historical sections keep original numbers. |
| [PR 5 / 3900523669](https://github.com/62656456/ai-film-skills/pull/5#discussion_r3900523669) | Corrected | The launch manifest must contain the full required asset set without duplicates. |
| [PR 13 / 3901527684](https://github.com/62656456/ai-film-skills/pull/13#discussion_r3901527684) | Corrected | The example actually requests and is refused a handover delay. |
| [PR 13 / 3901527692](https://github.com/62656456/ai-film-skills/pull/13#discussion_r3901527692) | Corrected | The self-audit reflects return after the apartment handover. |
| [PR 13 / 3901527702](https://github.com/62656456/ai-film-skills/pull/13#discussion_r3901527702) | Corrected | A missing example produces a validation error without a traceback. |
| [PR 13 / 3901527713](https://github.com/62656456/ai-film-skills/pull/13#discussion_r3901527713) | Corrected | The pawn-shop journey has a physically consistent timeline. |
| [PR 15 / 3901920570](https://github.com/62656456/ai-film-skills/pull/15#discussion_r3901920570) | Corrected | Four homepage video links use existing static covers; GIF bytes are preserved. |
| [PR 15 / 3901920577](https://github.com/62656456/ai-film-skills/pull/15#discussion_r3901920577) | Corrected | Actual GIF block delays and frame counts are validated. |
| [PR 15 / 3901920582](https://github.com/62656456/ai-film-skills/pull/15#discussion_r3901920582) | Corrected | README cover images must be embedded in their actual video links. |
| [PR 17 / 3941221380](https://github.com/62656456/ai-film-skills/pull/17#discussion_r3941221380) | Old preview only | Current main no longer uses this preview validator/workflow; old branch is preserved as history. |
| [PR 17 / 3941221383](https://github.com/62656456/ai-film-skills/pull/17#discussion_r3941221383) | Old preview only | Current main no longer uses this preview validator/workflow; old branch is preserved as history. |
| [PR 17 / 3941221389](https://github.com/62656456/ai-film-skills/pull/17#discussion_r3941221389) | Corrected | Internal design-state paths cannot be used as screenplay sources. |
| [PR 17 / 3941221392](https://github.com/62656456/ai-film-skills/pull/17#discussion_r3941221392) | Corrected | Selected-scene geometry gates do not include unrelated scenes. |

## Validation and evidence boundary

The maintenance uses regression tests, isolated-package checks, real ZIP content inspection, actual installer checks, media metadata validation and source/installed SHA-256 comparisons. The two font renderers are exercised only with isolated output paths; published artwork is preserved. These checks do not constitute image/video aesthetic acceptance or three accepted real creative tasks.

The previous public v1.3.0 release and separately labeled 5.6 preview retain their original artifacts. The superseded preview branch is not merged into current production. CodeRabbit CLI review was not performed because no compliant installed CLI was available; deterministic tests and repository CI are separate verification evidence, not a substitute claim of CodeRabbit approval.
