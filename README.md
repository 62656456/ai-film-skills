<div align="center">

<a href="docs/showcase/originals/xianxia-cloud-bell.png"><img src="docs/showcase/xianxia-cloud-bell.webp" width="100%" alt="《云海钟境》：本项目自主生成、用户已接受的仙侠画面；保持完整画幅，点击查看原始PNG" /></a>

*《云海钟境》｜项目自主生成、用户已接受；点击图片查看完整原图。*

# Open Film Skills｜开放影视技能

**从输入到可验收成片，让每个创作阶段有清楚的职责、交付和证据。**

*Independent Agent Skills for story, directing, visual assets, cinematography and AI-film production.*

[完整工作流](docs/WORKFLOW.md) · [14张用户接受成图](#本轮14张用户接受成图) · [全部20个技能](#全部20个独立技能) · [安装当前源码](docs/INSTALLATION.md#install-from-a-clone) · [版本与发布边界](#当前源码与下载版本) · [原创版权与商用](COMMERCIAL_USE.md)

**简体中文** · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [English overview](#english-overview)

![Regular packages](https://img.shields.io/badge/regular_packages-18-FF6B35?style=flat-square)
![Experimental packages](https://img.shields.io/badge/experimental_packages-2-D6A756?style=flat-square)
![Bilingual guides](https://img.shields.io/badge/bilingual_guides-40-7ED6A5?style=flat-square)
[![Validate Skills](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/62656456/ai-film-skills)](https://skills.sh/62656456/ai-film-skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-5B8CFF?style=flat-square)](LICENSE)

</div>

## 从输入到成片：完整工作流

![输入、剧本、导演方案、十种视觉路线、人物场景道具资产、5.6分镜与保存恢复、母提示词、可选白模、实际生成、剪辑声音、完整播放和用户验收](docs/assets/workflow-overview.svg)

[查看全部节点、交接与返回线](docs/WORKFLOW.md) · [下载完整Mermaid源图](docs/assets/production-workflow.mmd)

点子、小说、大纲、剧本、参考图或已有镜头都可以成为入口。已有可用成果就从相应阶段继续，按需选择主Skill；每项技能自带运行正文和必要引用，不要求先加载整个工作室。

完整工作流列出 **20项影视职责＋1项网页辅助**。其中外部仙侠只提供上游链接，本仓库实际分发 **18项常规＋2项实验＝20个模块**，对应 **40份英文/简体中文指南**。

## 当前源码与下载版本

| 入口 | 当前口径 |
|---|---|
| [当前源码](skills/ai-storyboard-director/SKILL.md) | 分镜入口为 **5.6.3**，已选择日常使用；增加紧凑提示词编译、打戏因果与受力设计，以及推进/变焦、横移/摇摄/环绕的按需诊断 |
| [已发布v1.3.0](https://github.com/62656456/ai-film-skills/releases/tag/v1.3.0) | **旧发布快照**，分镜是 **5.4.4**；源码更新不改变旧ZIP |
| 5.6独立Preview | 另有标签和清单的独立预览包，与当前源码及完整套装Release分别记录 |

本轮是源码与文档刷新，不能把它称为已经发布新Release。要用当前源码，请检查所取分支/提交与`SKILL.md`版本；旧Release适合明确复现旧快照。[安装选择与验证](docs/INSTALLATION.md)

## 全部20个独立技能

当前仓库收录 **18项常规包＋2项实验包**，下面逐项列出用途、源码版本和直接入口。版本列的“—”表示该包`SKILL.md`没有单独声明技能版本号，以实际Git提交和完整文件为准；不把模板中的资产版本、JSON协议版本或仓库Release号当成Skill版本。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `director-agent`<br/>编剧与导演 | 写作、改稿、对白与人物因果诊断；导演方案和条件式AI执行剧本 | — | 常规 | [运行正文](skills/director-agent/SKILL.md) · [中文说明](docs/skills/zh-CN/director-agent.md) |
| `ai-storyboard-director`<br/>分镜与摄影 | 将可用剧本设计为五列分镜和六模块母提示词；在作品目录保存恢复镜头决定 | 5.6.3 | 常规 | [运行正文](skills/ai-storyboard-director/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-storyboard-director.md) |
| `character-asset`<br/>人物资产 | 人物身份、外形、必要视图、表情与可变状态的参考任务和资产合同 | — | 常规 | [运行正文](skills/character-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/character-asset.md) |
| `scene-asset`<br/>场景资产 | 场景拓扑、空间锚点、光源、材质和连续性参考图/提示词 | — | 常规 | [运行正文](skills/scene-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/scene-asset.md) |
| `prop-asset`<br/>道具资产 | 道具结构、比例、可见面、持用和新旧状态；按要求交单图或必要视图 | — | 常规 | [运行正文](skills/prop-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/prop-asset.md) |
| `cyberpunk-design`<br/>赛博朋克 | 身体与技术关系、功能光源、空间层级和材质；不强制雨夜霓虹 | — | 常规 | [运行正文](skills/cyberpunk-design/SKILL.md) · [中文说明](docs/skills/zh-CN/cyberpunk-design.md) |
| `epic-design`<br/>史诗 | 地形、建筑、群体与个人代价共同建立尺度和画面秩序 | — | 常规 | [运行正文](skills/epic-design/SKILL.md) · [中文说明](docs/skills/zh-CN/epic-design.md) |
| `fantasy-design`<br/>奇幻 | 魔法来源、作用目标、世界规则和环境反馈的视觉参数 | — | 常规 | [运行正文](skills/fantasy-design/SKILL.md) · [中文说明](docs/skills/zh-CN/fantasy-design.md) |
| `horror-design`<br/>恐怖 | 可见异常证据、威胁显露、空间不安与可读暗部 | — | 常规 | [运行正文](skills/horror-design/SKILL.md) · [中文说明](docs/skills/zh-CN/horror-design.md) |
| `noir-design`<br/>黑色与犯罪 | 秘密、犯罪、关系压力和明暗信息；不以黑白滤镜替代剧情 | — | 常规 | [运行正文](skills/noir-design/SKILL.md) · [中文说明](docs/skills/zh-CN/noir-design.md) |
| `romance-design`<br/>爱情 | 距离、视线、接触和双向行动表达关系，不固定粉色、暖光或拥抱 | — | 常规 | [运行正文](skills/romance-design/SKILL.md) · [中文说明](docs/skills/zh-CN/romance-design.md) |
| `war-design`<br/>战争 | 地形、协同、负荷、行动与后果；检查武器方向和接触关系 | — | 常规 | [运行正文](skills/war-design/SKILL.md) · [中文说明](docs/skills/zh-CN/war-design.md) |
| `wuxia-design`<br/>武侠 | 兵器、步法、支撑、衣发反馈与东方空间的可观察参数 | — | 常规 | [运行正文](skills/wuxia-design/SKILL.md) · [中文说明](docs/skills/zh-CN/wuxia-design.md) |
| `produce-ai-video`<br/>实际视频生产 | 统筹实际生成、选片、剪辑、对白音效、完整播放审查与修复 | — | 常规 | [运行正文](skills/produce-ai-video/SKILL.md) · [中文说明](docs/skills/zh-CN/produce-ai-video.md) |
| `ai-short-drama-production`<br/>短剧控制 | 五列分镜＋一条六模块母提示词；5.6结构已对齐，文本验证通过，实片待验 | — | 常规；未部署 | [运行正文](skills/ai-short-drama-production/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-short-drama-production.md) |
| `web-design-director`<br/>网页辅助 | 明确网页或应用界面任务时设计与审核；仓库README维护不触发建站 | — | 常规 | [运行正文](skills/web-design-director/SKILL.md) · [中文说明](docs/skills/zh-CN/web-design-director.md) |
| `d-official-market-analysis`<br/>市场研究 | 根据当前可验证来源研究题材、平台、受众与制作机会，保留数据局限 | — | 常规 | [运行正文](skills/d-official-market-analysis/SKILL.md) · [中文说明](docs/skills/zh-CN/d-official-market-analysis.md) |
| `d-data-analysis-semantic-layer`<br/>知识审核与写入 | 用户批准后校验来源、版本、有效期与冲突，写入明确目标并回读 | — | 常规 | [运行正文](skills/d-data-analysis-semantic-layer/SKILL.md) · [中文说明](docs/skills/zh-CN/d-data-analysis-semantic-layer.md) |
| `hard-sci-fi-visual-director`<br/>硬科幻视觉 | 从物理、功能、制造与环境推导原创世界、设备、形体和完整提示词 | — | 实验 | [运行正文](experimental/hard-sci-fi-visual-director/SKILL.md) · [中文说明](docs/skills/zh-CN/hard-sci-fi-visual-director.md) |
| `whitebox-previs-executor`<br/>3D白模预演 | 将已有镜头编译成可播放机位与基础走位预演；打斗限已实现且过门的动作 | — | 实验 | [运行正文](experimental/whitebox-previs-executor/SKILL.md) · [中文说明](docs/skills/zh-CN/whitebox-previs-executor.md) |

**分发状态与完成证据分开。** 常规包不表示所有能力已通过实战；实验硬科幻已有接受图例，白模仍有明确能力限制。短剧控制器已在仓库源码对齐5.6交付结构，独立文本行为样本经修正后最终通过；仍未部署、未生成视频、未获用户实际效果验收，不新增独立版本号。其余实际使用和验收边界见各自运行正文与说明。

外部[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director)只作为仙侠工作流入口，不属于这20个源码包、不进本仓库ZIP；《云海钟境》是本项目自主生成并已接受的示例图，图的发布不等于再分发外部技能源码。

## 安装当前源码中的一个Skill

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
git log -1 --oneline
python scripts/install_skill.py --list
python scripts/install_skill.py ai-storyboard-director --platform codex
```

安装器使用当前检出的源码；公共默认分支不会自动包含未推送的本地修改。安装前查看所选源码版本，然后在Agent中调用：

```text
使用 $ai-storyboard-director，把下面剧本设计成人读分镜和一条完整视频母提示词。
保留已确认剧情、人物与台词；镜头标题直接显示具体摄影方案。
如果我提供了作品目录，请实际保存导演意图、选中镜头和场景状态，并核对恢复结果。
[粘贴剧本与已有约束]
```

也可用Skills CLI查看公共仓库的可发现条目，再按需要安装；该路线读取公共来源，不会取得未推送的本地修改：

```bash
npx --yes skills@latest add 62656456/ai-film-skills --list
npx --yes skills@latest add 62656456/ai-film-skills --skill ai-storyboard-director --agent codex --copy --yes
```

[skills.sh公开目录](https://skills.sh/62656456/ai-film-skills)显示平台自己的安装统计，其中包含维护者验证，不等于独立外部用户数。

其他宿主、历史ZIP与实验包的明确安装方式见[安装指南](docs/INSTALLATION.md)和[兼容边界](docs/COMPATIBILITY.md)。Skills CLI的[旧版发现与复制记录](examples/skills-cli-install-verification.md)保留为历史证据，不冒充本轮5.6宿主行为测试。

## 本轮14张用户接受成图

以下均为原创生成结果，用户已逐批明确接受。预览保留完整画幅，点击进入原始PNG；没有裁切成卡片来隐藏边缘。包括8类型、5张硬科幻与1张仙侠；仙侠技能本体来自外部，仅链接上游，图是本轮授权生成的原创成果。

<table>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/cyberpunk-after-the-new-eye.png"><img src="docs/showcase/cyberpunk-after-the-new-eye.webp" width="100%" alt="赛博朋克：身体、技术与人的处境；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《换眼之后》</strong><br />赛博朋克：身体、技术与人的处境。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/epic-open-gates.png"><img src="docs/showcase/epic-open-gates.webp" width="100%" alt="史诗：群体规模与门前的个人命运；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《开门》</strong><br />史诗：群体规模与门前的个人命运。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/fantasy-mending-the-bridge.png"><img src="docs/showcase/fantasy-mending-the-bridge.webp" width="100%" alt="奇幻：魔法作用、石桥与跨越；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《重续断桥》</strong><br />奇幻：魔法作用、石桥与跨越。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/horror-upstairs-visitor.png"><img src="docs/showcase/horror-upstairs-visitor.webp" width="100%" alt="恐怖：可读空间中的异常证据；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《楼上的访客》</strong><br />恐怖：可读空间中的异常证据。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/noir-before-the-money.png"><img src="docs/showcase/noir-before-the-money.webp" width="100%" alt="黑色：证据、封口费与未完成交易；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《收钱之前》</strong><br />黑色：证据、封口费与未完成交易。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/romance-tilted-umbrella.png"><img src="docs/showcase/romance-tilted-umbrella.webp" width="100%" alt="爱情：系鞋与偏伞的双向照顾；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《把伞偏过去》</strong><br />爱情：系鞋与偏伞的双向照顾。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-river-crossing.png"><img src="docs/showcase/war-river-crossing.webp" width="100%" alt="战争：负荷、协同与渡河行动；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《渡河》</strong><br />战争：负荷、协同与渡河行动。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/wuxia-tea-still-warm.png"><img src="docs/showcase/wuxia-tea-still-warm.webp" width="100%" alt="武侠：日常空间中的兵器与关系压力；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《茶未凉》</strong><br />武侠：日常空间中的兵器与关系压力。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/hard-scifi-orbital-morning.png"><img src="docs/showcase/hard-scifi-orbital-morning.webp" width="100%" alt="硬科幻：轨道生活与细小照料；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《环城清晨》</strong><br />硬科幻：轨道生活与细小照料。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/hard-scifi-lunar-lightfield.png"><img src="docs/showcase/hard-scifi-lunar-lightfield.webp" width="100%" alt="硬科幻：月面系统、尺度与日照；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《极昼镜阵》</strong><br />硬科幻：月面系统、尺度与日照。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/hard-scifi-titan-harbor.png"><img src="docs/showcase/hard-scifi-titan-harbor.webp" width="100%" alt="硬科幻：环境与装备形态；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《泰坦泊岸》</strong><br />硬科幻：环境与装备形态。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/hard-scifi-mars-first-harvest.png"><img src="docs/showcase/hard-scifi-mars-first-harvest.webp" width="100%" alt="硬科幻：农业系统与收获；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《火星的第一颗番茄》</strong><br />硬科幻：农业系统与收获。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/hard-scifi-europa-underice.png"><img src="docs/showcase/hard-scifi-europa-underice.webp" width="100%" alt="硬科幻：冰下环境与探测；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《冰壳下的来客》</strong><br />硬科幻：冰下环境与探测。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/xianxia-cloud-bell.png"><img src="docs/showcase/xianxia-cloud-bell.webp" width="100%" alt="仙侠：外部技能路线的原创成图；用户已接受的原创单幅成图，点击查看原始完整画幅" /></a><br /><strong>《云海钟境》</strong><br />仙侠：外部技能路线的原创成图。</td>
</tr>
</table>

[查看逐文件来源、版本、哈希与接受记录](docs/showcase/manifest.json)。这14张证明相应图例已通过用户审阅；没有旧版同题A/B，不能据此宣称量化升级、所有题材稳定成功或视频执行通过。

## 本轮视觉方法更新了什么

视觉与资产模块先确定成像方式和观看命题，再联合设计主体分离、光源及反射、空间尺度、材料差异和细节层次。每包都带自己的画面关系参考，单独复制仍可读取。

- 配色、焦段、光比、浅景深、前景人物和黄金时刻是可选设计，不是万能要求。
- 摄影写实、三维动画、二维动画/插画采用各自的失败标准；新物、真实塑料和设计发光不被通用负向误杀。
- 用户只要单图或提示词时，先交付点名结果；真实像素检查、连续视频检查和用户决定分别记录。

这些方法是本项目对用户供图关系分析的原创综合，不声称反推出第三方Skill、模型或未提供的摄影参数。

## 2026-09-11 源码研究增量

- `ai-storyboard-director` 5.6.3 仍保持一个分镜入口：普通任务按阶段读取；打戏另读攻防、接触阻力、节奏和摄影设计；只有用户要求运镜对照或诊断时，才读取推进/变焦与横移/摇摄/环绕的可见证据方法。内部格式、隔离和文本回归通过；真实视频和用户审美仍待验。
- 人物、场景和道具资产先通读剧本并区分明示事实与设计推定。人物默认交三面全身加中景，女性魅力按任务读取独立参考；场景无指定画风时默认摄影写实，并从用途、使用者、维护、天气和事件痕迹推导可信环境；道具继续围绕功能、接触和状态变化设计。
- `war-design` 1.0.0 合并战争类型视觉与军事顾问方法，覆盖故事关键帧、战斗、小队摄影和实际画面审查；它不认证真实战术、装备性能或任意视频结果。
- `web-design-director` 1.3.0 将优秀成品观察、开源实现与许可核对连接到具体设计机制，并把任务走查、布局实用性、材质、动效和交互恢复分开验证。本次升级获用户确认，不等同于跨项目、跨设备或真人研究结论。

本增量只更新源码和双语说明，不创建新Release、不改写v1.3.0附件，也不上传私有测试媒体、候选成片或第三方无授权源码。

## See the Skills in motion

历史预演证据展示了可观看的机位、走位与短动作门，保留原验收范围：

<table>
<tr>
<td width="50%" valign="top"><a href="https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4"><img src="docs/media/previs-blocking-preview.gif" width="100%" alt="5秒基础3D摄影机和走位预演" /></a><br /><strong>基础机位与走位 · 5秒</strong></td>
<td width="50%" valign="top"><a href="https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4"><img src="docs/media/rigged-contact-preview.gif" width="100%" alt="2.8秒骨骼接触动作门" /></a><br /><strong>骨骼接触动作门 · 2.8秒</strong></td>
</tr>
</table>

白模执行器现作为源码中的独立实验包列出；这些历史片段证明有限预演与动作门，不证明任意完整打斗、最终AI成片或新的用户接受。[媒体清单](docs/media/media-manifest.json)

[旧5.4.4文字行为案例](examples/storyboard-director-5.4.4-visible-camera-plan.md)和[历史视觉参考墙](docs/style-gallery/manifest.json)仍可查看，保留各自日期与原状态，不与本轮14张接受成图混记。

## 模块和证据边界

常规包可单独使用；实验硬科幻与白模不进入默认完整套装。已封装的短剧控制器已在仓库源码对齐5.6交付结构，仍未部署；文本验证不替代真实视频和用户验收。外部仙侠没有已核实再分发许可，因此不复制源码、不进ZIP；完整职责见[工作流](docs/WORKFLOW.md)。

结构有效、宿主实际加载、真实任务输出、媒体检查与用户接受是不同证据。5.6的状态程序不评审美，不替代实际读剧本，也不能强制所有聊天入口执行。费用、账户、工具和发布权限由实际任务与宿主决定。

[20模块目录](SKILL_CATALOG.md) · [40份设计指南](docs/skills/INDEX.md) · [共同审核逻辑](docs/SKILL_DESIGN_SYSTEM.md) · [分发范围](PUBLICATION_SCOPE.md)

## English overview

Open Film Skills provides **20 self-contained modules: 18 regular and 2 experimental**, with 40 English/Simplified Chinese guides. The [full workflow](docs/WORKFLOW.md) covers input, writing, directing, visual language, assets, shots, prompts, optional previs, actual video production, sound, playback review and acceptance. It lists one external xianxia workflow entry without redistributing its source.

Current source uses Storyboard Director 5.6.3. Published v1.3.0 ZIPs preserve the historical 5.4.4 snapshot; the separately labeled 5.6 Preview is another artifact. Source updates do not publish a new Release. The 2026-09-11 source increment adds compact prompt compilation, fight design, camera-motion diagnostics, script-first asset derivation, unified war-film visual methods, and research-to-design web guidance with explicit evidence limits. The primary showcase contains 14 original images explicitly accepted by the user, displayed without cropping; it is not a measured old/new A/B study or a guarantee of general reliability.

Start with the [catalog](SKILL_CATALOG.md), [source installation](docs/INSTALLATION.md) or [per-module English guides](docs/skills/INDEX.md).

## 贡献、来源与许可

[贡献说明](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [第三方说明](THIRD_PARTY_NOTICES.md) · [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions) · [Issues](https://github.com/62656456/ai-film-skills/issues)

本仓库原创Skill、脚本、文档、提示词和明确项目自主生成的示例，在权利人有权许可的范围内按[Apache License 2.0](LICENSE)允许个人与商业使用、修改、集成和再分发；保留适用许可说明、注明文件变更，不要求衍生项目全部开源。本轮14图属于项目原创AI辅助样本，并经人工参与设计、筛选、修订与接受；不承诺AI输出独一无二。新作品仍需遵守实际平台条款与输入素材、肖像、商标等权利，外部仙侠链接不授予其源码许可。

[阅读完整原创版权与商用说明](COMMERCIAL_USE.md) · [第三方范围](THIRD_PARTY_NOTICES.md)
