# ai-short-drama-production｜AI短剧控制合同

| 状态 | 已打包；未部署 |
|---|---|
| 单独可交付 | 针对已有决定的生产控制编排与缺口审计，也可单独交付六类控制合同中的任意一类。 |
| 单独不能声称 | 不会在一个文件夹里复制导演、资产、类型、生成和 QC 的全部能力。 |

[运行正文 `SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

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

**单独不能声称:** 不会在一个文件夹里复制导演、资产、类型、生成和 QC 的全部能力。

<!-- contract:inputs -->
## 4. 输入

- 受众、时长、剧本形态、人物目标与阻力、场景、主类型、目标平台和已有资产/草图。
- 已有批准的导演判断和资产版本；缺失值标 `pending`，推断值标 `assumed`。
- 点名控制缺口：节拍、资产索引、调度、布光、动作、草图转镜头或生成前 QC。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 取得现行导演与节拍决定，不用通用公式重做。
2. 建立或引用经人审的 Cxx/Sxx/Pxx 资产及版本。
3. 按需建立调度、布光、动作和草图转镜头控制合同。
4. 把合同装入一个连续机位 AG-CLIP，控制动作密度并留下可接续尾帧。
5. 审核实际画面，只有八项生成前门全部通过才输出 `ready_for_prompt`。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 故事、概念、节拍或台词退回导演/编剧层；资产漂移退回资产层。
- 空间、轴线或动作退回分镜控制；字段编译退回提示词；实际画面不符退回 QC。
- 本模块负责路由失败，绝不把“再生成一次”当诊断。

<!-- contract:review -->
## 7. 审核门

- [ ] 钩子、目标、阻力、信息差、权力转折、代价和结尾钩子可观察，不是形容词。
- [ ] 资产版本均经人审；调度能解释人物、道具、摄影机与轴线；布光有来源；动作有起点、路径、终点和反应。
- [ ] 每段无隐藏硬切，台词时序与动作密度成立，并以连续尾帧接下一镜。

<!-- contract:pass -->
## 8. 过关标准与状态

- 八项 `ready_for_prompt` 条件全部通过，合同编号可追溯，并完成所需真实画面审核。
- 该状态只表示控制任务可进入提示词生产，不是片段或成片通过。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 按需交付节拍合同、资产索引、调度图、布光图、动作账本或草图转镜头说明。
- 可追溯的 `ready_for_prompt` 包，或按责任层分类的回炉记录。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 它可以单独整理已批准决定或审计控制缺口，但不会复制导演、资产、类型、生成和 QC 的全部能力。
- 从零完成全流程仍需要相应专业 Skill 和宿主工具。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 合同设计依赖文本/文件；完整编排需要相关专业 Skill，真实画面审核和生成还需媒体工具与权限。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/ai-short-drama-production/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md)

**引用资料**

- [`references/control-contracts.md`](../../../skills/ai-short-drama-production/references/control-contracts.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/ai-short-drama-production/references/SOURCE-LEDGER.md)
