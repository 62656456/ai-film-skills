# AI Storyboard Director 5.6.0 Preview — 独立测试更新

**日常继续使用5.4.4；5.6.0-rc.1是独立测试候选，不覆盖主版，也不设为Latest。是否采用新版，等待实际制作检验与使用者明确决定。**

本次针对分镜在长对话、局部修改和新上下文续接时容易丢掉导演意图、已选镜头和人物道具状态的问题，加入作品内的实际保存与局部恢复，并补充构图和180度轴线的判断方法。程序会检查版本冲突、源变化、场景遗漏、明确状态断裂、时间缺口和固定二维轴的机位错误。

它不保证模型永不遗忘，不替代导演审美判断，也不证明视频模型一定能执行镜头。

## 下载与隔离使用

- 下载下方 **ai-storyboard-director-preview-5.6.0-rc.1.zip**；校验值见 **SHA256SUMS.txt**。
- 解压后将 **ai-storyboard-director-preview** 文件夹单独安装，与日常 **ai-storyboard-director** 并列。不要改名覆盖主版。
- 使用作品副本，在支持Skill、本地文件和Python的助手中明确调用 `$ai-storyboard-director-preview`。支持该策略的宿主将禁用自动调用；其他环境也应手动选用测试包。
- 运行程序仅使用Python标准库，不联网、不调用模型、不要求购买额外API。建议Python 3.12或更新版本；视频制作沿用自己的常用流程。

[完整中英说明](https://github.com/62656456/ai-film-skills/blob/ai-storyboard-director-v5.6.0-rc.1/previews/ai-storyboard-director-preview/README.md) · [可复现测试](https://github.com/62656456/ai-film-skills/tree/ai-storyboard-director-v5.6.0-rc.1/previews/tests) · [提交反馈](https://github.com/62656456/ai-film-skills/issues/new)

## 希望你实际测试

用准备制作的真实剧本完成分镜与提示词，经过几轮局部修改后，换新对话从同一作品副本恢复并继续。观察未点名镜头是否被改写、最新要求是否生效、动作与人物关系是否清楚。再按日常流程制作一段可观看视频，逐镜检查构图、运镜、动作和剪辑是否成立；方便时与5.4.4使用同一输入对照。

反馈标题请注明 **5.6 Preview**，并写明：

1. 助手环境、版本与片段长度。
2. 是否已实际制作，具体成功或失败的镜头/时间点。
3. 修改轮次、是否换对话，以及恢复时保留或遗漏的内容。
4. 一次局部修改的原要求与实际结果。
5. 与主版比较后愿意采用哪份方案，最应先修的问题。

只分享愿意公开且有权分享的材料；没有制作视频也请直接注明。

## 当前证据

公开副本包含9个运行文件、19处引用闭合；改名隔离后24项程序测试重新通过。此前一个新造文本用例完成了两个独立上下文的18秒与8秒设计续接，第一段场景数据保持不变。

这些证据覆盖程序和一个文本用例。长篇多轮稳定性、摄影审美提升、真实视频效果和用户实际制作接受仍未验证，CI通过或上传成功不等于采用新版。

---

## English

**5.4.4 remains the daily version. 5.6.0-rc.1 is an explicit-only preview, not a replacement or the Latest release.** Adoption depends on real production testing and an explicit user decision.

The preview saves directing intent, chosen shots with brief rationales, locked facts, and scene states inside a selected project folder. Scene-focused recovery reduces reliance on conversation summaries. Framing and axis guidance supports design, while the standard-library runtime checks source drift, stale writes, missing scenes, explicit continuity errors, timing gaps, and fixed 2D camera-axis constraints.

Download the preview ZIP and install the folder named **ai-storyboard-director-preview** beside the main Skill. Do not rename or overwrite the daily folder. Explicitly invoke `$ai-storyboard-director-preview` in a project copy. Use an assistant with Skill support, local file access, and Python, preferably 3.12 or newer. The runtime makes no network/model calls and requires no separate API purchase.

Please test real storyboarding, focused revisions, fresh-conversation continuation, and an actual watchable clip through your usual workflow. Compare against the daily version on the same scene if practical. Report the environment, production result and timestamps, continuation behavior, one requested-versus-actual revision, and which result you would keep.

The renamed package passed 24 program tests and isolated bundle validation. One original text scenario previously completed continuation across two fresh contexts without changing the first segment. These results do not establish perfect memory, better cinematography, long-project reliability, or successful video generation. Both concrete successes and failures are welcome in Issues titled **5.6 Preview**.
