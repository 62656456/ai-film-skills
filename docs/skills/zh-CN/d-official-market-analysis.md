# d-official-market-analysis｜官方影视市场研究

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 来源计划、校验数据集、证据表、分析报告和单独标记的知识候选。 |
| 单独不能声称 | 离线时不能补造当前市场事实，报告完成也不授权语义层写入。 |

[运行正文 `SKILL.md`](../../../skills/d-official-market-analysis/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-official-market-analysis.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

围绕明确决策，用当前官方与权威证据研究影视、短剧、动画、AI影视及相邻市场。

<!-- contract:principles -->
## 2. 设计理念

- 只说当前公开可验证证据能支持的结论，推断与官方事实分开。
- 每个结论都携带数据日期、统计周期、地区、平台、口径和来源等级。
- 报告可以生成知识候选，但只有后续明确批准才能授权语义层写入。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

来源计划、校验数据集、证据表、分析报告和单独标记的知识候选。

**单独不能声称:** 离线时不能补造当前市场事实，报告完成也不授权语义层写入。

<!-- contract:inputs -->
## 4. 输入

- 研究日期、地区、平台、内容类型、决策用途、预算、团队和限制。
- 指标与比较口径，包括榜单值或热度值不能推导什么。
- 需要当前一手或权威来源；否则只能交研究框架和来源缺口。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 规划来源并实际打开一手或权威证据。
2. 建立数据合同、清洗记录、执行质量检查并保留口径与缺失。
3. 比较周期与分区、检查反例，并区分事实、计算、推断和未知。
4. 按固定章节输出报告、证据表和决策影响。
5. 只生成知识候选；批准写入必须走独立语义层 Skill。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 缺当前证据退回采集，口径冲突退回数据合同，校验错误退回清洗或计算。
- warning 保持为证据边界，不能为了强结论而消失。
- 没有明确批准就不写知识层，即使候选已经完整。

<!-- contract:review -->
## 7. 审核门

- [ ] 来源已实际打开、与结论匹配、有日期和链接；读不到时明确标记，不靠记忆重构。
- [ ] 指标口径、清洗、计算、样本边界、反证、时效与未知可见。
- [ ] 图表和结论不把热度、排名、营销文案或单例冒充销售、播放、市场规模或成功率。

<!-- contract:pass -->
## 8. 过关标准与状态

- 报告通过结构与证据检查，每个结论标明事实类型和强度。
- 有限证据按有限报告；报告完成不代表结论永久有效或得到官方背书。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 包含范围、方法、证据表、发现、反证、决策影响和边界的来源化市场报告。
- 单独标记的语义层候选，绝不自动写入。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不把搜索摘要、营销页、不可核截图或仓库旧数据当当前官方证据。
- 不把推断变成官方事实，也不在无明确批准时写入语义层。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 当前市场分析需要联网/连接器访问一手来源，并用 Python/文件能力校验数据；离线只能设计研究和列缺口，不能补造当前结论。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/d-official-market-analysis/agents/openai.yaml)
- [`SKILL.md`](../../../skills/d-official-market-analysis/SKILL.md)

**引用资料**

- [`references/analysis-and-report.md`](../../../skills/d-official-market-analysis/references/analysis-and-report.md)
- [`references/connector-contract.md`](../../../skills/d-official-market-analysis/references/connector-contract.md)
- [`references/data-contract.md`](../../../skills/d-official-market-analysis/references/data-contract.md)
- [`references/evidence-and-sources.md`](../../../skills/d-official-market-analysis/references/evidence-and-sources.md)
- [`references/platform-metrics.md`](../../../skills/d-official-market-analysis/references/platform-metrics.md)

**确定性辅助脚本**

- [`scripts/validate_dataset.py`](../../../skills/d-official-market-analysis/scripts/validate_dataset.py)
