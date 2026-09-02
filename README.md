<div align="center">

<img src="docs/assets/hero.svg" width="100%" alt="Open Film Skills — 从剧本、资产和视觉语言到分镜、生产与验收的 AI 影视 Skill 工作室" />

# Open Film Skills｜开放影视技能

**让 Agent 把剧本变成可读剧本、可复用视觉资产、可执行分镜、可复制提示词和可验收的 AI 视频生产流程。**

*Script-to-screen Agent Skills for AI filmmaking — modular, inspectable, and independently installable.*

[从一个结果开始](#从一个结果开始) · [60 秒开始](#60-秒开始) · [查看真实证据](#see-the-skills-in-motion) · [浏览全部 Skill](SKILL_CATALOG.md) · [下载完整套装](https://github.com/62656456/ai-film-skills/releases/latest/download/open-film-skills-complete.zip)

**简体中文（当前页）** · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [English overview](#english-overview)

![Packaged skills](https://img.shields.io/badge/packaged_skills-18-FF6B35?style=flat-square)
![Experimental skills](https://img.shields.io/badge/experimental-1-D6A756?style=flat-square)
![Standalone packages](https://img.shields.io/badge/standalone_packages-19-7ED6A5?style=flat-square)
[![Validate Skills](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/62656456/ai-film-skills)](https://skills.sh/62656456/ai-film-skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-5B8CFF?style=flat-square)](LICENSE)

</div>

## 这是什么

Open Film Skills 不是一份“万能提示词”，而是一组面向 AI 影视创作的独立 Agent Skills。它把创作拆成六个可检查的阶段：

```text
故事与导演判断 → 人物 / 场景 / 道具资产 → 类型视觉语言 → 镜头与提示词 → 视频生产 → 证据与验收
```

你可以只安装当前需要的一项，也可以安装完整工作室。每个 Skill 都带自己的运行正文和必要引用，不依赖仓库里的共享知识目录。

> 设计原则：先交人能判断的结果，再让规则、检查和状态支撑结果。结构通过、宿主加载、真实任务、媒体效果和用户确认是五种不同证据，不能互相冒充。

## 能力总览

| 阶段 | 使用的 Skill | 直接得到什么 |
|---|---|---|
| 故事与导演 | [`director-agent`](docs/skills/zh-CN/director-agent.md) | 剧本创作与修改、人物因果、自然对白、潜台词、场景目的和分镜前导演判断 |
| 资产定义 | [`character-asset`](docs/skills/zh-CN/character-asset.md) · [`scene-asset`](docs/skills/zh-CN/scene-asset.md) · [`prop-asset`](docs/skills/zh-CN/prop-asset.md) | 可复用的人物、场景、道具参考任务与连续性合同 |
| 视觉语言 | [8 个类型视觉 Skill](SKILL_CATALOG.md#genre-visual-language) | 可观察的构图、光线、空间、动作、材质与连续性参数 |
| 分镜与提示词 | [`ai-storyboard-director`](docs/skills/zh-CN/ai-storyboard-director.md) | 人读分镜、人物调度、焦段与机位、摄影机路径、空间连续性和完整视频提示词 |
| 视频生产 | [`produce-ai-video`](docs/skills/zh-CN/produce-ai-video.md) · [`ai-short-drama-production`](docs/skills/zh-CN/ai-short-drama-production.md) | 生成准备、费用门、生产分段、剪辑、完整播放检查、修复与短剧编排 |
| 产品与研究 | [`web-design-director`](docs/skills/zh-CN/web-design-director.md) · [数据研究 Skills](SKILL_CATALOG.md#production-product-and-research) | 网页设计与实现、官方市场研究、经批准的数据知识写入 |

完整目录包含 19 个模块、38 个英文／简体中文设计说明，以及每个模块的运行正文和独立 ZIP：

- [按任务比较全部 Skill](SKILL_CATALOG.md)
- [浏览 38 个设计说明](docs/skills/INDEX.md)
- [理解共同的审核、退回与过关逻辑](docs/SKILL_DESIGN_SYSTEM.md)

## 从一个结果开始

| 你现在要什么 | 先用哪个 Skill | 一句话调用 |
|---|---|---|
| 写剧本、改剧本、解决人物和对白问题 | [`director-agent`](skills/director-agent/SKILL.md) | `使用 $director-agent，把这段故事改成因果清楚、人物行动可拍、对白自然的剧本。` |
| 把确认后的剧本做成分镜和提示词 | [`ai-storyboard-director`](skills/ai-storyboard-director/SKILL.md) | `使用 $ai-storyboard-director，把这段剧本设计成人读分镜和一条完整视频提示词。` |
| 定义人物、场景或道具参考资产 | [`character-asset`](skills/character-asset/SKILL.md) · [`scene-asset`](skills/scene-asset/SKILL.md) · [`prop-asset`](skills/prop-asset/SKILL.md) | `使用对应资产 Skill，把这个对象整理成可审核、可复用的参考资产合同。` |
| 为作品建立明确的类型视觉语言 | [类型视觉 Skill](SKILL_CATALOG.md#genre-visual-language) | `使用对应类型 Skill，只输出能在画面中被观察和检查的视觉参数。` |
| 把批准内容生产成可观看视频 | [`produce-ai-video`](skills/produce-ai-video/SKILL.md) | `使用 $produce-ai-video，在费用和权限确认后生成、剪辑、完整播放检查并修复。` |

## 60 秒开始

先列出可安装的正式 Skills：

```bash
npx --yes skills@latest add 62656456/ai-film-skills --list
```

只安装当前需要的一项：

```bash
npx --yes skills@latest add 62656456/ai-film-skills --skill ai-storyboard-director --agent codex --copy --yes
```

或使用仓库自带安装器：

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py ai-storyboard-director --platform codex
```

然后把已经确认的剧情交给 Agent：

```text
使用 $ai-storyboard-director，把下面已经确认的剧情设计成人读分镜和一条完整视频提示词。
每个时间段标题直接显示焦段/光学、机位方位与高度、摄影机路径与朝向变化、速度、焦点或遮挡接力和动作落点：
[粘贴剧情]
```

Skills CLI 1.5.23 的发现和六文件复制路径已经隔离验证；是否原生加载仍由具体宿主决定。查看 [CLI 验证记录](examples/skills-cli-install-verification.md)、[skills.sh 索引验证](examples/skills-sh-index-verification.md)和[完整安装指南](docs/INSTALLATION.md)。

## 为什么拆成多个独立 Skill

一个超级 Skill 看起来方便，但会让剧本、资产、摄影、风格、生产和审核规则同时进入上下文，增加冲突和误触发。Open Film Skills 选择把职责拆开：

1. **需要什么才加载什么**：写剧本时不必读取全部摄影和生产规则。
2. **每项能力单独验收**：结构通过不等于真实任务通过，分镜通过也不等于视频成片通过。
3. **可替换、可回退**：升级一个 Skill 不必同时改写整个创作系统。

如果需要完整短剧路线，再由 [`ai-short-drama-production`](docs/skills/zh-CN/ai-short-drama-production.md) 编排各阶段；编排器不会吞并各 Skill 的职责和验收门。

## See the Skills in motion

下面是两段真实可播放的本地 3D 预演证据，用来展示“镜头和动作如何被看见并检查”。

<table>
<tr>
<td width="50%" valign="top">
<a href="https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4"><img src="docs/media/previs-blocking-preview.gif" width="100%" alt="五秒灰模预演，展示摄影机推进、人物走位、切镜、横移跟拍和场景视差" /></a><br />
<strong>Camera and blocking previs · 5.0 seconds</strong><br />
摄影机运动、人物位置、切镜和空间视差可直接检查。<a href="https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4">播放原始 MP4</a>。
</td>
<td width="50%" valign="top">
<a href="https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4"><img src="docs/media/rigged-contact-preview.gif" width="100%" alt="二点八秒骨骼动作门，展示双手握持、接触保持和相反方向反作用" /></a><br />
<strong>Rigged contact action gate · 2.8 seconds</strong><br />
双手握持、最终接触面、接触保持时间和相反反作用可直接检查。<a href="https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4">播放原始 MP4</a>。
</td>
</tr>
</table>

These are rough 3D previs checkpoints, **not finished AI films**, not external-user adoption, and not proof that the **unpublished local previs executor** ships in this repository. [查看完整媒体证据与哈希边界](docs/media/media-manifest.json)。

## 一个具体差异：镜头标题不再只讲剧情

<img src="docs/assets/storyboard-544-proof.png" width="100%" alt="只有剧情短标题的旧写法与5.4.4可执行摄影方案标题的对比" />

Storyboard Director 5.4.4 会直接写出焦段与光学、机位方位与高度、摄影机路径与朝向变化、速度、焦点接力和动作落点，而不是只写“齿轮滑落”一类剧情标题。

这是已经回归验证的文字行为案例；它不代表视频模型已经完全执行，也不代表用户完成了成片审美验收。

- [查看完整 8 秒案例](examples/storyboard-director-5.4.4-visible-camera-plan.md)
- [读取正式运行合同](skills/ai-storyboard-director/SKILL.md)
- [查看当前证据状态](SKILL_CATALOG.md)

## Explore the visual language

这面参考墙展示 8 个已部署类型 Skill 和 1 个隔离实验 Skill 的可观察视觉重点。图片帮助人理解合同，不代替运行正文和真实项目验收。

<table>
<tr>
<td width="33%" valign="top"><a href="docs/skills/en/cyberpunk-design.md"><img src="docs/style-gallery/cyberpunk-design.jpg" width="100%" alt="赛博朋克街道维修场景，包含有来源的霓虹、湿地反射、阶层基础设施和人机接触" /></a><br /><strong><a href="docs/skills/en/cyberpunk-design.md">Cyberpunk</a></strong><br />功能性霓虹、不平等基础设施、潮湿材质反馈与维修劳动。</td>
<td width="33%" valign="top"><a href="docs/skills/en/epic-design.md"><img src="docs/style-gallery/epic-design.jpg" width="100%" alt="史诗沙漠队伍走向巨型岩石城塞，人物尺度、运动目的与尘光清晰" /></a><br /><strong><a href="docs/skills/en/epic-design.md">Epic</a></strong><br />人物渺小尺度、明确目的地、材料历史与可读运动。</td>
<td width="33%" valign="top"><a href="docs/skills/en/fantasy-design.md"><img src="docs/style-gallery/fantasy-design.jpg" width="100%" alt="奇幻旅人把紫色晶石放进森林观测池，魔法光源、空间层次与湿旧材质明确" /></a><br /><strong><a href="docs/skills/en/fantasy-design.md">Fantasy</a></strong><br />有来源的魔法光、分层世界空间与潮湿旧材质。</td>
</tr>
<tr>
<td width="33%" valign="top"><a href="docs/skills/en/horror-design.md"><img src="docs/style-gallery/horror-design.jpg" width="100%" alt="克制的医院走廊恐怖画面，手电光、湿脚印证据、负空间与镜面矛盾可读" /></a><br /><strong><a href="docs/skills/en/horror-design.md">Horror</a></strong><br />可读黑暗、局部证据、受控空间与不完整威胁。</td>
<td width="33%" valign="top"><a href="docs/skills/en/noir-design.md"><img src="docs/style-gallery/noir-design.jpg" width="100%" alt="黑色电影港口办公室，密封信封位于明暗边界，雨窗外有人等待" /></a><br /><strong><a href="docs/skills/en/noir-design.md">Noir</a></strong><br />实景光源、遮挡、道德张力与阴影边界证据。</td>
<td width="33%" valign="top"><a href="docs/skills/en/romance-design.md"><img src="docs/style-gallery/romance-design.jpg" width="100%" alt="雨天门口的克制爱情画面，两名成年人隔着冷暖光共同触碰修好的雨伞" /></a><br /><strong><a href="docs/skills/en/romance-design.md">Romance</a></strong><br />门槛距离、冷暖分离、共享物件接触与微情绪。</td>
</tr>
<tr>
<td width="33%" valign="top"><a href="docs/skills/en/war-design.md"><img src="docs/style-gallery/war-design.jpg" width="100%" alt="战争撤离场景，担架队、手势、可读路线、废墟地形与身体负荷明确" /></a><br /><strong><a href="docs/skills/en/war-design.md">War</a></strong><br />可读地形、人员协同、身体负荷与局部暖色。</td>
<td width="33%" valign="top"><a href="docs/skills/en/wuxia-design.md"><img src="docs/style-gallery/wuxia-design.jpg" width="100%" alt="水墨衍生的三维武侠山路，人物动作接地，亭台路径与克制红灯笼清楚" /></a><br /><strong><a href="docs/skills/en/wuxia-design.md">Wuxia</a></strong><br />深层路线几何、接地身体力学、水墨材质与单一强调色。</td>
<td width="33%" valign="top"><a href="docs/skills/en/hard-sci-fi-visual-director.md"><img src="docs/style-gallery/hard-sci-fi-visual-director.jpg" width="100%" alt="硬科幻月面居住舱门槛交接，压力密封、除尘磨损与人员操作逻辑明确" /></a><br /><strong><a href="docs/skills/en/hard-sci-fi-visual-director.md">Hard Sci-Fi</a></strong><br /><em>Experimental · self-audit only.</em> 物理门槛、材料操作与克制设备。</td>
</tr>
</table>

Seven frames were newly designed from the current Skill contracts; **two prior original atlas panels** were reused after an isolated-crop audit. This gallery is **not a claim that the Skill alone generated it** or that a user accepted the aesthetic result. [Inspect `docs/style-gallery/manifest.json`](docs/style-gallery/manifest.json) for provenance, hashes, inventory boundaries, and review state.

## 完整 Skill 地图

| 层级 | Skills | 当前状态 |
|---|---|---|
| 故事与导演 | `director-agent` · `ai-storyboard-director` | 已部署 |
| 资产定义 | `character-asset` · `scene-asset` · `prop-asset` | 已部署 |
| 类型视觉 | `cyberpunk` · `epic` · `fantasy` · `horror` · `noir` · `romance` · `war` · `wuxia` | 已部署 |
| 视频生产 | `produce-ai-video` | 已部署 |
| 短剧编排 | `ai-short-drama-production` | 已封装，尚未部署 |
| 产品与研究 | `web-design-director` · `d-official-market-analysis` · `d-data-analysis-semantic-layer` | 已部署 |
| 实验 | `hard-sci-fi-visual-director` | 与正常安装隔离，待用户视觉审阅 |

[打开完整目录、下载链接和逐项证据状态](SKILL_CATALOG.md)

## 安装一个 Skill 或完整工作室

| 只需要一项能力 | 需要完整工作室 |
|---|---|
| 从 [Skill 目录](SKILL_CATALOG.md) 选择一项，下载对应 ZIP，或使用安装器只复制该文件夹。 | 下载 [`open-film-skills-complete.zip`](https://github.com/62656456/ai-film-skills/releases/latest/download/open-film-skills-complete.zip)，按故事、资产、视觉、镜头、生产和验收逐阶段使用。 |
| 每个包都带自身运行引用，不需要保留整个仓库。 | 实验 Skill 不进入正常完整包，避免未批准能力被自动加载。 |

支持的宿主路径和边界：

| 宿主 | 安装方式 |
|---|---|
| Codex | `.codex/skills/<name>/` |
| Claude Code | `.claude/skills/<name>/` 或 `.claude/skills/<name>/` |
| TRAE | 项目内 `.agents/skills/<name>/` |
| CodeBuddy | `.codebuddy/skills/<name>/` |
| WorkBuddy | “添加技能 → 上传技能”导入独立 ZIP |
| 其他 Agent | 导入 `SKILL.md` 与包内本地引用；不把“能阅读指令”冒充原生发现或工具执行 |

详细路径、产品名核对和宿主限制见 [Agent 兼容说明](docs/COMPATIBILITY.md)。

## 状态和证据怎么读

- **已部署**：当前个人运行包正在使用，不等于已完成三个不同真实任务的稳定验证。
- **已封装**：结构达到分发要求，但当前没有部署。
- **实验中**：与正常安装隔离，明确保留未批准或未完成状态。
- **已淘汰**：故意不收录，不能从旧文件自动恢复。
- **第三方**：不当成个人原创再次发布。

仓库验证器会检查独立依赖、公开阅读路径、媒体哈希、图库来源、打包边界和文档结构；这些检查仍不能替代真实项目质量、视频模型执行和用户审美判断。

## English overview

Open Film Skills is a public toolkit of 19 independently installable Agent Skills for AI filmmaking. It separates story and directing, reusable assets, genre-specific visual language, executable storyboards, video production, and validation so each stage can be loaded, tested, replaced, and reviewed on its own.

- Start with [`director-agent`](docs/skills/en/director-agent.md) to write or repair the story.
- Use [`ai-storyboard-director`](docs/skills/en/ai-storyboard-director.md) to turn an approved scene into readable shots and a copy-ready generation prompt.
- Use [`produce-ai-video`](docs/skills/en/produce-ai-video.md) when an approved passage is ready for cost-gated generation, editing, full-playback review, and repair.
- Browse every module, runtime source, ZIP, and evidence state in the [Skill catalog](SKILL_CATALOG.md).

Each package is self-contained inside its stated outcome boundary. Structural validation, host execution, real-task evidence, media quality, and explicit user acceptance remain separate states.

## 贡献、安全与来源

- 提交修改前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 意外密钥或隐私问题通过 [SECURITY.md](SECURITY.md) 报告，不要公开到 Issue。
- 第三方排除与改编边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
- 公开发布范围见 [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md)。
- 反馈真实任务结果可使用 [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions)、[GitHub Issues](https://github.com/62656456/ai-film-skills/issues) 或 [反馈模板](docs/FEEDBACK.md)。

## License

除非文件另有声明，本仓库个人原创内容使用 [Apache License 2.0](LICENSE)。
