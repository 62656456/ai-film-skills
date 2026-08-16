# hard-sci-fi-visual-director｜证据化硬科幻视觉设计

| 状态 | 实验；未部署；用户视觉审核待完成 |
|---|---|
| 单独可交付 | 针对明确场景或资产的研究驱动视觉诊断、推导、圣经、导演方案和可复制提示词包。 |
| 单独不能声称 | 仍是实验模块，不能声称已部署、实战稳定、生成成功或用户视觉通过。 |

[运行正文 `SKILL.md`](../../../experimental/hard-sci-fi-visual-director/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/hard-sci-fi-visual-director.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

从剧本事实、证据、物理、制作和连续性推导原创硬科幻世界、系统、生物、设备、界面、摄影机和提示词。

<!-- contract:principles -->
## 2. 设计理念

- 方法固定，但每个项目的视觉身份必须从原文事实、证据、物理、制作和叙事可读性推导。
- 剧本事实、必要外推、提案、批准决定和锁定决定保持不同状态。
- 研究设证据底线，不设创意上限；高振幅设计必须暴露推测规则与代价。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

针对明确场景或资产的研究驱动视觉诊断、推导、圣经、导演方案和可复制提示词包。

**单独不能声称:** 仍是实验模块，不能声称已部署、实战稳定、生成成功或用户视觉通过。

<!-- contract:inputs -->
## 4. 输入

- 当前剧本/场景、批准世界圣经、明确前提、已有视觉资产或提示词，以及点名模式。
- 必须保留事实、禁止改写项、开放身份决定和每个既有选择的权限状态。
- 点名媒介与功能：世界、环境、界面、生物、机器、普通设备、防御/救援系统或连续性。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 建立来源权威、保护剧情拍点并选择适用功能合同。
2. 提出研究问题、打开证据并区分事实、外推、假设和未知。
3. 推导物理边界、世界/环境系统；只为开放决定提出候选路线，并建立空间模型。
4. 从功能与历史推导身体/系统、制作路线、摄影机、色彩、界面、家族语法和连续性。
5. 生成完整提示词和场景专项负向，执行适用通用/条件门，只在权限明确后生成。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 审核门失败退回对应的来源、研究、物理、世界、系统、摄影机、色彩、界面或连续性推导阶段。
- 锁定身份不能被视觉迭代擅自重开；开放决定可以获得真正不同的候选。
- 该实验模块有设计回炉，但没有已登记的版本回滚清单。

<!-- contract:review -->
## 7. 审核门

- [ ] 所有适用通用门保护原文事实、剧情可读性、证据边界、原创性、物理关系、制作路线、摄影机、色彩、界面和连续性。
- [ ] 按实际功能检查生态、生物、机械、设备、防御/救援系统或界面拓扑的内部一致。
- [ ] 排除在世创作者模仿、既有 IP 默认、装饰性科技和可操作武器制造细节。

<!-- contract:pass -->
## 8. 过关标准与状态

- 适用审核门通过，输出明确事实、推断、候选、批准、锁定、未知、已生成和用户审核状态。
- 内部通过或生成文件都不能把该实验模块升级为已部署、稳定或用户通过。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 来源与空白卡、证据化推导、候选/决定记录、视觉或资产圣经、导演方案、完整提示词、负向和状态审计。
- 诊断模式输出“可见失败 → 来源/物理/摄影机/设计原因 → 一个修正”的简明链。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不复制受保护 IP、不模仿在世创作者、不提供可操作武器制造，也不在无授权时生成。
- 这是实验模块而非已部署模块；大量研究和内部检查不等于用户视觉通过。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 文本诊断与提示词可在阅读宿主使用；证据敏感任务需联网，连续性需文件，生图需授权媒体工具和用户视觉审核。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../experimental/hard-sci-fi-visual-director/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/hard-sci-fi-visual-director/SKILL.md)

**引用资料**

- [`references/aesthetic-audit.md`](../../../experimental/hard-sci-fi-visual-director/references/aesthetic-audit.md)
- [`references/future-interface-systems.md`](../../../experimental/hard-sci-fi-visual-director/references/future-interface-systems.md)
- [`references/future-weapon-systems.md`](../../../experimental/hard-sci-fi-visual-director/references/future-weapon-systems.md)
- [`references/inspiration-engine.md`](../../../experimental/hard-sci-fi-visual-director/references/inspiration-engine.md)
- [`references/live-action-cinematography.md`](../../../experimental/hard-sci-fi-visual-director/references/live-action-cinematography.md)
- [`references/mecha-and-megafauna.md`](../../../experimental/hard-sci-fi-visual-director/references/mecha-and-megafauna.md)
- [`references/organism-and-ecology.md`](../../../experimental/hard-sci-fi-visual-director/references/organism-and-ecology.md)
- [`references/physics-and-engineering.md`](../../../experimental/hard-sci-fi-visual-director/references/physics-and-engineering.md)
- [`references/production-design.md`](../../../experimental/hard-sci-fi-visual-director/references/production-design.md)
- [`references/prompt-examples.md`](../../../experimental/hard-sci-fi-visual-director/references/prompt-examples.md)
- [`references/scene-routes.md`](../../../experimental/hard-sci-fi-visual-director/references/scene-routes.md)
- [`references/scene-world-design.md`](../../../experimental/hard-sci-fi-visual-director/references/scene-world-design.md)
- [`references/script-to-visual-derivation.md`](../../../experimental/hard-sci-fi-visual-director/references/script-to-visual-derivation.md)
- [`references/style-color-system.md`](../../../experimental/hard-sci-fi-visual-director/references/style-color-system.md)
- [`references/visual-continuity.md`](../../../experimental/hard-sci-fi-visual-director/references/visual-continuity.md)
