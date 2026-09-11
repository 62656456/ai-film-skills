# war-design｜战争电影视觉顾问（合并版）

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 类型参数、军事视觉顾问设计、完整图像提示词、实际图片，以及已定镜头的战争视觉与声音补充。 |
| 单独不能声称 | 合并与安装不能替代新的图像、视频或用户审美验收，也不认证真实战术和装备性能。 |

[运行正文 `SKILL.md`](../../../skills/war-design/SKILL.md) · [v1.3.0 历史 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/war-design.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

v1.3.0历史快照；已更新模块与当前源码不同。

<!-- contract:purpose -->
## 1. 设计目的

统一战争类型光色空间、军事服装装备、场景道具、故事战斗、小队摄影和实际画面审查；内部名继续为war-design。

<!-- contract:principles -->
## 2. 设计理念

- 先判断本次要类型参数、资产、故事还是镜头补充，再选择必要规则；纯空景不强加人物。
- 保留用户锁定，参数是可选设计，原图观察、来源声明和创作推断分开。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

类型参数、军事视觉顾问设计、完整图像提示词、实际图片，以及已定镜头的战争视觉与声音补充。

**单独不能声称:** 合并与安装不能替代新的图像、视频或用户审美验收，也不认证真实战术和装备性能。

<!-- contract:inputs -->
## 4. 输入

- 目标媒介、故事或对象、已锁定人物/空间/风格，以及本次需要的参考。
- 只在当前输出需要时补时长、平台和已有声音；未确认的型号和日期不猜。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 按任务选择纯参数、人物、场景、道具、故事、战斗或小队模式。
2. 建立注意力、空间与材料关系；类型色表与镜头起点按需采用。
3. 故事任务补人物目标、阻碍与可见证据；纯资产保持原交付范围。
4. 核对实际请求内的角色、装备、动作方向和参考用途；自然名称用于可复制正文。
5. 按要求交提示词或调用可用图像工具，查看实际结果并修正具体问题。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 按具体位置、可见现象与任务影响返修；不靠加雾、裁切或换话术掩盖问题。
- 保留用户已经采用的状态与版本回退资料，合并不重复累计图像接受。

<!-- contract:review -->
## 7. 审核门

- [ ] 当前媒介、主体数量、用户锁定、形制/穿戴、空间、方向、光源和材料一致。
- [ ] 低光中的关键人物和装备可辨；同配装不自动等于同一演员。
- [ ] 静帧不以文字补时间因果；视频补充才核对时长、尾态和声场。
- [ ] 地形、掩体、武器方向、动作因果、碎屑、烟尘、伤情和移动路线一致；慢镜有剧情理由。

<!-- contract:pass -->
## 8. 过关标准与状态

- 结构和提示词就绪、实际生成、主审、用户接受分别报告；ready_for_prompt只表示准备就绪。
- 旧战争代表图及顾问五图的历史接受有来源保留，合并检查不算新的图像验收。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 当前任务的具体视觉设计、自然名称提示词、实际图片或已定镜头的视觉补充。
- 按需保留style_module、style_route和qc_contract；数字10为内核，不强制十段外显。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不改写已定故事或接管完整剧本/逐镜分镜，不覆盖上游资产与导演决定。
- 不提供现实武器制造或攻击操作教程；静态效果不认证工程、真实战术或动态能力。
- 独立包包含运行知识；模型工具、账户与额外权限不由Skill提供。
- 用户已接受本轮该类型代表图，见docs/showcase/manifest.json；这是图例级结果，不是通用成功保证。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 视觉参数与质检包是宿主无关的文本合同；真实图片或视频另需媒体工具、模型权限和视觉审核。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/war-design/agents/openai.yaml)
- [`SKILL.md`](../../../skills/war-design/SKILL.md)

**引用资料**

- [`references/cinematic-image-direction.md`](../../../skills/war-design/references/cinematic-image-direction.md)
- [`references/combat-visual.md`](../../../skills/war-design/references/combat-visual.md)
- [`references/COMMON-12-SECTION-PROTOCOL.md`](../../../skills/war-design/references/COMMON-12-SECTION-PROTOCOL.md)
- [`references/NEGATIVE-CASE-BOOK.md`](../../../skills/war-design/references/NEGATIVE-CASE-BOOK.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/war-design/references/SOURCE-LEDGER.md)
- [`references/sources.md`](../../../skills/war-design/references/sources.md)
- [`references/squad-cinematography.md`](../../../skills/war-design/references/squad-cinematography.md)
- [`references/story-visual.md`](../../../skills/war-design/references/story-visual.md)
- [`references/visual-design.md`](../../../skills/war-design/references/visual-design.md)
- [`references/visual-review.md`](../../../skills/war-design/references/visual-review.md)
- [`references/war-visual-presets.md`](../../../skills/war-design/references/war-visual-presets.md)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
