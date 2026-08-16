# ai-storyboard-director｜剧本转分镜与提示词

| 状态 | 已部署；5.4.2 候选基线继承 5.4.1 连续性合同 |
|---|---|
| 单独可交付 | 针对已有批准剧本的完整分镜和可复制提示词包。 |
| 单独不能声称 | 不改写剧本、不直接生成视频，也不证明平台生成成功。 |

[运行正文 `SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

把已批准剧本变成人读多镜头设计和生产提示词，同时守住因果、调度、时长和世界空间连续性。

<!-- contract:principles -->
## 2. 设计理念

- 剧情因果、人物目的、调度和空间行动先于镜头术语。
- 人物调度与摄影机共同设计；复合运镜必须有可见起点、触发、阶段和终点。
- 世界状态固定；每次换机位都重新计算当前画面的投影。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

针对已有批准剧本的完整分镜和可复制提示词包。

**单独不能声称:** 不改写剧本、不直接生成视频，也不证明平台生成成功。

<!-- contract:inputs -->
## 4. 输入

- 已批准的剧本或片段，包含完整剧情事实、台词和用户锁定的镜头决定。
- 总时长、画幅、已知平台、批准资产和入场世界状态。
- 尚未解决的导演判断必须明确，不能藏进镜头术语。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 先读因果、人物目标、关系、情绪、空间、动作和连续性。
2. 先固定世界状态并设计调度，再选择摄影机投影。
3. 构建镜头句、丰富覆盖和分阶段摄影机事件，让剧情拍点可见。
4. 输出人读分镜，并把数字10信息编译进六个可见提示词模块。
5. 执行十二项完成门，只返回点名创作成果和真正未解决的边界。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 故事或导演问题退回上游；空间、调度、摄影机、时长或提示词编译问题退回对应设计阶段。
- 版本回滚不同于创作回炉；只有用户明确要求时，才可使用已有的 5.4.1 哈希快照。
- 连续性失败从固定世界坐标修复，不能为了保持画面左右而移动房间。

<!-- contract:review -->
## 7. 审核门

- [ ] 镜头保留剧本事实、人物目的、动作结果、台词和用户锁定顺序。
- [ ] 摄影机、调度、纵深、焦点、运动与剪辑形成镜头句，而不是轮换术语。
- [ ] 时长闭合；台词、世界投影、出框主体、光向、道具和尾帧状态连续。

<!-- contract:pass -->
## 8. 过关标准与状态

- 十二项完成检查全部通过，且人读分镜不依赖工程字段。
- 六模块包含数字10全部信息，但这仍不证明平台已经成功生成视频。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 包含时间、景别/摄影机、可见动作、台词与声音的人读多镜头分镜。
- 使用六模块外层和数字10信息内核的可复制正式提示词。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不改写锁定剧情事实或台词，不虚构平台能力或生成成功。
- 分镜完成不等于成片，也不等于用户通过视觉结果。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 任何能读取完整文件夹的宿主都可做文本分镜；文件能力用于引用和哈希回滚，真实生成另需媒体工具与权限。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/ai-storyboard-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md)

**引用资料**

- [`references/production-contract.md`](../../../skills/ai-storyboard-director/references/production-contract.md)
- [`references/shot-design-engine.md`](../../../skills/ai-storyboard-director/references/shot-design-engine.md)

**版本与回退证据**

- [`versions/5.4.1/production-contract.snapshot.md`](../../../skills/ai-storyboard-director/versions/5.4.1/production-contract.snapshot.md)
- [`versions/5.4.1/rollback-manifest.json`](../../../skills/ai-storyboard-director/versions/5.4.1/rollback-manifest.json)
- [`versions/5.4.1/SKILL.snapshot.md`](../../../skills/ai-storyboard-director/versions/5.4.1/SKILL.snapshot.md)
