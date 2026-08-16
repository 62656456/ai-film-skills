# web-design-director｜产品原生网页设计

| 状态 | 已部署 |
|---|---|
| 单独可交付 | 完整界面方向或审查；有代码与浏览器能力时，可交付经验证的实现切片。 |
| 单独不能声称 | 没有真实渲染和交互审核时，不能声称视觉实现或用户接受通过。 |

[运行正文 `SKILL.md`](../../../skills/web-design-director/SKILL.md) · [独立 ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) · [安装说明](../../INSTALLATION.md) · [兼容说明](../../COMPATIBILITY.md) · [设计总则](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. 设计目的

从产品真实出发，完成有辨识度的生产级网页方向、审查或构建，并以真实渲染验证。

<!-- contract:principles -->
## 2. 设计理念

- 先做产品与设计判断，再实施；界面方向必须来自真实产品、受众和页面任务。
- 把视觉大胆用在一个有依据的标志性元素上，其余系统保持克制。
- 源码检查和实现测试不能替代真实渲染、状态、响应式与无障碍审核。

<!-- contract:standalone -->
## 3. 适合单独使用的范围

当点名结果落在以下边界内时，可以只拿这一个模块使用：

完整界面方向或审查；有代码与浏览器能力时，可交付经验证的实现切片。

**单独不能声称:** 没有真实渲染和交互审核时，不能声称视觉实现或用户接受通过。

<!-- contract:inputs -->
## 4. 输入

- 产品类型、受众、页面唯一任务、主路径、真实内容、品牌/设计系统和技术栈。
- 审核或修改现有产品时，需要现有界面、截图或仓库。
- 所需状态、设备、无障碍约束、性能边界和代码修改授权。

<!-- contract:workflow -->
## 5. 流程逻辑

1. 锁定产品、受众、页面唯一任务和词汇。
2. 提出方向前先检查真实界面与系统。
3. 选择产品原生的色彩、字体、布局和一个标志元素，排除模板化默认。
4. 设计用户路径、空/载入/失败/成功状态、响应式和工程合同。
5. 实现一个完整切片，真实渲染并审核视觉、交互、键盘、移动端和回归。

<!-- contract:returns -->
## 6. 退回、重做与版本回滚

- 产品事实或路径不清时退回产品定义，不能靠装饰解决。
- 方向可套在任何产品上时，退回产品原生方向与标志元素。
- 状态缺失退回流程设计；实现或渲染阻塞退回工程合同，并在真实界面重新验证。

<!-- contract:review -->
## 7. 审核门

- [ ] 产品真实、信息架构、独特性、视觉系统、交互、无障碍、响应式和工程质量全部通过。
- [ ] 所有必要状态可见并能指导用户；错误说明恢复方式，操作命名一致。
- [ ] 真实渲染在桌面和移动宽度下检查，包含键盘焦点与减少动画行为。

<!-- contract:pass -->
## 8. 过关标准与状态

- 方向模式在设计系统与流程具体可实施时通过；构建模式还必须有真实渲染证据。
- 没有渲染和交互证据时，只能写设计/源码审查，不能写视觉实现通过。

> 下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。

<!-- contract:outputs -->
## 9. 输出

- 产品原生设计方向与工程合同、带证据的审查，或经验证的实现切片。
- 具体设计决定、按阻塞级排序的问题、实施时的准确变更文件和剩余验证边界。

<!-- contract:boundaries -->
## 10. 边界、依赖与权限

- 不为审美统一擅自迁移框架、增加依赖或重做无关界面。
- 不把源码检查、测试或静态稿冒充用户通过的视觉质量。

<!-- contract:agents -->
## 11. 跨 Agent 使用

- 标准包是完整 Skill 文件夹，不是只复制一段提示词。
- `agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。
- 方向和审查可用文本完成；构建和视觉通过还需仓库/文件权限、项目运行环境、浏览器渲染或截图及交互检查。
- Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。

<!-- contract:sources -->
## 12. 原始文件与引用

**运行正文与元数据**

- [`agents/openai.yaml`](../../../skills/web-design-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/web-design-director/SKILL.md)

**引用资料**

- [`references/creative-direction.md`](../../../skills/web-design-director/references/creative-direction.md)
- [`references/design-rubric.md`](../../../skills/web-design-director/references/design-rubric.md)
- [`references/web-quality-checklist.md`](../../../skills/web-design-director/references/web-quality-checklist.md)
