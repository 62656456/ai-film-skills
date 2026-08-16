# produce-ai-video｜合格成片生产

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 完整生产与验收合同；宿主工具和权限齐全时，可交付真实审核后的最终视频。 |
| 单独不能声称 | 只安装 Skill 不会自动获得模型、额度、版权、剪辑工具或合格成片。 |

[运行正文 `SKILL.md`](../../../skills/produce-ai-video/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

通过导演、分镜、生成、剪辑、声音、完整回放和修复，把批准剧本或片段做成合格可观看 AI 成片。

<!-- contract:principles -->
## 2. 设计理念

- 最终可观看视频才是结果；提示词、片段、剪辑工程和 QC 报告只是中间产物。
- 保留锁定源事实，审核完整最终渲染，不用漂亮单帧代替。
- 修复观众最早失去信任的位置，并严格区分候选成片和合格成片。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

完整生产与验收合同；宿主工具和权限齐全时，可交付真实审核后的最终视频。

**单独不能声称:** 只安装 Skill 不会自动获得模型、额度、版权、剪辑工具或合格成片。

<!-- contract:inputs -->
## 4. 输入

- 当前批准剧本、资产、视觉规则、决定、检查点、交付格式和合格定义。
- 付费生成、外部服务、音乐、声音、发布等重要动作的明确权限。
- 在自主生产与用户直接导演模式之间明确选择，尤其已有锁定分镜或结构时。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 锁定来源、验收、权限与模式；理解剧本并完成导演判断。
2. 设计镜头组，并使用 `ai-storyboard-director` 完成下游分镜与提示词合同。
3. 选择生成路线，产生真实运动，完成剪辑、声音和最终文件渲染。
4. 至少完整观看两遍：一遍看故事与情绪，一遍看技术与连续性。
5. 修复阻塞问题，并以“合格成片 / 候选成片 / 未完成或待验证”诚实交付。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 退回最早错误层：剧本/导演、分镜、提示词、源片段、剪辑、声音或最终渲染。
- 平台任务成功、时长正确或单帧好看都不能绕过完整回放审核。
- 用户锁定的分镜保持不变，除非明确授权修改。

<!-- contract:review -->
## 7. 审核门

- [ ] 故事、镜头、空间与资产连续性、生成质量、剪辑、声音和交付通过适用硬门。
- [ ] 真实最终文件可打开并已从头看到尾，没有用其他文件代替审核。
- [ ] 版权、费用、权限和未解决边界明确。

<!-- contract:pass -->
## 8. 过关标准与状态

- 只有完整观看并通过全部适用硬门的渲染文件，才能叫合格成片。
- 即使文件和工程存在，缺关键审核门也只能是候选或未完成。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 真实可播放的最终视频、精确状态和交付入口。
- 必要的中间产物，以及审核、修复、权利和剩余边界的简明记录。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 安装本方法不会自动获得视频模型、付费额度、音乐权、声音权或发布权。
- 不把分镜、提示词、生成片段、剪辑时间线或未审渲染冒充成片。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 真实生产需要媒体生成、剪辑、声音、文件能力、足够权限或预算以及完整回放；纯文本宿主只能读方法，不能声称成片。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/produce-ai-video/agents/openai.yaml)
- [`SKILL.md`](../../../skills/produce-ai-video/SKILL.md)

**引用资料**

- [`references/autonomous-production-workflow.md`](../../../skills/produce-ai-video/references/autonomous-production-workflow.md)
- [`references/qualified-video-acceptance.md`](../../../skills/produce-ai-video/references/qualified-video-acceptance.md)
