# ai-short-drama-production｜AI短剧控制合同

| 状态 | 已打包；未部署 |
|---|---|
| 单独可交付 | 针对已有决定的生产控制编排与缺口审计，也可单独交付六类控制合同中的任意一类。 |
| 单独不能声称 | 不需要配套技能包：导演、资产、类型、提示词和 QC 规则均按短剧用途重写为本地模块；真实图片和视频生成仍需要宿主媒体工具与权限。 |

[运行正文 `SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md) · [v1.3.0 历史 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-short-drama-production.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

v1.3.0历史快照；已更新模块与当前源码不同。

<!-- contract:purpose -->
## 1. 设计目的

把批准的创作决定编排为可追溯的节拍、资产、调度、布光、动作、草图、提示词和 QC 控制合同。

<!-- contract:principles -->
## 2. 设计理念

- 这是控制合同层，把批准的导演、资产、视觉、分镜、提示词和 QC 接起来，但不替代专业模块。
- 每个假设、版本、调度图、光源、动作状态和尾帧都可追溯。
- 是否就绪由实际画面 QC 决定，不能靠盲目再生成。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

针对已有决定的生产控制编排与缺口审计，也可单独交付六类控制合同中的任意一类。

**单独不能声称:** 不需要配套技能包：导演、资产、类型、提示词和 QC 规则均按短剧用途重写为本地模块；真实图片和视频生成仍需要宿主媒体工具与权限。

<!-- contract:inputs -->
## 4. 输入

- 受众、时长、剧本形态、人物目标与阻力、场景、主类型、目标平台和已有资产/草图。
- 已有批准的导演判断和资产版本；缺失值标 `pending`，推断值标 `assumed`。
- 点名控制缺口：节拍、资产索引、调度、布光、动作、草图转镜头或生成前 QC。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 取得现行导演与节拍决定，不用通用公式重做。
2. 沿用批准资产；未定资产可标候选支持文本设计，正式生成前完成相应审阅。
3. 按需建立调度、布光、动作和草图转镜头控制合同。
4. 编译五列分镜与覆盖点名总时长的一条六模块母提示词，保留锁定格式、切点、摄影路径、对白和时长。
5. 区分文本自洽的 ready_for_prompt 与资产审阅、执行条件齐全的 ready_for_generation；生成后再检查真实媒体。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 故事、概念、节拍或台词退回导演/编剧层；资产漂移退回资产层。
- 空间、轴线或动作退回分镜控制；字段编译退回提示词；实际画面不符退回 QC。
- 本模块负责路由失败，绝不把“再生成一次”当诊断。

<!-- contract:review -->
## 7. 审核门

- [ ] 钩子、目标、阻力、信息差、权力转折、代价和结尾钩子可观察，不是形容词。
- [ ] 批准与候选资产状态分明；调度能解释世界空间及每个机位投影；光有实体来源，动作有起点、路径、终点和反应。
- [ ] 切镜或连续长镜明确、锁定结构不变、台词时间成立，最终提示词保留已选摄影与尾态连续性。

<!-- contract:pass -->
## 8. 过关标准与状态

- 点名产物完整，最终正文可还原时序、动作、摄影与用户锁定；六模块内十类信息齐全。
- 文本就绪、生成就绪、真实视频检查与用户接受分别记录。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 按需交付节拍合同、资产索引、调度图、布光图、动作账本或草图转镜头说明。
- 交付点名控制合同、五列分镜或完整六模块提示词；编号留在内部记录，用户提示词使用自然名称。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 它可以单独整理已批准决定或审计控制缺口，但不会复制导演、资产、类型、生成和 QC 的全部能力。
- 本包自带与5.6分镜格式对齐的交付合同，不引入其状态程序；源码对齐不代表部署或真实视频验收。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 文本设计使用本包规则及交付合同；实际生成、播放审核与剪辑需要宿主媒体能力、相应授权与已核实平台限制。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/ai-short-drama-production/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md)

**引用资料**

- [`references/control-contracts.md`](../../../skills/ai-short-drama-production/references/control-contracts.md)
- [`references/independent-production-core.md`](../../../skills/ai-short-drama-production/references/independent-production-core.md)
- [`references/production-handoff.md`](../../../skills/ai-short-drama-production/references/production-handoff.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/ai-short-drama-production/references/SOURCE-LEDGER.md)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
