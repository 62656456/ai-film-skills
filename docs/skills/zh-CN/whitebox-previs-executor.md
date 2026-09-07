# whitebox-previs-executor｜可检查的3D机位与基础走位预演

| 状态 | 实验；已实现基础预演与逐项合格动作门 |
|---|---|
| 单独可交付 | 宿主具备运行条件时的MP4预演及编译/验证合同。 |
| 单独不能声称 | 不能承诺任意主体、未经测试的完整打斗、成片质量或其他AI视频模型会生成的像素。 |

[运行正文 `SKILL.md`](../../../experimental/whitebox-previs-executor/SKILL.md) · [安装当前源码](../../INSTALLATION.md#experimental-packages) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

新增源码包；v1.3.0没有此发布附件。

<!-- contract:purpose -->
## 1. 设计目的

把已有提示词或分镜编译为可播放3D机位、空间视差、基础走位、时长与切镜预演，明确动作能力限制。

<!-- contract:principles -->
## 2. 设计理念

- 把已有提示词编译成可见3D解释，不重新导演故事。
- 第一交付是可播放MP4；截图、工程文件或数值检查不能单独证明观看结果。
- 只使用已实现代理和动作；动作密集打斗先过短动作门，再扩成长段。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

宿主具备运行条件时的MP4预演及编译/验证合同。

**单独不能声称:** 不能承诺任意主体、未经测试的完整打斗、成片质量或其他AI视频模型会生成的像素。

<!-- contract:inputs -->
## 4. 输入

- 原提示词、镜头描述或分镜，以及已有时长、画幅和摄影决定。
- 宿主Python/Blender与实际MP4解码能力，以及明确来源、输出路径和渲染权限。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 保留来源，记录明确值、推导值、确定默认和未解决决定。
2. 渲染前校验摄影机、主体和时间合同。
3. 用已实现基础或合格骨骼后端渲染，不暗中替换不支持主体或用根节点位移冒充打斗。
4. 实际解码MP4并检查机位、尺度、走位和切镜；打斗另需独立可视动作门。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 未解决几何或不支持代理退回编译解释或明确能力缺口。
- 动作门未过则停止扩张，保留诊断状态，不称打斗预演通过。

<!-- contract:review -->
## 7. 审核门

- [ ] 实际解码时长、帧率、帧数、分辨率和切点符合合同。
- [ ] 请求的运镜产生可观察3D视差，人物道具接触落在最终渲染几何。
- [ ] 打斗须能辨认攻方、守方、武器、接触与反作用，仅数值接触不够。

<!-- contract:pass -->
## 8. 过关标准与状态

- 存在可播放且已检查MP4与编译/验证记录，默认值和未解决边界明确。
- 已有基础预演与短接触证据不证明任意招式或完整30秒打斗通过。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 可播放MP4、previs_compiled.json、previs_validation.json，可选可编辑Blender工程。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 这是实验预演执行器，不是AI视频模型、成片渲染器或对生成模型像素的预测。
- 人形/基础代理和合格动作有限；四足、车辆或新打斗未实现并验证前不得声称支持。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 完整可读包，以及宿主Python、兼容Blender、媒体解码和文件/渲染权限；不捆绑Blender或模型。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../experimental/whitebox-previs-executor/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/whitebox-previs-executor/SKILL.md)

**引用资料**

- [`references/previs-spec.md`](../../../experimental/whitebox-previs-executor/references/previs-spec.md)
- [`references/prompt-to-previs.md`](../../../experimental/whitebox-previs-executor/references/prompt-to-previs.md)

**确定性辅助脚本**

- [`scripts/blender_previs_adapter.py`](../../../experimental/whitebox-previs-executor/scripts/blender_previs_adapter.py)
- [`scripts/blender_rigged_fight_adapter.py`](../../../experimental/whitebox-previs-executor/scripts/blender_rigged_fight_adapter.py)
- [`scripts/render_previs.py`](../../../experimental/whitebox-previs-executor/scripts/render_previs.py)
- [`scripts/run_blender_previs.py`](../../../experimental/whitebox-previs-executor/scripts/run_blender_previs.py)
- [`scripts/run_blender_rigged_fight.py`](../../../experimental/whitebox-previs-executor/scripts/run_blender_rigged_fight.py)
- [`scripts/validate_compiled_previs.py`](../../../experimental/whitebox-previs-executor/scripts/validate_compiled_previs.py)
- [`scripts/validate_spec.py`](../../../experimental/whitebox-previs-executor/scripts/validate_spec.py)

**其他随包文件**

- [`assets/sample-previs.json`](../../../experimental/whitebox-previs-executor/assets/sample-previs.json)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
