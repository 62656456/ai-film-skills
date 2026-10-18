# ai-storyboard-director｜剧本转分镜与提示词

| 状态 | 当前分镜5.8.6：默认按观看任务选择专业光学，具体表达电影摄影，并使用新版六模块。包/文字检查与实际媒体接受分别记录。 |
|---|---|
| 单独可交付 | 按当前阶段交创意镜头思路、可读分镜或可复制提示词；点名多种产物才分别交付。 |
| 单独不能声称 | 不改写剧本、不直接生成视频，也不证明平台生成成功。 |

[运行正文 `SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) · [ai-storyboard-director-v5.8.6 ZIP](https://github.com/62656456/ai-film-skills/releases/download/ai-storyboard-director-v5.8.6/ai-storyboard-director.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

本发布快照统一分镜5.8.6提示词合同及制作交接；历史归档保持原内容。

<!-- contract:purpose -->
## 1. 设计目的

设计观众观看顺序、调度、摄影、时长与连续性；按请求另供创意备选或编译已选镜头。

<!-- contract:principles -->
## 2. 设计理念

- 剧情因果、人物目的、调度和空间行动先于镜头术语。
- 人物调度与摄影机共同设计；复合运镜必须有可见起点、触发、阶段和终点。
- 世界状态固定；每次换机位都重新计算当前画面的投影。
- 设计观众体验与场所运行，保留已选环境活动，不强制运动、天气或空气颗粒。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

按当前阶段交创意镜头思路、可读分镜或可复制提示词；点名多种产物才分别交付。

**单独不能声称:** 不改写剧本、不直接生成视频，也不证明平台生成成功。

<!-- contract:inputs -->
## 4. 输入

- 已批准的剧本或片段，包含完整剧情事实、台词和用户锁定的镜头决定。
- 总时长、画幅、已知平台、批准资产和入场世界状态。
- 尚未解决的导演判断必须明确，不能藏进镜头术语。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 人物、场景、道具设计之前，先由用户明确通过项目统一风格模板及完整母提示词；未通过时只推进风格提案和已授权试样，已有有效批准直接复用。
2. 先读因果、人物目标、关系、情绪、空间、动作和连续性。
3. 先固定世界状态并设计调度，再选择摄影机投影。
4. 在明确作品目录中实际恢复设计记录和所需知识，以版本与哈希检查保存意图、镜头和状态，再回读结果。
5. 构建镜头句、丰富覆盖和分阶段摄影机事件，让剧情拍点可见。
6. 用户要创意思路时，实际展示观看策略不同的候选；未采用内容不进入主镜序与提示词。
7. 分镜请求交可读设计；提示词请求或已授权视频生成阶段才编译一条六模块母稿。
8. 执行当前包完成门，反向核对提示词格式化是否保留已选摄影设计；只交付点名创作成果与真实边界。
9. 保留电影摄影、真实光影和相互应答规则。重要开放选择先比较实际观看距离下的起中终画框，再查支持方案的离线机制。
10. 以可选schema-1记录保存选中画框、关键保留项和已采用摄影阶段；机制库与记录检查不证明模型执行或审美。
11. 视频提示词默认顺序：生成任务、视觉风格、主要主体、场景状态、情绪目标、分段脚本；末尾附不编号负面提示词。前两模块共同强化同一成像方向。
12. 联合选择焦距、光学类别、观察位置、焦点与运动；区分普通微距、广角探针、固定视向潜望、分焦、移轴和电影变焦，保留真实机械边界及用户锁定镜头。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 失败图只用于诊断；检查实际提示词与参考，重写完整提示词，从合格原始基准重生成，失败图及其派生图不进入后续图像或视频输入。
- 故事或导演问题退回上游；空间、调度、摄影机、时长或提示词编译问题退回对应设计阶段。
- 技能包维护不同于创作回炉；分享 ZIP 只包含当前独立运行内容，不含历史运行依赖。
- 连续性失败从固定世界坐标修复，不能为了保持画面左右而移动房间。

<!-- contract:review -->
## 7. 审核门

- [ ] 镜头保留剧本事实、人物目的、动作结果、台词和用户锁定顺序。
- [ ] 摄影机、调度、纵深、焦点、运动与剪辑形成镜头句，而不是轮换术语。
- [ ] 时长闭合；台词、世界投影、出框主体、光向、道具和尾帧状态连续。
- [ ] 按实际主色、明暗塑形、材质差异和统一成像判断质感；允许有目的地使用IMAX、摄影机、胶片与镜头参照，名称和静态检查不能证明画质。
- [ ] 从实际成品重建选中画框、四种速度、真实光路、持物接触连续性以及人物/道具/机位共同占位。

<!-- contract:pass -->
## 8. 过关标准与状态

- 当前包完成门通过，且人读分镜无需工程字段即可理解。
- 适用信息在编译中保全；结构与文字检查不证明实际视频执行或审美接受。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 创意镜头以独立文字备选交付，说明故事作用、可见过程、前后衔接与取舍；采用只修改选中设计，不自动授权生成。
- 可读分镜或用户既定镜头表；提示词请求才交六模块母稿，两者都要才分别交付。
- 使用六模块外层和数字10信息内核的可复制正式提示词。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不改写锁定剧情事实或台词，不虚构平台能力或生成成功。
- 分镜完成不等于成片，也不等于用户通过视觉结果。
- 5.6程序检查已记录状态、时间与明确几何，不评审美、不证明图像/视频语义，也不能强制每个聊天入口执行；无作品目录的文字咨询不虚构持久化。
- 创意镜头以独立文字备选交付，说明故事作用、可见过程、前后衔接与取舍；采用只修改选中设计，不自动授权生成。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 文本分镜需完整文件夹；项目保存恢复另需授权文件能力和包内Python标准库程序；媒体执行另需模型工具权限。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/ai-storyboard-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md)

**引用资料**

- [`references/camera-motion-diagnostics.md`](../../../skills/ai-storyboard-director/references/camera-motion-diagnostics.md)
- [`references/cinematography-design-engine.md`](../../../skills/ai-storyboard-director/references/cinematography-design-engine.md)
- [`references/color-and-image-formation.md`](../../../skills/ai-storyboard-director/references/color-and-image-formation.md)
- [`references/creative-shot-ideas.md`](../../../skills/ai-storyboard-director/references/creative-shot-ideas.md)
- [`references/delivery-mode-guard.md`](../../../skills/ai-storyboard-director/references/delivery-mode-guard.md)
- [`references/design-memory-protocol.md`](../../../skills/ai-storyboard-director/references/design-memory-protocol.md)
- [`references/fcml-motion-index.md`](../../../skills/ai-storyboard-director/references/fcml-motion-index.md)
- [`references/fight-design.md`](../../../skills/ai-storyboard-director/references/fight-design.md)
- [`references/fight-reference-case.md`](../../../skills/ai-storyboard-director/references/fight-reference-case.md)
- [`references/framing-and-axis.md`](../../../skills/ai-storyboard-director/references/framing-and-axis.md)
- [`references/optical-shot-selection.md`](../../../skills/ai-storyboard-director/references/optical-shot-selection.md)
- [`references/production-contract.md`](../../../skills/ai-storyboard-director/references/production-contract.md)
- [`references/project-visual-style.md`](../../../skills/ai-storyboard-director/references/project-visual-style.md)
- [`references/reference-design-and-handoff.md`](../../../skills/ai-storyboard-director/references/reference-design-and-handoff.md)
- [`references/shot-design-engine.md`](../../../skills/ai-storyboard-director/references/shot-design-engine.md)

**确定性辅助脚本**

- [`scripts/design_memory.py`](../../../skills/ai-storyboard-director/scripts/design_memory.py)
- [`scripts/fcml_motion.py`](../../../skills/ai-storyboard-director/scripts/fcml_motion.py)
- [`scripts/fcml_source_audit.py`](../../../skills/ai-storyboard-director/scripts/fcml_source_audit.py)

**其他随包文件**

- [`assets/fcml-motion-library.json`](../../../skills/ai-storyboard-director/assets/fcml-motion-library.json)
- [`LICENSE`](../../../skills/ai-storyboard-director/LICENSE)
