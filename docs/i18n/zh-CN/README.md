<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="开放影视 Skill：面向 AI 影视创作的故事、设计、镜头与生产能力" />

# 开放影视 Skill

**可独立安装、可组合使用，适配 Codex、Claude Code、TRAE、CodeBuddy、WorkBuddy 与其他 Agent 工具。**

[English](../../../README.md) · **简体中文** · [日本語](../ja/README.md) · [한국어](../ko/README.md)

</div>

## 从这里开始

| 你的任务 | 使用哪个 Skill |
|---|---|
| 写剧本、改剧本、梳理人物因果与对白 | [`director-agent`](../../../skills/director-agent/) |
| 把确认后的剧本设计成分镜与视频提示词 | [`ai-storyboard-director`](../../../skills/ai-storyboard-director/) |
| 设计人物、场景或道具参考资产 | [`character-asset`](../../../skills/character-asset/) · [`scene-asset`](../../../skills/scene-asset/) · [`prop-asset`](../../../skills/prop-asset/) |
| 为画面加入可观察的类型视觉语言 | [查看完整目录](../../../SKILL_CATALOG.md) |
| 把批准内容生产成可观看 AI 视频 | [`produce-ai-video`](../../../skills/produce-ai-video/) |
| 编排 AI 短剧完整生产流程 | [`ai-short-drama-production`](../../../skills/ai-short-drama-production/) |
| 设计、实现或审查网页界面 | [`web-design-director`](../../../skills/web-design-director/) |

## 这套 Skill 解决什么

它们不是把热门视觉词堆成提示词，而是把剧情因果、人物目的、走位、空间连续性、动作物理、光线、材质和生产门转成可复用的执行合同。

第一交付层始终是人能判断的真实结果：剧本、分镜、资产合同、视觉方向、研究报告或合格媒体。内部字段和检查只用于支撑结果，不代替结果。

<img src="../../assets/skill-map.svg" width="100%" alt="从故事与资产到视觉语言、镜头、生产和验证的能力地图" />

## 跨 Agent 安装

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py --list
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

同一个 Skill 文件夹可安装到：Codex 的 `.codex/skills/`、Claude Code 的 `.claude/skills/`、TRAE 项目的 `.agents/skills/`、CodeBuddy 的 `.codebuddy/skills/`；WorkBuddy 可在“添加技能 → 上传技能”中导入独立 ZIP。其他 Agent 若没有原生 Skill 加载器，可以把 `SKILL.md` 与本地引用文件作为指令导入。

每个模块已经自带所需引用，不依赖共享目录。`agents/openai.yaml` 只是 Codex 可选界面元数据，其他 Agent 可以安全忽略。具体产品名核对、官方依据和限制见 [Agent 兼容说明](../../COMPATIBILITY.md)，完整步骤见 [安装指南](../../INSTALLATION.md)。

## 状态不是装饰

- **已部署**：当前个人运行包正在使用，但不等于已经完成三个不同真实任务的稳定验证。
- **已封装**：结构达到分发要求，但当前没有部署。
- **实验中**：与正常安装隔离，明确保留未批准或未完成状态。
- **已淘汰**：故意不收录，不能从旧文件自动恢复。
- **第三方**：不当成个人原创再次发布。

详细状态见 [Skill 完整目录](../../../SKILL_CATALOG.md)，结构说明见 [架构](../../ARCHITECTURE.md)。

## 仓库设计来源

仓库借鉴了 [OmniRoute](https://github.com/diegosouzapw/OmniRoute) 的信息组织优点：清晰首屏、快速导航、多语种入口、可复制安装命令、状态展示、图解、贡献入口、安全规则和第三方说明。没有复制其品牌、图片、文案或代码。

## 反馈与联系

欢迎通过 [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions)、[GitHub Issues](https://github.com/62656456/ai-film-skills/issues) 或邮件 [haldissita@gmail.com](mailto:haldissita@gmail.com) 提供真实使用反馈。

## 开源协议

除非文件另有声明，本仓库个人原创内容使用 [Apache License 2.0](../../../LICENSE)。
