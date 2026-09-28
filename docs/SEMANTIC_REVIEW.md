# 两套评审方式：本地检查与可选 Jev

两套方式使用同一导演、分镜和提示词核心。工具只检查给定文本，不创作镜头、不修改文件、不自动淘汰方案，也不证明成片或审美通过。普通创作无需运行它。

| 方式 | 做什么 | 不覆盖什么 |
|---|---|---|
| A：`--mode local` | 输入结构、已声明对白的逐字与说话人一致、对白是否存在于正文、有限数值与时间区间 | 自动提取漏报对白、语义保真、语速、空间美感、模型实际执行 |
| B：`--mode jev --allow-external` | 完成同一套本地检查后，一次批量提交少量锁定要求与实际文本，返回支持／违反／证据不足信号 | 直接看图片、听声音、看视频、全局电影感排名、替用户决定采用 |

## 输入与运行

入口为 `scripts/semantic_review.py`，仅使用 Python 标准库。可运行的虚构示例为 `tests/fixtures/semantic_review.json`。从仓库根运行：

```powershell
python -B scripts/semantic_review.py --mode local --input tests/fixtures/semantic_review.json
```

四个输入字段都必须存在：

- `source`：对象，`text` 是当前源文本；可附 `dialogue` 数组，每项含 `id`、`speaker`、`text`。声明的原文对白必须确实在 source.text 中，工具不自动从自然语言中抽取对白。
- `locked_facts`：最多 12 项本次值得检查的原子要求；每项含 `id`、`text`、`severity`（`major`／`minor`）、`target`。`target` 为 `deliverable` 或某项观察证据的 id。`question_type` 可选 `choice`（默认）或 `noul`。
- `deliverable`：对象，`text` 是实际准备交付的成品；可附 `duration_seconds`、`segments`（每项 `start_seconds`／`end_seconds`）、`dialogue`（`source_id`／`speaker`／`text` 和可选时间对）。原文对白声明必须逐项保留，说话人和标点均按原值检查；成品对白也必须出现在成品正文中。时间检查只核有限数、非负起点、终点晚于起点及不超声明时长；不擅自禁止重叠声音或并行轨道。
- `observed_evidence`：文本观察数组，可以为空；每项为 `id`、`type: "text"`、`text`。观察必须来自实际观察，静帧不能证明动态过程；文件路径、URL、图片、音频、视频和 base64 不会被工具加载或转成观察。

`locked_facts[].excerpt` 可给出目标文本中**只出现一次的原文片段**，用于定位待复核问题。不存在或出现多次的片段会在本地拒绝。文本里的要求是否确实得到用户锁定，仍应由调用方从当前有效来源确认；这个程序不恢复项目身份、不推断批准。

Jev 方式还需要当前进程的 `TYPESAFE_API_KEY`。工具只从这个环境变量读取，不接受命令行密钥、文件内密钥或备用服务，也不创建密钥文件。凭证由现有安全入口注入后才运行：

```powershell
python -B scripts/semantic_review.py --mode jev --allow-external --input tests/fixtures/semantic_review.json
```

不要把密钥粘贴进文档、命令历史或输入 JSON。缺密钥、未给外发开关、接口拒绝或网络失败均返回 `failed`，不会偷偷退回 A 并声称 B 已通过。A 永远不读取密钥、不访问网络。工具不自动重试或跟随 HTTP 重定向，一次运行最多一个请求；请求超本地字节预算时直接拒绝，字节预算不等于精确 token 计数。

## Jev 请求与结果边界

固定 API 为 `POST https://api.typesafe.ai/v1/systemone`，固定模型 `jev-1.13.0`。实际发送源文本、已选锁定要求、对应的成品／观察文本及可选定位片段；只选择与本次检查有关且允许外发的材料。脚本不读取目录中其他项目文件，不把私有输入保存进报告。

每项 Choice 只问一个要求，并明确区分 `yes`／`no`／`insufficient_evidence`。Noul 每项使用两道并行独立问题：现有事实是否足够判断，以及事实是否支持要求；第二题不能看到第一题答案。程序随后组合结果，证据不足不得被当作违反。计划写了什么不是视频已实现的证据。

Choice 使用 confidence 与获选概率均不低于 0.85 的保守复核门槛；Noul 的证据概率至少 0.90，支持概率至少 0.90 或至多 0.10 才属于明确方向。**这些是尚待本任务样本校准的分流策略，不是 85%／90% 准确率，也不是自动验收权限。** 独立问题可能相互不一致，接口正确不保证判断正确。

输出只包含 schema、provider、status、检查位置、问题索引、概率、耗时、实际模型、token usage 和请求 SHA256 等信息，不复述完整私有输入、原文片段、密钥或服务错误正文。`latency_seconds` 是本检查器从校验到返回的耗时，`request_latency_seconds` 是包含网络与返回读取的一次请求耗时；都不包含主模型创作和后续修复。`character_range` 是目标字符串内从 0 起算的 Unicode 字符区间，末端不包含在内。需要看到上下文时由调用方在原输入中定位。

| status | 意义 | 退出码 |
|---|---|---|
| `local_checks_passed` | A 的已声明确定性检查通过，未进行语义评审 | 0 |
| `no_issue_detected` | B 本次文本问题未发现明确问题；不是审美通过 | 0 |
| `review_required` | 低置信度、证据不足、无语义问题、轻微或未能具体定位的问题 | 2 |
| `candidate_repair` | 至少一个高方向确定性的 major 违反，且有本地确认存在的唯一片段；仅为候选修复信号 | 2 |
| `failed` | 输入、本地检查、凭证、网络、拒绝或返回结构失败 | 1 |

多个问题混合时，顶层优先显示 `candidate_repair`，仍须逐项查看 `findings` 中其他 `review_required`，不能把它们当成已通过。任何修改都由主创作流程结合原文复核，工具自身不写成品。工具只校验模型返回的类型与概率合法性；不能靠模型解释补造证据，也不把任何分数变成镜头审美排名。

## 两套方式怎样公平比较

固定同一核心版本、源文本、资产、初稿和修订上限。A 使用当前主模型按合同自检，B 在同一自检之外加 Jev；本脚本的 local 模式只承担 A 中可确定的程序检查。B 不能额外获得 A 未见的图像观察、导演理由或预期答案。

冻结包含正确、遗漏、冲突、合法静止、正反打、缺证据及局部修订的样本；比较实际找到的问题、误报、未知保留、修订后旁支破坏、总耗时和总成本。端到端耗时应包含主模型复核和修复；API 往返时间不能冒充全流程速度。允许无收益、平局与分歧，不用 Jev 给自己的结果打分证明 B 更好。

现有 2026-09-22 本地三轮实测仅证明有限条件判断：第二轮明确目标下选择较稳定，但 R16 把 `unknown` 误判为 `none`；第三轮只问“哪个最有镜头感”，同组三份中性观察换序后首选不一致，confidence 约 0.35–0.39。Jev 接收的是观察文字，未直接看图；不能据此自动淘汰或宣称镜头感提高。

离线测试入口：

```powershell
python -B -m unittest discover -s tests -p test_semantic_review.py
```

测试使用 fake transport 覆盖无密钥、未允许外发、API 错误、拒绝、未知、低置信度、Noul 证据门、输入图片、时序、对白与隐私输出。它们不调用真实服务，不证明当前 API 可用或中文语义可靠。真实小样本对照前还需要：有效凭证、已允许发送的具体样本、明确调用预算及预先冻结的人工参照；随后才能报告实际费用和效果。没有这些条件时，A 与 B 的代码和离线检查仍可完整交付。

## 官方依据（2026-09-28 实际查阅）

- [文档索引](https://docs.typesafe.ai/llms.txt)、[HTTP API](https://docs.typesafe.ai/api)：state 与独立 typed questions、返回 schema。
- [模型说明](https://docs.typesafe.ai/models)：当前 `jev-1.13.0`、纯文本输入、$0.042／百万输入 token、输出免费。价格及模型需在未来真实使用前复核；本工具不读取账单。
- [State](https://docs.typesafe.ai/concepts/state)、[已知弱项](https://docs.typesafe.ai/model-jaggedness/jev-1.13)：中文/CJK、长无关上下文、对抗输入、计数和复杂推理的限制。
- [语义核对案例](https://docs.typesafe.ai/cookbooks/citation_check)：确定性定位与窄语义核对分别处理；示例阈值不直接用作本项目准确率或验收标准。
