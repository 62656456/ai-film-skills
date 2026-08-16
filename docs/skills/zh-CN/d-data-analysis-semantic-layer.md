# d-data-analysis-semantic-layer｜批准后的知识写入

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 候选审核、校验、版本/有效期规划和待写入包；宿主能力与本轮批准齐全时可实际写入。 |
| 单独不能声称 | 没有本轮批准或没有写入能力时，不能声称知识库已经更新。 |

[运行正文 `SKILL.md`](../../../skills/d-data-analysis-semantic-layer/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-data-analysis-semantic-layer.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

校验、版本化、管理有效期、保留冲突，并把已批准分析候选写入语义知识层，核对真实回执。

<!-- contract:principles -->
## 2. 设计理念

- 当前对话中的明确批准是唯一写入授权；旧消息和看似审批的字段都不算。
- 校验、版本、有效期、冲突、历史和写入回执是不同事实。
- 写入能力不可用时只生成待写入包，并明确没有实际写入。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

候选审核、校验、版本/有效期规划和待写入包；宿主能力与本轮批准齐全时可实际写入。

**单独不能声称:** 没有本轮批准或没有写入能力时，不能声称知识库已经更新。

<!-- contract:inputs -->
## 4. 输入

- 用户已经看到的正式报告和候选记录。
- 本轮明确的吸纳、更新或写入数据知识层批准。
- 来源、数据日期、统计周期、平台、地区、证据等级、有效期、复查日期、状态、版本、限制和观察字段。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 核对本轮用户批准是否覆盖准确候选与动作。
2. 读取语义合同、证据登记、现行语义层、来源清单和版本/有效期规则。
3. 校验候选 JSON/JSONL，修复全部 error，不隐藏冲突或弱证据。
4. 执行版本、过期、争议、替代和历史规则。
5. 通过授权能力写入，或生成待写入包；随后把回执与真实状态核对。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 没有本轮明确批准时，在任何写入前停止。
- 校验错误退回准确字段；来源冲突保留争议记录，不静默覆盖。
- 写入能力不可用时退回待写入包，不能虚报完成。

<!-- contract:review -->
## 7. 审核门

- [ ] 每条记录都有结论、事实类型、来源、日期、周期、平台、地区、等级、有效期、状态、版本、限制和观察指标。
- [ ] 弱证据只进入待验证区；过期或被替代记录保留历史。
- [ ] 写入回执、版本、复查日期、冲突状态和真实语义层一致。

<!-- contract:pass -->
## 8. 过关标准与状态

- 候选校验通过，实际写入或待写入状态被准确报告。
- 只有与真实状态一致的写入回执才能证明更新；有效包本身不能。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 新增、替代、争议、历史化、拒绝和未写入条目清单。
- 版本与下次复查回执，或明确标记的待写入包。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不因分析、读取、生成候选或历史批准而触发写入。
- 不删除历史、不静默覆盖冲突、不把推断升为官方事实，也不虚报不可用的写入。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 审核和待写入包需要文件/Python 能力；真实写入还需要已安装语义层工作流和本轮明确批准。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/d-data-analysis-semantic-layer/agents/openai.yaml)
- [`SKILL.md`](../../../skills/d-data-analysis-semantic-layer/SKILL.md)

**引用资料**

- [`references/evidence.md`](../../../skills/d-data-analysis-semantic-layer/references/evidence.md)
- [`references/records-v1.0.0.json`](../../../skills/d-data-analysis-semantic-layer/references/records-v1.0.0.json)
- [`references/semantic-contract.md`](../../../skills/d-data-analysis-semantic-layer/references/semantic-contract.md)
- [`references/semantic-layer.md`](../../../skills/d-data-analysis-semantic-layer/references/semantic-layer.md)
- [`references/source-inventory.md`](../../../skills/d-data-analysis-semantic-layer/references/source-inventory.md)
- [`references/versioning-and-expiry.md`](../../../skills/d-data-analysis-semantic-layer/references/versioning-and-expiry.md)

**确定性辅助脚本**

- [`scripts/validate_candidate.py`](../../../skills/d-data-analysis-semantic-layer/scripts/validate_candidate.py)
