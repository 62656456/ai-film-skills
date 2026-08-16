<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="开放影视 Skill：面向 AI 影视创作的故事、设计、镜头与生产能力" />

# 开放影视 Skill

**可独立安装、可组合使用，适配 Codex、Claude Code、TRAE、CodeBuddy、WorkBuddy 与其他 Agent 工具。**

[English](../../../README.md) · **简体中文** · [日本語](../ja/README.md) · [한국어](../ko/README.md)

</div>

## 在 GitHub 直接阅读

19 个模块都已经提供英文和简体中文设计说明，共 **38 个逐模块页面**。每页讲清设计目的、理念、输入、流程、定向退回、审核门、过关证据、输出、边界、跨 Agent 条件和随包文件。

- [浏览全部 38 个设计说明](../../skills/INDEX.md)
- [阅读共同的定向退回、审核与过关逻辑](../../SKILL_DESIGN_SYSTEM.md)
- [按任务比较 19 个模块、运行正文和独立 ZIP](../../../SKILL_CATALOG.md)

设计说明是给人在 GitHub 上阅读的入口；`SKILL.md` 仍是 Agent 的运行真相。结构通过、宿主执行、真实任务证据和用户接受必须分开记录。

## 从这里开始

| 你的任务 | 阅读设计说明 | 运行正文 | 独立 ZIP |
|---|---|---|---|
| 写剧本、改剧本、梳理人物因果与对白 | [`director-agent`](../../skills/zh-CN/director-agent.md) | [`SKILL.md`](../../../skills/director-agent/SKILL.md) | [下载](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) |
| 把确认后的剧本设计成分镜与视频提示词 | [`ai-storyboard-director`](../../skills/zh-CN/ai-storyboard-director.md) | [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) | [下载](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) |
| 设计人物、场景或道具参考资产 | [`character-asset`](../../skills/zh-CN/character-asset.md) · [`scene-asset`](../../skills/zh-CN/scene-asset.md) · [`prop-asset`](../../skills/zh-CN/prop-asset.md) | [人物](../../../skills/character-asset/SKILL.md) · [场景](../../../skills/scene-asset/SKILL.md) · [道具](../../../skills/prop-asset/SKILL.md) | [人物](https://github.com/62656456/ai-film-skills/releases/latest/download/character-asset.zip) · [场景](https://github.com/62656456/ai-film-skills/releases/latest/download/scene-asset.zip) · [道具](https://github.com/62656456/ai-film-skills/releases/latest/download/prop-asset.zip) |
| 为画面加入可观察的类型视觉语言 | [查看完整目录](../../../SKILL_CATALOG.md#genre-visual-language) | [运行索引](../../skills/INDEX.md) | [最新发布](https://github.com/62656456/ai-film-skills/releases/latest) |
| 把批准内容生产成可观看 AI 视频 | [`produce-ai-video`](../../skills/zh-CN/produce-ai-video.md) | [`SKILL.md`](../../../skills/produce-ai-video/SKILL.md) | [下载](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) |
| 编排 AI 短剧完整生产流程 | [`ai-short-drama-production`](../../skills/zh-CN/ai-short-drama-production.md) | [`SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md) | [下载](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) |
| 设计、实现或审查网页界面 | [`web-design-director`](../../skills/zh-CN/web-design-director.md) | [`SKILL.md`](../../../skills/web-design-director/SKILL.md) | [下载](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) |

## 这套 Skill 解决什么

它们不是把热门视觉词堆成提示词，而是把剧情因果、人物目的、走位、空间连续性、动作物理、光线、材质和生产门转成可复用的执行合同。

第一交付层始终是人能判断的真实结果：剧本、分镜、资产合同、视觉方向、研究报告或合格媒体。内部字段和检查只用于支撑结果，不代替结果。

<img src="../../assets/skill-map.svg" width="100%" alt="从故事与资产到视觉语言、镜头、生产和验证的能力地图" />

## 单独可用不等于包办全部

每个模块都能在自己点名的结果边界内单独使用。例如，人物资产模块可以单独输出人物任务说明与资产合同，类型模块可以单独输出视觉参数包，导演模块可以单独写或诊断剧本。

“可独立”不代表类型模块同时负责写剧本，也不代表没有生图工具就已经生成资产图，更不代表生产模块可以绕过费用、版权、发布权限和用户审核。每个逐模块页面都明确写出“单独可交付”和“单独不能声称”。

## 跨 Agent 安装

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py --list
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

同一个 Skill 文件夹可安装到：Codex 的 `.codex/skills/`、Claude Code 的 `.claude/skills/`、TRAE 项目的 `.agents/skills/`、CodeBuddy 的 `.codebuddy/skills/`；WorkBuddy 可在“添加技能 → 上传技能”中导入独立 ZIP。其他 Agent 若没有原生 Skill 加载器，可以把 `SKILL.md` 与本地引用文件作为指令导入。

每个模块已经自带所需引用，不依赖共享目录。`agents/openai.yaml` 只是 Codex 可选界面元数据，其他 Agent 可以安全忽略。Agent 能阅读指令不等于原生发现或原生执行。具体产品名核对、官方依据和限制见 [Agent 兼容说明](../../COMPATIBILITY.md)，完整步骤见 [安装指南](../../INSTALLATION.md)。

## 状态不是装饰

- **已部署**：当前个人运行包正在使用，但不等于已经完成三个不同真实任务的稳定验证。
- **已封装**：结构达到分发要求，但当前没有部署。
- **实验中**：与正常安装隔离，明确保留未批准或未完成状态。
- **已淘汰**：故意不收录，不能从旧文件自动恢复。
- **第三方**：不当成个人原创再次发布。

详细状态见 [Skill 完整目录](../../../SKILL_CATALOG.md)，设计总则见 [每个 Skill 如何设计](../../SKILL_DESIGN_SYSTEM.md)，结构说明见 [架构](../../ARCHITECTURE.md)。

## 仓库设计来源

仓库借鉴了 [OmniRoute](https://github.com/diegosouzapw/OmniRoute) 的信息组织优点：清晰首屏、快速导航、多语种入口、可复制安装命令、状态展示、图解、贡献入口、安全规则和第三方说明。没有复制其品牌、图片、文案或代码。

## 反馈与联系

欢迎通过 [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions)、[GitHub Issues](https://github.com/62656456/ai-film-skills/issues) 或邮件 [haldissita@gmail.com](mailto:haldissita@gmail.com) 提供真实使用反馈。

## 开源协议

除非文件另有声明，本仓库个人原创内容使用 [Apache License 2.0](../../../LICENSE)。
