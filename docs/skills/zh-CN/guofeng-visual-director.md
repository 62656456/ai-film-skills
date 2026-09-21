# guofeng-visual-director｜古风视觉设计总监

| 状态 | 候选0.1.1；主动选择的实验包；图像待审 |
|---|---|
| 单独可交付 | 完整视觉方案、图像提示词、受控变体或诊断。 |
| 单独不能声称 | 不自动证明历史准确、用户接受或视频成片。 |

[运行正文 `SKILL.md`](../../../experimental/guofeng-visual-director/SKILL.md) · [安装当前源码](../../INSTALLATION.md#experimental-packages) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

候选源码；历史v1.3.0无此ZIP。

<!-- contract:purpose -->
## 1. 设计目的

统一设计古风人物服饰、建筑空间、器物、光色与完整图像提示词。

<!-- contract:principles -->
## 2. 设计理念

- 从简报推导文化、生活空间与画面；区分历史还原、架空古风和风格化表达。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

完整视觉方案、图像提示词、受控变体或诊断。

**单独不能声称:** 不自动证明历史准确、用户接受或视频成片。

<!-- contract:inputs -->
## 4. 输入

- 故事、人像、环境、器物简报或视觉参考，以及已有锁定事实。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 区分依据与开放项，选择文化与媒介，设计人物、空间、光色和材质，编译提示词并检查实际结果。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 保留已认可内容，修复最早出现的文化、空间或画面偏差。

<!-- contract:review -->
## 7. 审核门

- [ ] 对照真实图片与简报；文字检查不代表画面被接受。

<!-- contract:pass -->
## 8. 过关标准与状态

- 结果符合指定媒介和证据；用户审美由用户单独确认。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 按要求交付视觉方案、完整图像提示词、受控变体或图像诊断。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不自动变仙侠、武侠、固定朝代，不因讨论技能就生图或扩为全片。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 视觉参数与质检包是宿主无关的文本合同；真实图片或视频另需媒体工具、模型权限和视觉审核。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../experimental/guofeng-visual-director/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/guofeng-visual-director/SKILL.md)

**引用资料**

- [`references/cultural-grounding.md`](../../../experimental/guofeng-visual-director/references/cultural-grounding.md)
- [`references/image-direction.md`](../../../experimental/guofeng-visual-director/references/image-direction.md)
- [`references/people-and-objects.md`](../../../experimental/guofeng-visual-director/references/people-and-objects.md)
- [`references/prompt-and-review.md`](../../../experimental/guofeng-visual-director/references/prompt-and-review.md)
- [`references/world-and-space.md`](../../../experimental/guofeng-visual-director/references/world-and-space.md)

**新构建 ZIP 的分发许可文件**

新构建会将下列文件附在 ZIP 内的 Skill 目录，不修改运行源码；既有历史 Release 附件不变。

- [`LICENSE`](../../../LICENSE)
