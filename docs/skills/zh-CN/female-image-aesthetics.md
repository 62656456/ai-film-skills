# female-image-aesthetics｜女性影像美学导演

| 状态 | 当前 v0.3.0 源码；公开案例只对应具体任务，不代表通用稳定性保证。 |
|---|---|
| 单独可交付 | 摄影设计、完整实际提示词、已授权生成的图片及可选分享文案。 |
| 单独不能声称 | 技能包不内置模型或账号，也不因安装而自动授权出图或发布。 |

[运行正文 `SKILL.md`](../../../skills/female-image-aesthetics/SKILL.md) · [安装当前源码](../../INSTALLATION.md) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

请安装完整的当前源码文件夹；既有 Release ZIP 不含本次新增模块。

<!-- contract:purpose -->
## 1. 设计目的

联合神态、动作成因、造型、物理表现、构图、光线与成像，创作有吸引力的成年女性摄影影像。

<!-- contract:principles -->
## 2. 设计理念

- 以整幅美感统筹神态、有动因的动作、造型、场景、道具、光色和摄影成像。
- 把情绪落实到视线、面部张力、身体线条与材质反应；每张静帧只容纳一个时刻。
- 按具体观看目的选择柔焦、散景、运动痕迹或反差，不以器材名称代替实际成像。
- 继承已确认的身份和设计，区分独立主题、同身份变体及同故事不同图。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

摄影设计、完整实际提示词、已授权生成的图片及可选分享文案。

**单独不能声称:** 技能包不内置模型或账号，也不因安装而自动授权出图或发布。

<!-- contract:inputs -->
## 4. 输入

- 点名交付物、主体或主题、用途，以及已有的生成和发布授权。
- 已确认参考图，以及它们对身份、服装、构图、光色或情绪的具体职责。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 恢复已有设计决定，辨明本次需要讨论、提示词、实际图片还是分享文案。
2. 形成具体画面主张，围绕它统筹轮廓、色块、纵深、材质和曝光。
3. 把神态、动作成因、物理表现、构图和光线写入完整提示词，按明确职责使用参考。
4. 按当前授权生成，实际审看结果，发现具体失败时回到合格原始基准修订。
5. 交付点名图片或文字，并附完整实际提示词及准确的参考使用说明。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 美感或张力不足时，修订神态、线条、光色、造型或空间中的少量主因。
- 失败图只作诊断；回到合格原始参考或完整文字，不沿失败编辑链继续修。

<!-- contract:review -->
## 7. 审核门

- [ ] 整幅吸引力、主次秩序和摄影表达相互一致。
- [ ] 肩、肘、前臂、腕、手、接触与持物形成可信动作链。
- [ ] 风雨、衣料重量、阴影、反射及景深支持同一个定格瞬间。
- [ ] 准确区分提示词、实际参考输入、生成结果与用户决定。

<!-- contract:pass -->
## 8. 过关标准与状态

- 文字交付完整可执行；图片交付包含真实生成且实际审看的图片。
- 结构检查、公开案例与明确审美接受分别举证。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 完整摄影设计与图像提示词；工具和授权具备时交实际图片。
- 按需交图片加提示词分享文案，附 AI 说明和准确的参考使用记录。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 本模块设计成年人物；普通肖像请求不扩成强制多视图人物资产任务。
- 文字、出图与对外发布分别遵守当前授权，已有授权持续沿用。
- 不冒称真实拍摄、未执行的修图、精确镜头复现或全题材稳定效果。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 能读取完整文件夹的宿主可使用设计方法；实际图片需要生图工具和视觉审看，对外发布还需要已授权账号流程。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/female-image-aesthetics/agents/openai.yaml)
- [`SKILL.md`](../../../skills/female-image-aesthetics/SKILL.md)

**引用资料**

- [`references/body-and-prop.md`](../../../skills/female-image-aesthetics/references/body-and-prop.md)
- [`references/photographic-expression.md`](../../../skills/female-image-aesthetics/references/photographic-expression.md)
- [`references/photographic-prompt-design.md`](../../../skills/female-image-aesthetics/references/photographic-prompt-design.md)
- [`references/reference-to-live-action.md`](../../../skills/female-image-aesthetics/references/reference-to-live-action.md)
- [`references/style-integration.md`](../../../skills/female-image-aesthetics/references/style-integration.md)
- [`references/x-content-handoff.md`](../../../skills/female-image-aesthetics/references/x-content-handoff.md)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
