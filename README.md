<div align="center">

# Open Film Skills｜开放影视技能

**把故事变成可执行的导演、资产、镜头与制作方案，让每个阶段都有能直接使用的结果。**

*Independent Agent Skills for story, directing, visual assets, cinematography and AI-film production.*

[技能与工作流程](#overview) · [功能与实际成果](#features) · [版本更新](#updates) · [完整技能目录](SKILL_CATALOG.md)

**简体中文** · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [English overview](#english-overview)

![Regular packages](https://img.shields.io/badge/regular_packages-18-FF6B35?style=flat-square)
![Experimental packages](https://img.shields.io/badge/experimental_packages-3-D6A756?style=flat-square)
![Bilingual guides](https://img.shields.io/badge/bilingual_guides-42-7ED6A5?style=flat-square)
[![Validate Skills](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/62656456/ai-film-skills)](https://skills.sh/62656456/ai-film-skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-5B8CFF?style=flat-square)](LICENSE)

</div>

<a id="overview"></a>

## 1. 技能介绍与完整工作流程

这套技能服务于影视创作中的具体工作：写故事和对白、形成导演方案、设计人物场景道具、安排摄影与分镜、编写生成提示词，以及组织实际视频制作与看片修复。你可以从点子、小说、剧本、参考图或已经确定的镜头开始，直接调用当前阶段需要的技能。

仓库提供 **18项常规包＋3项实验包＝21个独立模块**，配有42份英文／简体中文指南。每个包自带运行正文与必要引用，可以单独使用。完整工作流另列外部仙侠入口，因此图中是21项影视职责＋1项网页辅助；外部入口不计入本仓库源码包。

<a id="从输入到成片完整工作流"></a>

**输入 → 剧本与导演判断 → 视觉方向与资产 → 分镜与摄影 → 生成提示词 → 按需预演或实际生成 → 剪辑、声音、完整看片与修复。**

<a href="docs/research/skill-overhaul/workflows/active-a.svg"><img src="docs/research/skill-overhaul/workflows/active-a.svg" width="100%" alt="A方案完整技能工作流程：各阶段入口、职责、交接物、检查与返回路径；点击查看可放大的SVG" /></a>

[打开完整工作流与三版关系](docs/research/skill-overhaul/workflows/index.md) · [三套工作流并排总图](docs/research/skill-overhaul/workflows/compare-all.svg) · [逐节点职责说明](docs/WORKFLOW.md) · [原始Mermaid源图](docs/assets/production-workflow.mmd)

已有可用导演方案就直接编排分镜；已有锁定镜头就沿用其摄影和动作。创意思路、可读分镜、视频提示词、实际媒体分别交付，后续阶段按明确请求进入。实际视频还需要可调用的生成工具、相应授权、完整播放检查和用户验收。

<a id="features"></a>

## 2. 功能、实现目的与实际成果

### 按你要完成的事选入口

| 你要完成的事 | 技能怎样帮助 | 直接入口 |
|---|---|---|
| 写出能推进剧情的场景、对白和导演方案 | 检查人物目的、行动、因果、信息顺序与表演，修具体问题 | [编剧与导演](docs/skills/zh-CN/director-agent.md) |
| 让人物、场景、道具成为可重复使用的资产 | 从剧情和使用方式确定外观、空间、状态与必要视图 | [人物](docs/skills/zh-CN/character-asset.md) · [场景](docs/skills/zh-CN/scene-asset.md) · [道具](docs/skills/zh-CN/prop-asset.md) |
| 把故事拍成具体镜头 | 设计观看顺序、调度、景别机位、光学、运动、声音和切点 | [分镜与摄影](docs/skills/zh-CN/ai-storyboard-director.md) |
| 为同一故事寻找不同拍法 | 交创意思路、叙事作用和取舍，采用后再并入主方案 | [三版测试与融合研究](docs/research/skill-overhaul/index.md) |
| 选出符合故事的视觉语言 | 分别处理类型、光色、材料、尺度和构图，保留真实图例与待修处 | [类型目录](SKILL_CATALOG.md#genre-visual-language) · [视觉研究](docs/research/visual/index.md) |
| 生成前检查机位、视差和基础走位 | 把已写好的镜头做成有限范围的可播放3D预演 | [白模实验包](experimental/whitebox-previs-executor/SKILL.md) · [实际预演](docs/research/whitebox/index.md) |
| 交付可观看的AI视频 | 组织生成、选片、剪辑、声音、完整看片和返修 | [实际视频生产](docs/skills/zh-CN/produce-ai-video.md) |
| 研究题材或搭建创作工具 | 基于可验证来源研究市场；按请求处理知识写入或网页界面 | [市场研究](docs/skills/zh-CN/d-official-market-analysis.md) · [知识审核](docs/skills/zh-CN/d-data-analysis-semantic-layer.md) · [网页辅助](docs/skills/zh-CN/web-design-director.md) |

### 分镜与摄影：七题材、三版、21张首轮测试图

七个全新原创故事分别交给测试时默认5.6.5、A5.7.1、B5.7.1-jev独立设计，得到 **21套30秒分镜、149个镜头和21张实际分镜图**。题材涵盖悬疑、恐怖、爱情、近身打戏、枪战、赛车追逐与超能力动作。

**这批是首轮测试图，尚未获得整批审美通过。** 逐图检查记录中，15张存在明确或限定范围的待修观察，共29条；其余6张本轮未发现足以确认的硬冲突，也不因此记为通过。换手、道具状态、人物复制、破损位置与空间关系等问题和原图一起保留。

[按题材切换查看高清三版对照](docs/research/skill-overhaul/seven-genres/viewer.html) · [全部原图、故事、分镜、生成提示词与逐图问题](docs/research/skill-overhaul/seven-genres/index.md)

<table>
<tr><th colspan="3">悬疑 ·《背过身的镜子》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/01-suspense-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/01-suspense-current.png" width="100%" alt="悬疑《背过身的镜子》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/01-suspense-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/01-suspense-a.png" width="100%" alt="悬疑《背过身的镜子》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/01-suspense-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/01-suspense-b.png" width="100%" alt="悬疑《背过身的镜子》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">恐怖 ·《最后一排床单》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/02-horror-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/02-horror-current.png" width="100%" alt="恐怖《最后一排床单》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/02-horror-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/02-horror-a.png" width="100%" alt="恐怖《最后一排床单》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/02-horror-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/02-horror-b.png" width="100%" alt="恐怖《最后一排床单》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">爱情 ·《下一班也可以》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/03-romance-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/03-romance-current.png" width="100%" alt="爱情《下一班也可以》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/03-romance-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/03-romance-a.png" width="100%" alt="爱情《下一班也可以》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/03-romance-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/03-romance-b.png" width="100%" alt="爱情《下一班也可以》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">近身打戏 ·《桥上只过一个人》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/04-fight-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/04-fight-current.png" width="100%" alt="近身打戏《桥上只过一个人》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/04-fight-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/04-fight-a.png" width="100%" alt="近身打戏《桥上只过一个人》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/04-fight-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/04-fight-b.png" width="100%" alt="近身打戏《桥上只过一个人》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">枪战 ·《关门之前》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/05-gunfight-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/05-gunfight-current.png" width="100%" alt="枪战《关门之前》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/05-gunfight-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/05-gunfight-a.png" width="100%" alt="枪战《关门之前》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/05-gunfight-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/05-gunfight-b.png" width="100%" alt="枪战《关门之前》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">赛车追逐 ·《松开的油门》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/06-racing-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/06-racing-current.png" width="100%" alt="赛车追逐《松开的油门》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/06-racing-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/06-racing-a.png" width="100%" alt="赛车追逐《松开的油门》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/06-racing-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/06-racing-b.png" width="100%" alt="赛车追逐《松开的油门》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
<tr><th colspan="3">超能力动作 ·《逆坠》</th></tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/07-superpower-current.png"><img src="docs/research/skill-overhaul/seven-genres/images/07-superpower-current.png" width="100%" alt="超能力动作《逆坠》测试时默认 5.6.5的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>测试时默认 5.6.5</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/07-superpower-a.png"><img src="docs/research/skill-overhaul/seven-genres/images/07-superpower-a.png" width="100%" alt="超能力动作《逆坠》A 5.7.1的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>A 5.7.1</strong></td>
<td width="33%" valign="top"><a href="docs/research/skill-overhaul/seven-genres/images/07-superpower-b.png"><img src="docs/research/skill-overhaul/seven-genres/images/07-superpower-b.png" width="100%" alt="超能力动作《逆坠》B 5.7.1-jev的30秒首轮分镜图；验收与待修情况见逐图报告，点击查看完整原图" /></a><br/><strong>B 5.7.1-jev</strong></td>
</tr>
</table>

这些图片使用统一图像模型；A/B参照同题基准图的人物与场景外观，仍可能继承图像模型的姿态、构图或错误。本轮不构成严格盲测，不按镜数、术语量、问题条数或记录耗时给技能排名；静图也不能证明实际运镜和完整动作已执行。

### 同题融合：保留有效拍法，再检查衔接

《修表铺外》把5.6.5的交接细节、A的仰摇与观察方式放进同一方案。用户已明确选择末镜直接看男子本人走进巷口；这个具体选择不等于其余融合方案或整套技能都通过。研究保留旧版、A、局部修订、融合图与对应文字。

<a href="docs/research/skill-overhaul/fusion/fusion-storyboard.png"><img src="docs/research/skill-overhaul/fusion/fusion-storyboard.png" width="100%" alt="《修表铺外》融合候选导演故事分镜；末镜直接观看真人为用户已选决定，其余观看效果仍分别待验" /></a>

[看完整融合过程、原稿、图片与文字复核](docs/research/skill-overhaul/fusion/index.md) · [查看全部整改研究](docs/research/skill-overhaul/index.md)

A/B共用创作核心。A由当前主模型检查，B可选增加Jev对明确文字要求的核对；Jev本轮没有接收图片像素或连续视频。文字核对结果和逐图检查分别记录。

### 视觉与资产：历史21张已接受作品

<a id="本轮21张用户接受视觉成果"></a>

这组是此前已获用户接受的作品，和上方21张首轮分镜测试属于**不同批次**。原图与接受范围继续保留，不用旧成果的接受状态替新版本测试背书。

<details>
<summary>展开历史21张作品：19张原创静帧与2张LUMEN界面截图</summary>

以下历史19张是原创生成静帧，另有2张是原创LUMEN界面的真实浏览器截图；用户均已逐批明确接受。预览保持原始比例，点击进入原始PNG，没有裁切成卡片来隐藏边缘。仙侠技能本体来自外部，仅链接上游，图是原展示批次授权生成的原创成果。

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
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-bold-black-shadow-advance.png"><img src="docs/showcase/war-bold-black-shadow-advance.webp" width="100%" alt="战争小队：工业夜景中的四人纵深与暴露边缘；用户已接受，点击查看原始完整画幅" /></a><br /><strong>《黑影前行》</strong><br />贴地广角、实用光源和四人差异化动作。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-bold-suspended-city-landing.png"><img src="docs/showcase/war-bold-suspended-city-landing.webp" width="100%" alt="战争小队：高楼外立面的垂直接力；用户已接受，点击查看原始完整画幅" /></a><br /><strong>《悬城落点》</strong><br />高差、绳索承托、器材负荷和协作关系。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-bold-red-sand-contact.png"><img src="docs/showcase/war-bold-red-sand-contact.webp" width="100%" alt="战争小队：红砂路堑的近距离交锋；用户已接受，点击查看原始完整画幅" /></a><br /><strong>《赤沙交锋》</strong><br />过肩近景、局部碎屑和不同步的队员反应。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-bold-floodgate-blue.png"><img src="docs/showcase/war-bold-floodgate-blue.webp" width="100%" alt="战争小队：潮门下涉水搬运器材；用户已接受，点击查看原始完整画幅" /></a><br /><strong>《潮门幽蓝》</strong><br />水阻、低矮障碍、共同承重和警戒分工。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/war-bold-snowline-backlight.png"><img src="docs/showcase/war-bold-snowline-backlight.webp" width="100%" alt="战争小队：雪线逆光中的分层攀登；用户已接受，点击查看原始完整画幅" /></a><br /><strong>《雪线逆光》</strong><br />雪地阻力、错落队形、援手和明确目的地。</td>
<td width="50%" valign="top"><a href="docs/showcase/originals/web-design-lumen-desktop-confirmed.png"><img src="docs/showcase/web-design-lumen-desktop-confirmed.webp" width="100%" alt="网页设计：LUMEN桌面端收藏回访界面；用户已接受，点击查看原始截图" /></a><br /><strong>LUMEN·桌面端</strong><br />收藏结果、再次回访入口和本地保存边界同时可见。</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/showcase/originals/web-design-lumen-mobile-favorites.png"><img src="docs/showcase/web-design-lumen-mobile-favorites.webp" width="100%" alt="网页设计：LUMEN手机端收藏回访界面；用户已接受，点击查看原始截图" /></a><br /><strong>LUMEN·手机端</strong><br />390像素宽度下保留收藏、身份和回访路径。</td>
</tr>
</table>

[查看逐文件来源、版本、哈希与接受记录](docs/showcase/manifest.json)。这21张证明对应静帧或界面结果已通过用户审阅；五张战争小队图来自一次接受批次，两张LUMEN截图来自一次接受的界面交付，不能据此宣称跨任务稳定、真人可用性研究、所有题材成功或视频执行通过。

</details>

### 视觉与预演：继续公开研究过程

历史研究包含26张原创候选图、7组视频展示（8个完整MP4）和3份可编辑白模工程。下面按它们解决的视觉与制作问题展示；研究候选、已接受单幅作品、实际视频与有限预演各自保留原来的证据范围。

[研究结论与后续问题](docs/RESEARCH.md) · [全部研究图与提示词](docs/research/visual/index.md) · [全部白模与生成对照](docs/research/whitebox/index.md)

#### 3D 白模：动作重排与多镜切换

<table>
<tr>
<td width="50%" valign="top"><a href="docs/research/whitebox/action-reblock-30s.mp4"><img src="docs/research/whitebox/action-reblock-30s.gif" width="100%" alt="30秒动作重排与连续摄影机预演，完整时长低帧率预览" /></a><br/><strong>动作重排 · 30 秒 · 9/19</strong><br/>重新安排脚步、转身、手势与队伍展开，检查它们和连续运镜是否接得上。<br/><a href="docs/research/whitebox/action-reblock-30s.mp4">观看完整 MP4</a></td>
<td width="50%" valign="top"><a href="docs/research/whitebox/minimal-shots-30s.mp4"><img src="docs/research/whitebox/minimal-shots-30s.gif" width="100%" alt="30秒11镜极简白模，完整时长低帧率预览" /></a><br/><strong>极简分镜 · 30 秒 / 11 镜 · 9/18</strong><br/>用必要的代理形体检查站位、视线、走位、切镜和注意力变化。<br/><a href="docs/research/whitebox/minimal-shots-30s.mp4">观看完整 MP4</a></td>
</tr>
</table>

两条均为历史研究候选；GIF 保留完整时长，降低帧率与分辨率便于首页观看。它们展示简化关节代理和摄影实验，动作与审美仍待审；不证明最终 AI 成片。20 秒早期失败实验也保留在[研究演进页](docs/research/whitebox/index.md)。

#### 从白模到生成片：看哪里继承、哪里偏离

https://github.com/user-attachments/assets/951b5ff1-86e0-4629-b6cc-c3e3d915c9e0

赛车案例把原白模与实际生成片上下对照，并配中文讲解。**原设计为 15 秒，生成时误选约 30 秒**；12.5–27.375 秒没有对应的原白模镜头，保留完整结果供检查。[完整视频、对应关系与许可说明](docs/research/whitebox/index.md)

<details>
<summary>展开观看三组完整原白模：追逐、博弈、棍术</summary>

**高速追击 · 15 秒 / 6 镜**

https://github.com/user-attachments/assets/7bbea66b-d855-47c4-a7b0-b628bbd7d208

**权力博弈 · 30 秒 / 8 镜**

https://github.com/user-attachments/assets/be73270a-9cea-49a4-b421-39b2ea15abd8

**棍术打戏 · 15 秒 / 7 镜**

https://github.com/user-attachments/assets/fef933aa-eee3-40b9-8930-feb019b4e507

[每组完整 MP4、参考图和实际提示词](docs/research/whitebox/index.md) · [可运行案例与交互预演台](https://github.com/62656456/ai-visual-previs-lab)

</details>

#### 六种视觉风格：人物、环境和材质共同变化

<table>
<tr>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-film-realism.png"><img src="docs/research/visual/previews/style-film-realism.webp" width="100%" alt="胶片诗意写实，完整画幅的研究候选" /></a><br/><strong>胶片诗意写实</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-mineral-painting.png"><img src="docs/research/visual/previews/style-mineral-painting.webp" width="100%" alt="东方岩彩，完整画幅的研究候选" /></a><br/><strong>东方岩彩</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-copperplate-etching.png"><img src="docs/research/visual/previews/style-copperplate-etching.webp" width="100%" alt="铜版线刻，完整画幅的研究候选" /></a><br/><strong>铜版线刻</strong></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-paper-theatre.png"><img src="docs/research/visual/previews/style-paper-theatre.webp" width="100%" alt="纸雕剧场，完整画幅的研究候选" /></a><br/><strong>纸雕剧场</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-needle-felt-v2.png"><img src="docs/research/visual/previews/style-needle-felt-v2.webp" width="100%" alt="羊毛毡定格感 · v2，完整画幅的研究候选" /></a><br/><strong>羊毛毡定格感 · v2</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/style-glazed-porcelain.png"><img src="docs/research/visual/previews/style-glazed-porcelain.webp" width="100%" alt="釉彩瓷偶，完整画幅的研究候选" /></a><br/><strong>釉彩瓷偶</strong></td>
</tr>
</table>

胶片诗意写实、东方岩彩、铜版线刻、纸雕剧场、羊毛毡定格感与釉彩瓷偶，围绕相近题材进行探索。研究得到的具体方法是：风格规则必须覆盖人物和环境；羊毛毡版本针对水面进行了单独修订，避免真实液体与纤维世界混杂。六图为静态研究候选。[完整图、可复制提示词与风格规则](docs/research/visual/index.md)

#### 古风真实感：让人物与环境处在同一束光里

<table>
<tr>
<td width="33%" valign="top"><a href="docs/research/visual/originals/guofeng-window-letter.png"><img src="docs/research/visual/previews/guofeng-window-letter.webp" width="100%" alt="窗边家书 · 窗光，完整画幅的研究候选" /></a><br/><strong>窗边家书 · 窗光</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/guofeng-seedling-handoff.png"><img src="docs/research/visual/previews/guofeng-seedling-handoff.webp" width="100%" alt="田埂递秧 · 阴天，完整画幅的研究候选" /></a><br/><strong>田埂递秧 · 阴天</strong></td>
<td width="33%" valign="top"><a href="docs/research/visual/originals/guofeng-market-eaves.png"><img src="docs/research/visual/previews/guofeng-market-eaves.webp" width="100%" alt="檐下挑货 · 光影交界，完整画幅的研究候选" /></a><br/><strong>檐下挑货 · 光影交界</strong></td>
</tr>
</table>

从“色彩与故事感成立、真实感不足”的六朝首图出发，继续修订肤色、照明与材质，再以窗边家书、田埂递秧、檐下挑货验证新的生活场景。新图仍待审阅。[六朝原图→修订对照与三张新场景](docs/research/visual/index.md) · [古风技能 0.1.1 候选源码](experimental/guofeng-visual-director/SKILL.md)

### 全部21个独立技能

当前仓库收录 **18项常规包＋3项实验包**，下面逐项列出用途、源码版本和直接入口。版本列的“—”表示该包`SKILL.md`没有单独声明技能版本号，以实际Git提交和完整文件为准；不把模板中的资产版本、JSON协议版本或仓库Release号当成Skill版本。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `director-agent`<br/>编剧与导演 | 写作、改稿、对白与人物因果诊断；导演方案和条件式AI执行剧本 | — | 常规 | [运行正文](skills/director-agent/SKILL.md) · [中文说明](docs/skills/zh-CN/director-agent.md) |
| `ai-storyboard-director`<br/>分镜与摄影 | 按请求设计可读分镜或编译六模块提示词；在作品目录保存恢复镜头决定 | 5.7.1 | 常规 | [运行正文](skills/ai-storyboard-director/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-storyboard-director.md) |
| `character-asset`<br/>人物资产 | 人物身份、外形、必要视图、表情与可变状态的参考任务和资产合同 | — | 常规 | [运行正文](skills/character-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/character-asset.md) |
| `scene-asset`<br/>场景资产 | 场景拓扑、空间锚点、光源、材质和连续性参考图/提示词 | — | 常规 | [运行正文](skills/scene-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/scene-asset.md) |
| `prop-asset`<br/>道具资产 | 道具结构、比例、可见面、持用和新旧状态；按要求交单图或必要视图 | — | 常规 | [运行正文](skills/prop-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/prop-asset.md) |
| `cyberpunk-design`<br/>赛博朋克 | 身体与技术关系、功能光源、空间层级和材质；不强制雨夜霓虹 | — | 常规 | [运行正文](skills/cyberpunk-design/SKILL.md) · [中文说明](docs/skills/zh-CN/cyberpunk-design.md) |
| `epic-design`<br/>史诗 | 地形、建筑、群体与个人代价共同建立尺度和画面秩序 | — | 常规 | [运行正文](skills/epic-design/SKILL.md) · [中文说明](docs/skills/zh-CN/epic-design.md) |
| `fantasy-design`<br/>奇幻 | 魔法来源、作用目标、世界规则和环境反馈的视觉参数 | — | 常规 | [运行正文](skills/fantasy-design/SKILL.md) · [中文说明](docs/skills/zh-CN/fantasy-design.md) |
| `horror-design`<br/>恐怖 | 可见异常证据、威胁显露、空间不安与可读暗部 | — | 常规 | [运行正文](skills/horror-design/SKILL.md) · [中文说明](docs/skills/zh-CN/horror-design.md) |
| `noir-design`<br/>黑色与犯罪 | 秘密、犯罪、关系压力和明暗信息；不以黑白滤镜替代剧情 | — | 常规 | [运行正文](skills/noir-design/SKILL.md) · [中文说明](docs/skills/zh-CN/noir-design.md) |
| `romance-design`<br/>爱情 | 距离、视线、接触和双向行动表达关系，不固定粉色、暖光或拥抱 | — | 常规 | [运行正文](skills/romance-design/SKILL.md) · [中文说明](docs/skills/zh-CN/romance-design.md) |
| `war-design`<br/>战争 | 地形、协同、负荷、行动与后果；检查武器方向和接触关系 | 1.0.0 | 常规 | [运行正文](skills/war-design/SKILL.md) · [中文说明](docs/skills/zh-CN/war-design.md) |
| `wuxia-design`<br/>武侠 | 兵器、步法、支撑、衣发反馈与东方空间的可观察参数 | — | 常规 | [运行正文](skills/wuxia-design/SKILL.md) · [中文说明](docs/skills/zh-CN/wuxia-design.md) |
| `produce-ai-video`<br/>实际视频生产 | 统筹实际生成、选片、剪辑、对白音效、完整播放审查与修复 | — | 常规 | [运行正文](skills/produce-ai-video/SKILL.md) · [中文说明](docs/skills/zh-CN/produce-ai-video.md) |
| `ai-short-drama-production`<br/>短剧控制 | 保留2026-09-07按5.6.0建立的独立合同：五列分镜＋六模块提示词；文本验证通过，实片待验 | — | 常规；实片待验 | [运行正文](skills/ai-short-drama-production/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-short-drama-production.md) |
| `web-design-director`<br/>网页辅助 | 明确网页或应用界面任务时设计与审核；仓库README维护不触发建站 | 1.3.0 | 常规 | [运行正文](skills/web-design-director/SKILL.md) · [中文说明](docs/skills/zh-CN/web-design-director.md) |
| `d-official-market-analysis`<br/>市场研究 | 根据当前可验证来源研究题材、平台、受众与制作机会，保留数据局限 | — | 常规 | [运行正文](skills/d-official-market-analysis/SKILL.md) · [中文说明](docs/skills/zh-CN/d-official-market-analysis.md) |
| `d-data-analysis-semantic-layer`<br/>知识审核与写入 | 用户批准后校验来源、版本、有效期与冲突，写入明确目标并回读 | — | 常规 | [运行正文](skills/d-data-analysis-semantic-layer/SKILL.md) · [中文说明](docs/skills/zh-CN/d-data-analysis-semantic-layer.md) |
| `hard-sci-fi-visual-director`<br/>硬科幻视觉 | 从物理、功能、制造与环境推导原创世界、设备、形体和完整提示词 | — | 实验 | [运行正文](experimental/hard-sci-fi-visual-director/SKILL.md) · [中文说明](docs/skills/zh-CN/hard-sci-fi-visual-director.md) |
| `whitebox-previs-executor`<br/>3D白模预演 | 将已有镜头编译成可播放机位与基础走位预演；打斗限已实现且过门的动作 | — | 实验 | [运行正文](experimental/whitebox-previs-executor/SKILL.md) · [中文说明](docs/skills/zh-CN/whitebox-previs-executor.md) |
| `guofeng-visual-director`<br/>古风视觉 | 文化依据、生活空间、人物器物、光色与图像提示词；附真实候选图 | 0.1.1 | 实验候选 | [运行正文](experimental/guofeng-visual-director/SKILL.md) · [中文说明](docs/skills/zh-CN/guofeng-visual-director.md) |

**分发状态与完成证据分开。** 常规包不表示所有能力已通过实战；实验硬科幻已有接受图例，白模仍有明确能力限制。短剧控制器已按当前阶段区分分镜与提示词，独立包不依赖其他技能；真实视频及用户效果验收未完成，实际宿主启用以对应安装记录为准，不新增独立版本号。其余实际使用和验收边界见各自运行正文与说明。

外部[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director)只作为仙侠工作流入口，不属于这21个源码包、不进本仓库ZIP；《云海钟境》是本项目自主生成并已接受的示例图，图的发布不等于再分发外部技能源码。

### 安装并使用当前源码中的一个Skill

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
git log -1 --oneline
python scripts/install_skill.py --list
python scripts/install_skill.py ai-storyboard-director --platform codex
```

安装器使用当前检出的源码。使用前核对分支、提交与`SKILL.md`版本，再按当前任务调用，例如：

```text
使用 $ai-storyboard-director，为下面30秒故事设计可读分镜。
保留已确认剧情、人物、台词与结尾，逐镜写清时间、画面、摄影、台词和声音。
本次先交分镜；如有创意拍法，单独说明作用和取舍，采用后再并入主方案。
[粘贴故事与已有约束]
```

需要提示词时，再明确请求把已确定的同一套分镜编译成完整视频提示词。实际生图、视频生成和预演分别发起，不从“看分镜”自动进入制作。

也可以先查看公共仓库可发现的技能，再复制所需入口：

```bash
npx --yes skills@latest add 62656456/ai-film-skills --list
npx --yes skills@latest add 62656456/ai-film-skills --skill ai-storyboard-director --agent codex --copy --yes
```

[完整安装与实验包选择](docs/INSTALLATION.md) · [宿主兼容边界](docs/COMPATIBILITY.md) · [42份中英设计指南](docs/skills/INDEX.md) · [历史CLI复制验证](examples/skills-cli-install-verification.md)

文件成功复制、宿主实际加载、真实任务输出和用户接受分别核验。[skills.sh目录](https://skills.sh/62656456/ai-film-skills)的统计包含维护者验证，不等于独立外部用户数。

### 历史动态证据

历史预演证据展示了可观看的机位、走位与短动作门，保留原验收范围：

<table>
<tr>
<td width="50%" valign="top"><a href="https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4"><img src="docs/media/previs-blocking-preview.gif" width="100%" alt="5秒基础3D摄影机和走位预演" /></a><br /><strong>基础机位与走位 · 5秒</strong></td>
<td width="50%" valign="top"><a href="https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4"><img src="docs/media/rigged-contact-preview.gif" width="100%" alt="2.8秒骨骼接触动作门" /></a><br /><strong>骨骼接触动作门 · 2.8秒</strong></td>
</tr>
</table>

白模执行器现作为源码中的独立实验包列出；这些历史片段证明有限预演与动作门，不证明任意完整打斗、最终AI成片或新的用户接受。[媒体清单](docs/media/media-manifest.json)

[旧5.4.4文字行为案例](examples/storyboard-director-5.4.4-visible-camera-plan.md)和[历史视觉参考墙](docs/style-gallery/manifest.json)仍可查看，保留各自日期与原状态，不与历史21张接受视觉成果混记。

### English overview

Open Film Skills provides **21 self-contained modules: 18 regular and 3 experimental**, with 42 English/Simplified Chinese guides. The workflow connects writing, directing, reusable assets, cinematography, prompts, optional previs, production, sound and full-playback review. Start with the [catalog](SKILL_CATALOG.md), [installation](docs/INSTALLATION.md) or [English guides](docs/skills/INDEX.md).

The [seven-genre study](docs/research/skill-overhaul/seven-genres/index.md) publishes 21 first-round storyboard boards with known repair items. It is separate from the 21 historically accepted artworks and interface screenshots. The [fusion study](docs/research/skill-overhaul/fusion/index.md) makes selected shots and remaining candidates visible. Text review, pixel review, continuous-video execution and user acceptance are recorded separately; version decisions appear in the final section below.

### 来源、许可与贡献

[共同审核逻辑](docs/SKILL_DESIGN_SYSTEM.md)

[原创版权与商用](COMMERCIAL_USE.md) · [Apache License 2.0](LICENSE) · [第三方说明](THIRD_PARTY_NOTICES.md) · [公开范围](PUBLICATION_SCOPE.md) · [贡献说明](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions) · [Issues](https://github.com/62656456/ai-film-skills/issues)

原创Skill、脚本、文档、提示词和明确授权的原创示例沿用仓库许可与各自来源说明。外部仙侠仅链接上游，不复制未核实再分发许可的源码；第三方参考、私人项目、凭证和本机状态不进入公开资料。

<a id="updates"></a>

## 3. 版本更新内容

### 2026-09-29：明确启用A，公开测试与待修问题

**本轮依据用户直接、明确的启用授权，将A5.7.1设为默认方案；B5.7.1-jev保留为可选文字复核方案。** 启用是使用决定，不代表21张首轮测试图已通过审美验收，也不把已发现的待修项改成完成。

- **创意思路独立交付**：说明拍法、叙事作用、前后衔接与取舍，采用后再并入主方案；不默认生图或生成视频。
- **阶段与交接更明确**：可读分镜、视频提示词和实际媒体按当前请求分别执行，已有导演决定和局部修改范围继续保留。
- **摄影与时间服务具体故事**：不预定镜数，不用固定时间切片约束题材；保留空间、人物支撑、环境持续、摄影起点与落点。
- **公开完整研究材料**：三版工作流、同题原稿与融合、七题材21张首轮图、生成说明和逐图问题一起可查。
- **已知待修继续可见**：新21图共29条明确或限定范围的观察，涉及15张；图像错误与文字设计分别追查，修复前保留首轮结果。

内部记录包括21包结构核对、6项仓库质量门和168项回归（164通过、4跳过），并有独立前向文本试用。它们的原始执行范围和日期保留在[整改研究](docs/research/skill-overhaul/index.md)中，不等同于21包跨任务稳定、视频执行成功或整套用户接受。

[两种检查方式与边界](docs/SEMANTIC_REVIEW.md) · [检查、部署和回退方法](docs/RELEASE_WORKFLOW.md) · [七题材逐图问题与待修](docs/research/skill-overhaul/seven-genres/index.md)

### 当前源码与下载版本

| 入口 | 当前用途与边界 |
|---|---|
| [当前分镜源码](skills/ai-storyboard-director/SKILL.md) | **A5.7.1默认方案**；本轮明确授权启用，按阶段交付；已知待修和审美状态另列 |
| B5.7.1-jev | 共用A创作核心，可选Jev文字核对；不会自动看图、采用创意或决定审美，详见[方案说明](docs/research/skill-overhaul/index.md) |
| 测试图中的“现用5.6.5” | 指本次对照实验开始时的默认版本，是历史测试标签；保留原图与原稿，不改贴为A结果 |
| [已发布v1.3.0](https://github.com/62656456/ai-film-skills/releases/tag/v1.3.0) | **历史Release快照**，分镜为5.4.4；源码更新不会重写旧ZIP |
| 5.6独立Preview | 独立预览包，保留自身标签、清单和范围；从[安装版本说明](docs/INSTALLATION.md)查看，与当前源码和v1.3.0分别记录 |

本次更新源码、研究成果和展示入口，不以推送源码冒充创建新Release。此前21张已接受作品、9月视觉研究、白模实验与旧版本案例继续按各自原始状态保留。后续修图与重测会标明具体对象和范围，保留可回看的首轮证据。
