# noir-design｜黑色与犯罪视觉参数

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 黑色 `style_route`、场景与光影参数、负向约束和 QC 合同。 |
| 单独不能声称 | 不等于蓝黑滤镜、无来源烟雾、乱向百叶阴影或夸张荷兰角。 |

[运行正文 `SKILL.md`](../../../skills/noir-design/SKILL.md) · [v1.3.0 历史 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/noir-design.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

v1.3.0历史快照；已更新模块与当前源码不同。

<!-- contract:purpose -->
## 1. 设计目的

把黑色与犯罪张力转成可读对比、有来源实用光、遮挡、权力几何、湿旧材质、克制动作和声音。

<!-- contract:principles -->
## 2. 设计理念

- 把类型感翻译成可观察的镜头、色彩、空间、动作、材质、声音和连续性参数。
- 类型参数服务已批准的故事和资产，不改写它们。
- 导演名和色值只是来源或起点，不是模仿命令或普适定律。
- 黄金时刻、互补色、浅景深、前景人物、固定焦段和磨损都是可选设计，不是通用质量条件。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

黑色 `style_route`、场景与光影参数、负向约束和 QC 合同。

**单独不能声称:** 不等于蓝黑滤镜、无来源烟雾、乱向百叶阴影或夸张荷兰角。

<!-- contract:inputs -->
## 4. 输入

- 类型、目标媒介、场景功能、主体、锁定要求及相关资产；仅当前交付需要时读取时长和平台字段。
- 已有导演、调度、布光、连续性和尾帧决定。
- 缺失字段保持开放，不能用“电影感”等空词补全。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 先读包内电影画面关系判断，选择成像媒介，建立可见命题和注意力层次，再选预设。
2. 推导有功能的色彩、光源、空间结构和场景参数。
3. 补材质、接触和状态连续性；仅视频加入运镜、时间和声音，保留已有批准资产。
4. 编译数字10信息和平台转译，不改变上游决定。
5. 执行共享与类型专项审核，输出 `ready_for_prompt` 或具体字段的 `rework`。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 故事、资产或调度失败退回责任层；风格失败退回造成问题的镜头、色彩、空间、动作、材质或连续性字段。
- 审核失败必须输出带具体字段的 `rework`，不能靠再生成一次绕过。
- 这些模块有设计回炉，但没有历史版本回滚机制。

<!-- contract:review -->
## 7. 审核门

- [ ] 当前媒介必需字段相互一致：构图、功能色彩、有来源光、空间、主体材质关系和状态；视频才补运动与声音。
- [ ] 共享假电影感检查会拦截空质量词、无动机运镜、无源光、装饰性色彩和不稳定道具/空间。
- [ ] 类型专项负向只针对高概率失败，不压制剧情允许的色彩、尺度、静止或运动。
- [ ] 实用光与阴影方向一致，暗部可读，遮挡与反差承担信息或权力功能。

<!-- contract:pass -->
## 8. 过关标准与状态

- 共享与类型检查全部通过，批准资产未被改写，模块可输出 `ready_for_prompt`。
- `ready_for_prompt` 只表示视觉参数包就绪，不证明图片、片段或成片已经通过。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 可独立使用的类型 `style_route`、`style_module` 和 `qc_contract` 视觉参数包。
- 可进入场景生产的提示词字段、负向约束、连续性状态和声音提示。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不写剧本、不替代导演判断、不修改批准资产外观。
- 不宣称普适类型配色、不模仿在世创作者，也不宣称生成成功。
- 新增画面关系参考是作者对所供图片分析的综合；14张接受成图不证明他方Skill内部方法、稳定成功率或旧新版同题A/B提升。
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

- [`agents/openai.yaml`](../../../skills/noir-design/agents/openai.yaml)
- [`SKILL.md`](../../../skills/noir-design/SKILL.md)

**引用资料**

- [`references/cinematic-image-direction.md`](../../../skills/noir-design/references/cinematic-image-direction.md)
- [`references/COMMON-12-SECTION-PROTOCOL.md`](../../../skills/noir-design/references/COMMON-12-SECTION-PROTOCOL.md)
- [`references/NEGATIVE-CASE-BOOK.md`](../../../skills/noir-design/references/NEGATIVE-CASE-BOOK.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/noir-design/references/SOURCE-LEDGER.md)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
