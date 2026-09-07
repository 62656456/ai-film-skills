# 全部技能目录 / Skill catalog

**本仓库20个源码包：18项常规＋2项实验；40份英文/简体中文指南。** 此页列出每包实际用途、源码版本和直接文件入口，GitHub仓库首页是[README](README.md)。

[完整工作流](docs/WORKFLOW.md) · [全部双语指南](docs/skills/INDEX.md) · [安装](docs/INSTALLATION.md) · [原创版权与商用](COMMERCIAL_USE.md)

版本列“—”表示`SKILL.md`未声明独立技能版本，按实际Git提交和完整文件识别；不据模板或协议字段编造版本。当前分镜源码明确为5.6.0。常规/实验是分发状态，不是全部能力通过实战的声明。

## 当前源码与历史下载

当前源码、已发布归档和独立Preview分别记录。[公开v1.3.0](https://github.com/62656456/ai-film-skills/releases/tag/v1.3.0)是含分镜5.4.4及旧清单的历史快照；5.6独立Preview是另行标记的分发物。这里不提供尚未发布的新Release下载地址。

```bash
python scripts/install_skill.py <skill-name> --platform codex
```

安装器读取实际检出版本；实验包另需`--experimental`。完整套装只含18项常规包，实验包单独选择。工具、模型、额度与账号权限不由Skill本身提供。

## Story and directing

编剧、导演与分镜。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `director-agent`<br/>编剧与导演 | 写作、改稿、对白与人物因果诊断；导演方案和条件式AI执行剧本 | — | 常规 | [运行正文](skills/director-agent/SKILL.md) · [中文说明](docs/skills/zh-CN/director-agent.md) · [EN](docs/skills/en/director-agent.md) |
| `ai-storyboard-director`<br/>分镜与摄影 | 将可用剧本设计为五列分镜和六模块母提示词；在作品目录保存恢复镜头决定 | 5.6.0 | 常规 | [运行正文](skills/ai-storyboard-director/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-storyboard-director.md) · [EN](docs/skills/en/ai-storyboard-director.md) |

## Asset definition

人物、场景与道具。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `character-asset`<br/>人物资产 | 人物身份、外形、必要视图、表情与可变状态的参考任务和资产合同 | — | 常规 | [运行正文](skills/character-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/character-asset.md) · [EN](docs/skills/en/character-asset.md) |
| `scene-asset`<br/>场景资产 | 场景拓扑、空间锚点、光源、材质和连续性参考图/提示词 | — | 常规 | [运行正文](skills/scene-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/scene-asset.md) · [EN](docs/skills/en/scene-asset.md) |
| `prop-asset`<br/>道具资产 | 道具结构、比例、可见面、持用和新旧状态；按要求交单图或必要视图 | — | 常规 | [运行正文](skills/prop-asset/SKILL.md) · [中文说明](docs/skills/zh-CN/prop-asset.md) · [EN](docs/skills/en/prop-asset.md) |

## Genre visual language

八项常规类型视觉。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `cyberpunk-design`<br/>赛博朋克 | 身体与技术关系、功能光源、空间层级和材质；不强制雨夜霓虹 | — | 常规 | [运行正文](skills/cyberpunk-design/SKILL.md) · [中文说明](docs/skills/zh-CN/cyberpunk-design.md) · [EN](docs/skills/en/cyberpunk-design.md) |
| `epic-design`<br/>史诗 | 地形、建筑、群体与个人代价共同建立尺度和画面秩序 | — | 常规 | [运行正文](skills/epic-design/SKILL.md) · [中文说明](docs/skills/zh-CN/epic-design.md) · [EN](docs/skills/en/epic-design.md) |
| `fantasy-design`<br/>奇幻 | 魔法来源、作用目标、世界规则和环境反馈的视觉参数 | — | 常规 | [运行正文](skills/fantasy-design/SKILL.md) · [中文说明](docs/skills/zh-CN/fantasy-design.md) · [EN](docs/skills/en/fantasy-design.md) |
| `horror-design`<br/>恐怖 | 可见异常证据、威胁显露、空间不安与可读暗部 | — | 常规 | [运行正文](skills/horror-design/SKILL.md) · [中文说明](docs/skills/zh-CN/horror-design.md) · [EN](docs/skills/en/horror-design.md) |
| `noir-design`<br/>黑色与犯罪 | 秘密、犯罪、关系压力和明暗信息；不以黑白滤镜替代剧情 | — | 常规 | [运行正文](skills/noir-design/SKILL.md) · [中文说明](docs/skills/zh-CN/noir-design.md) · [EN](docs/skills/en/noir-design.md) |
| `romance-design`<br/>爱情 | 距离、视线、接触和双向行动表达关系，不固定粉色、暖光或拥抱 | — | 常规 | [运行正文](skills/romance-design/SKILL.md) · [中文说明](docs/skills/zh-CN/romance-design.md) · [EN](docs/skills/en/romance-design.md) |
| `war-design`<br/>战争 | 地形、协同、负荷、行动与后果；检查武器方向和接触关系 | — | 常规 | [运行正文](skills/war-design/SKILL.md) · [中文说明](docs/skills/zh-CN/war-design.md) · [EN](docs/skills/en/war-design.md) |
| `wuxia-design`<br/>武侠 | 兵器、步法、支撑、衣发反馈与东方空间的可观察参数 | — | 常规 | [运行正文](skills/wuxia-design/SKILL.md) · [中文说明](docs/skills/zh-CN/wuxia-design.md) · [EN](docs/skills/en/wuxia-design.md) |

## Production, product, and research

生产、网页辅助与研究。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `produce-ai-video`<br/>实际视频生产 | 统筹实际生成、选片、剪辑、对白音效、完整播放审查与修复 | — | 常规 | [运行正文](skills/produce-ai-video/SKILL.md) · [中文说明](docs/skills/zh-CN/produce-ai-video.md) · [EN](docs/skills/en/produce-ai-video.md) |
| `ai-short-drama-production`<br/>短剧控制 | 五列分镜＋一条六模块母提示词；5.6结构已对齐，文本验证通过，实片待验 | — | 常规；未部署 | [运行正文](skills/ai-short-drama-production/SKILL.md) · [中文说明](docs/skills/zh-CN/ai-short-drama-production.md) · [EN](docs/skills/en/ai-short-drama-production.md) |
| `web-design-director`<br/>网页辅助 | 明确网页或应用界面任务时设计与审核；仓库README维护不触发建站 | — | 常规 | [运行正文](skills/web-design-director/SKILL.md) · [中文说明](docs/skills/zh-CN/web-design-director.md) · [EN](docs/skills/en/web-design-director.md) |
| `d-official-market-analysis`<br/>市场研究 | 根据当前可验证来源研究题材、平台、受众与制作机会，保留数据局限 | — | 常规 | [运行正文](skills/d-official-market-analysis/SKILL.md) · [中文说明](docs/skills/zh-CN/d-official-market-analysis.md) · [EN](docs/skills/en/d-official-market-analysis.md) |
| `d-data-analysis-semantic-layer`<br/>知识审核与写入 | 用户批准后校验来源、版本、有效期与冲突，写入明确目标并回读 | — | 常规 | [运行正文](skills/d-data-analysis-semantic-layer/SKILL.md) · [中文说明](docs/skills/zh-CN/d-data-analysis-semantic-layer.md) · [EN](docs/skills/en/d-data-analysis-semantic-layer.md) |

## Experimental

两项隔离实验。

| 技能 / 职责 | 逐项用途 | 当前源码版本 | 分发 | 入口 |
|---|---|---|---|---|
| `hard-sci-fi-visual-director`<br/>硬科幻视觉 | 从物理、功能、制造与环境推导原创世界、设备、形体和完整提示词 | — | 实验 | [运行正文](experimental/hard-sci-fi-visual-director/SKILL.md) · [中文说明](docs/skills/zh-CN/hard-sci-fi-visual-director.md) · [EN](docs/skills/en/hard-sci-fi-visual-director.md) |
| `whitebox-previs-executor`<br/>3D白模预演 | 将已有镜头编译成可播放机位与基础走位预演；打斗限已实现且过门的动作 | — | 实验 | [运行正文](experimental/whitebox-previs-executor/SKILL.md) · [中文说明](docs/skills/zh-CN/whitebox-previs-executor.md) · [EN](docs/skills/en/whitebox-previs-executor.md) |

短剧控制器已在仓库源码对齐5.6交付结构，独立文本行为样本经修正后最终通过；未部署、未生成视频、未获用户实际效果验收，未新增独立版本号。白模只对已实现代理和已过动作门负责，不能把基础预演升级为任意完整打斗。

## 历史v1.3.0单包附件

以下19个附件保留旧发布快照。它们不随当前源码变化；尤其分镜旧ZIP是5.4.4，新白模不在该旧Release中。当前白模从[源码安装入口](docs/INSTALLATION.md#experimental-packages)安装。

| 旧包 | 历史附件 |
|---|---|
| `director-agent` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/director-agent.zip) |
| `ai-storyboard-director` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-storyboard-director.zip) |
| `character-asset` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/character-asset.zip) |
| `scene-asset` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/scene-asset.zip) |
| `prop-asset` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/prop-asset.zip) |
| `cyberpunk-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/cyberpunk-design.zip) |
| `epic-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/epic-design.zip) |
| `fantasy-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/fantasy-design.zip) |
| `horror-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/horror-design.zip) |
| `noir-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/noir-design.zip) |
| `romance-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/romance-design.zip) |
| `war-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/war-design.zip) |
| `wuxia-design` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/wuxia-design.zip) |
| `produce-ai-video` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/produce-ai-video.zip) |
| `ai-short-drama-production` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-short-drama-production.zip) |
| `web-design-director` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/web-design-director.zip) |
| `d-official-market-analysis` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/d-official-market-analysis.zip) |
| `d-data-analysis-semantic-layer` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/d-data-analysis-semantic-layer.zip) |
| `hard-sci-fi-visual-director` | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/hard-sci-fi-visual-director.zip) |

## 外部仙侠与计数边界

[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director)只提供上游链接，不再分发其源码或ZIP；上游尚无已核实再分发许可。十种视觉路线为八项常规类型、实验硬科幻和外部仙侠。

本仓库20包＝19项影视＋1项网页辅助；另计外部仙侠后，完整工作流是20项影视职责＋1项网页辅助。外部项不计入20包或40份指南。

## 实际证据与返修

[14张展示图](docs/showcase/manifest.json)均为用户已接受的项目自主生成结果；这不是旧新版同题A/B，也不证明全题材稳定、视频执行或全部技能实战通过。旧[视觉图库](docs/style-gallery/manifest.json)、[5.4.4文字案例](examples/storyboard-director-5.4.4-visible-camera-plan.md)和[预演片段](docs/media/media-manifest.json)保留原证据状态。

结果失败时退回最早的故事、资产、摄影、光影、材质或执行环节，保留已确认事实。结构检查、实际加载、真实任务、媒体检查和用户接受分别记录。

## 排除与许可

已淘汰的`sci-fi-design`不恢复；外部系统/连接器/插件、私人项目、凭据和未经授权媒体不进入本仓库。详情见[公开范围](PUBLICATION_SCOPE.md)、[第三方说明](THIRD_PARTY_NOTICES.md)及[原创版权与商用](COMMERCIAL_USE.md)。
