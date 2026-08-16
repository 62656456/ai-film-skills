# director-agent｜剧本与导演设计

| 状态 | 已部署；长期实战证据单独记录 |
|---|---|
| 单独可交付 | 剧本、替换段落、诊断、导演方案、工作台或分镜前导演设计稿。 |
| 单独不能声称 | 不能单独交付完整生产分镜、真实生成媒体或用户接受证明。 |

[运行正文 `SKILL.md`](../../../skills/director-agent/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

创作、修改或诊断剧本，并完成进入完整分镜前必须成立的导演判断。

<!-- contract:principles -->
## 2. 设计理念

- 先用人物行动和因果把故事讲清楚，再使用状态引擎、检查表和视觉润色。
- 每个导演决定都必须落到观众效果、剧情功能、演员动作或物理画面。
- 独立冷读审核真实剧本，但不能替代写作，也不能保证审美接受。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

剧本、替换段落、诊断、导演方案、工作台或分镜前导演设计稿。

**单独不能声称:** 不能单独交付完整生产分镜、真实生成媒体或用户接受证明。

<!-- contract:inputs -->
## 4. 输入

- 剧本、故事、梗概、纯对白、小说段落或抽象材料，以及点名的工作模式。
- 已锁定事实、格式、长度、受众、生产约束，以及已批准或禁止的决定。
- 未知故事事实保持为假设，不能静默补成设定。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 只加载与当前任务有关的写作和导演引用。
2. 按故事、人物、导演三层读材料，核对刺激、目标、策略、状态变化和对白回应。
3. 选择创作、诊断、导演方案、工作台或分镜前设计模式。
4. 从因果判断生成视觉概念、表演动作、声音、时间、剪辑、主题和潜台词。
5. 冷读真实产物，修复最早的上游断裂，并优先交付用户点名的可读成品。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 因果、人物知识或场景目的失败时，先退回最早断裂的场景，不先润色台词或视觉。
- 若任务实际需要完整生产分镜，把已批准的导演判断交给 `ai-storyboard-director`，不让本模块越界。
- 冷读 PASS 只是剧本审阅状态，不是用户喜欢或采用的证明。

<!-- contract:review -->
## 7. 审核门

- [ ] 每个关键动作和台词都有前置刺激、目的、策略、对方影响和状态变化。
- [ ] 主角不会为了制造冲突而无理由忽略明显更安全、更容易的选择。
- [ ] 场景把变化后的状态交给下一场；铺垫与回收会改变意义、权力、可能性、选择或结果。

<!-- contract:pass -->
## 8. 过关标准与状态

- 点名的剧本、诊断、导演方案、工作台或分镜前稿无需隐藏解释即可使用。
- 最早的阻塞级故事问题已修复，或被明确标为未解决边界。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 可直接阅读的完整剧本或替换段落；用户要正文时不能只交大纲。
- 按任务交付导演方案、工作台、诊断或分镜前导演设计稿。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不编造影史、引用、导演方法或缺失的故事事实。
- 不把导演分析冒充完整分镜，也不把冷读通过冒充用户接受。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 只要宿主能读取完整文件夹即可做文本创作与诊断；涉及当前事实或来源敏感内容时，需要联网与引用能力。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/director-agent/agents/openai.yaml)
- [`SKILL.md`](../../../skills/director-agent/SKILL.md)

**引用资料**

- [`references/anti-laziness-contract.md`](../../../skills/director-agent/references/anti-laziness-contract.md)
- [`references/director-thinking-spine.md`](../../../skills/director-agent/references/director-thinking-spine.md)
- [`references/director-workbench-protocol.md`](../../../skills/director-agent/references/director-workbench-protocol.md)
- [`references/github-project-watchlist.md`](../../../skills/director-agent/references/github-project-watchlist.md)
- [`references/local-knowledge-map.md`](../../../skills/director-agent/references/local-knowledge-map.md)
- [`references/research-update-protocol.md`](../../../skills/director-agent/references/research-update-protocol.md)
- [`references/screenplay-cold-read-protocol.md`](../../../skills/director-agent/references/screenplay-cold-read-protocol.md)
- [`references/screenplay-exemplar-benchmarks.md`](../../../skills/director-agent/references/screenplay-exemplar-benchmarks.md)
- [`references/screenplay-state-engine.md`](../../../skills/director-agent/references/screenplay-state-engine.md)
- [`references/screenplay-writing-core.md`](../../../skills/director-agent/references/screenplay-writing-core.md)
- [`references/verified-director-logic.md`](../../../skills/director-agent/references/verified-director-logic.md)
