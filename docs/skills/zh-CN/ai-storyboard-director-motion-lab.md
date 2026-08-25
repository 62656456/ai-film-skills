# ai-storyboard-director-motion-lab｜5.4.3 复杂运镜测试线

| 状态 | 测试中；5.4.3 实验候选；仅限显式调用 |
|---|---|
| 单独可交付 | 用户显式点名后交付 5.4.3 测试分镜、输入职责裁决和复杂运镜六模块提示词包。 |
| 单独不能声称 | 它不是默认分镜 Skill，不能声称已经转正、模型稳定生成、成片合格或用户接受。 |

[运行正文 `SKILL.md`](../../../experimental/ai-storyboard-director-motion-lab/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director-motion-lab.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

测试复杂摄影机路径、视觉变换、运镜参考视频和 3D 预演能否在不替换正式 5.4.2 分镜合同的前提下增加必要可见信息。

<!-- contract:principles -->
## 2. 设计理念

- 剧情因果、人物目的、调度和空间行动先于镜头术语。
- 人物调度与摄影机共同设计；复合运镜必须有可见起点、触发、阶段和终点。
- 世界状态固定；每次换机位都重新计算当前画面的投影。
- 比较固定、简单和复杂摄影机方案；只有复杂方案带来简单方案无法等价完成的剧情、空间、时间或主观可见结果时才采用。
- 文字、参考视频、3D 预演、图片和关键帧各自保持明确职责边界，不能静默覆盖剧情或资产事实。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

用户显式点名后交付 5.4.3 测试分镜、输入职责裁决和复杂运镜六模块提示词包。

**单独不能声称:** 它不是默认分镜 Skill，不能声称已经转正、模型稳定生成、成片合格或用户接受。

<!-- contract:inputs -->
## 4. 输入

- 已批准的剧本或片段，包含完整剧情事实、台词和用户锁定的镜头决定。
- 总时长、画幅、已知平台、批准资产和入场世界状态。
- 尚未解决的导演判断必须明确，不能藏进镜头术语。
- 用户显式要求测试 `$ai-storyboard-director-motion-lab`；仅出现“复杂运镜”四字不构成实验授权。
- 运镜参考视频或 3D 预演必须写清负责的运动/拓扑，以及不提供的人物、地点、品牌、材质和剧情事实。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 先读因果、人物目标、关系、情绪、空间、动作和连续性。
2. 先固定世界状态并设计调度，再选择摄影机投影。
3. 构建镜头句、丰富覆盖和分阶段摄影机事件，让剧情拍点可见。
4. 输出人读分镜，并把数字10信息编译进六个可见提示词模块。
5. 执行十二项完成门，只返回点名创作成果和真正未解决的边界。
6. 先标记为不改变正式 5.4.2 的 5.4.3 测试，裁决输入职责；路径无法可靠描述时拆段或要求预演。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 故事或导演问题退回上游；空间、调度、摄影机、时长或提示词编译问题退回对应设计阶段。
- 版本回滚不同于创作回炉；只有用户明确要求时，才可使用已有的 5.4.1 哈希快照。
- 连续性失败从固定世界坐标修复，不能为了保持画面左右而移动房间。
- 复杂运镜若只增加奇观则退回固定或简单方案；拓扑或遮挡无法证明时退回 3D 预演，不虚构连续性。

<!-- contract:review -->
## 7. 审核门

- [ ] 镜头保留剧本事实、人物目的、动作结果、台词和用户锁定顺序。
- [ ] 摄影机、调度、纵深、焦点、运动与剪辑形成镜头句，而不是轮换术语。
- [ ] 时长闭合；台词、世界投影、出框主体、光向、道具和尾帧状态连续。
- [ ] 每个运动阶段都有可见触发、路径、焦点/遮挡接力、速度变化、新信息、终点，并说明简单替代为何不足。

<!-- contract:pass -->
## 8. 过关标准与状态

- 十二项完成检查全部通过，且人读分镜不依赖工程字段。
- 六模块包含数字10全部信息，但这仍不证明平台已经成功生成视频。
- 结构或文字行为通过后仍保持“测试中”；只有用户后续明确批准，才能另开转正决定。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 包含时间、景别/摄影机、可见动作、台词与声音的人读多镜头分镜。
- 使用六模块外层和数字10信息内核的可复制正式提示词。
- 输出以“5.4.3 实验候选｜仅本次测试｜正式 5.4.2 不变”开头，并同时包含五列分镜和完整六模块提示词。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不改写锁定剧情事实或台词，不虚构平台能力或生成成功。
- 分镜完成不等于成片，也不等于用户通过视觉结果。
- 该包保持 `allow_implicit_invocation: false`，不进入完整工作室 ZIP，本地安装必须显式添加 `--experimental`。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 任何能读取完整文件夹的宿主都可做文本分镜；文件能力用于引用和哈希回滚，真实生成另需媒体工具与权限。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../experimental/ai-storyboard-director-motion-lab/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/ai-storyboard-director-motion-lab/SKILL.md)

**引用资料**

- [`references/advanced-motion-engine.md`](../../../experimental/ai-storyboard-director-motion-lab/references/advanced-motion-engine.md)
- [`references/formal-production-contract.md`](../../../experimental/ai-storyboard-director-motion-lab/references/formal-production-contract.md)
- [`references/input-duty-matrix.md`](../../../experimental/ai-storyboard-director-motion-lab/references/input-duty-matrix.md)
