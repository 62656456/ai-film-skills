# 21 个技能的源码盘点

2026-09-21｜本次核对覆盖全部 **21 个包、172 个运行文本文件**：18 个常规包与3个主动选择的实验包。逐文件比较维护源、公开包及可用运行副本的完整内容；区分换行差异、发布适配和实质方法差异。没有另行版本号的技能以仓库提交和文件内容识别，不为本次展示虚构版本。

本次明确同步分镜导演5.6.4的12个文件，新增古风0.1.1候选包，并对人物参考中的私有会话标识脱敏。其余已收录的方法和公开修复保留；在本次可访问并核对的维护来源中，未发现遗漏的更新文件。此结论不覆盖未提供的私有分支或不可访问资料，也不代表所有技能都在本轮新增。

| 技能 | 已记录版本 | 本次处理 | 来源一致性与公开适配 |
|---|---|---|---|
| [director-agent](../../skills/director-agent/SKILL.md) | 按提交识别 | 保留 | 仓库是维护源；15个运行文件完整。保留公开生产交接修订，不用较旧运行副本覆盖。 |
| [ai-storyboard-director](../../skills/ai-storyboard-director/SKILL.md) | 5.6.4 | 同步 | 12个运行文件与当前维护源及运行副本的完整内容一致；公开文本可规范末尾空行，不改变业务内容。融合六段母稿、打戏设计与运镜诊断同属一个入口。 |
| [character-asset](../../skills/character-asset/SKILL.md) | 按提交识别 | 保留并脱敏 | 5个运行文件；与维护源的唯一正文差异是移除女性魅力参考中的私有会话标识，保留方法与来源限制。 |
| [scene-asset](../../skills/scene-asset/SKILL.md) | 按提交识别 | 保留 | 4个运行文件与维护源及运行副本一致；保留剧本先行和环境使用逻辑。 |
| [prop-asset](../../skills/prop-asset/SKILL.md) | 按提交识别 | 保留 | 4个运行文件与维护源及运行副本一致。 |
| [cyberpunk-design](../../skills/cyberpunk-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [epic-design](../../skills/epic-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [fantasy-design](../../skills/fantasy-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [horror-design](../../skills/horror-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [noir-design](../../skills/noir-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [romance-design](../../skills/romance-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [war-design](../../skills/war-design/SKILL.md) | 1.0.0 | 保留 | 13个运行文件；方法正文一致，公开入口保留既有精简元数据格式。军事顾问已合并，不恢复第二运行入口。 |
| [wuxia-design](../../skills/wuxia-design/SKILL.md) | 按提交识别 | 保留 | 6个运行文件与维护源及运行副本一致。 |
| [produce-ai-video](../../skills/produce-ai-video/SKILL.md) | 按提交识别 | 保留 | 仓库是维护源；5个运行文件完整。保留公开提示词编译修订，不从较旧运行副本回退。 |
| [ai-short-drama-production](../../skills/ai-short-drama-production/SKILL.md) | 按提交识别 | 保留 | 6个公开运行文件，包括既有独立交接文件。2026-09-07按5.6.0建立的五列分镜＋六模块合同保留，未采用5.6.4融合单稿；未部署。 |
| [web-design-director](../../skills/web-design-director/SKILL.md) | 1.3.0 | 保留 | 仓库是维护源；8个文件的方法正文与运行副本一致，公开入口保留既有精简元数据格式。 |
| [d-official-market-analysis](../../skills/d-official-market-analysis/SKILL.md) | 按提交识别 | 保留 | 仓库是维护源；9个运行文件与运行副本一致。 |
| [d-data-analysis-semantic-layer](../../skills/d-data-analysis-semantic-layer/SKILL.md) | 按提交识别 | 保留 | 仓库是维护源；10个运行文件与运行副本一致。 |
| [hard-sci-fi-visual-director](../../experimental/hard-sci-fi-visual-director/SKILL.md) | 按提交识别 | 保留实验状态 | 20个运行文件与维护源一致；不因既有图例被接受而自动提升整个包的状态。 |
| [whitebox-previs-executor](../../experimental/whitebox-previs-executor/SKILL.md) | 按提交识别 | 保留公开修复 | 12个运行文件完整。保留环境变量依赖发现、去除作者电脑路径、规格预检与打斗后端分流等四文件公开适配。 |
| [guofeng-visual-director](../../experimental/guofeng-visual-director/SKILL.md) | 0.1.1 candidate | 新增实验包 | 7个文件与本次核对的候选运行副本逐字节一致；候选元数据保留。文化研究入口、摄影真实感诊断与图像检查已写入，实际样图仍按各自审阅结果标记。 |

## 盘点的证据边界

- 分镜5.6.4的源码同步不改写历史v1.3.0下载附件；当前源码、旧发行快照与独立Preview分别识别。
- 白模公开适配提高可移植性和错误处理，不新增通用动作、车辆或任意编舞后端。研究页的具体可播放实验与通用执行器能力分别说明。
- 古风包只包含自行撰写的方法与公开来源链接，不捆绑博物馆图像；候选公开不等于用户接受或历史准确性认证。
- 本次172个运行文本的隐私检查未发现作者电脑绝对路径、私有会话UUID或常见凭据模式。项目状态、私有审阅记录、缓存与第三方未获许可源码不属于运行包。
- 文件完整、源码一致、程序检查、实际图片或视频结果、用户接受是不同证据；本清单不把它们合并为“全部实战稳定”。

[返回研究成果](../RESEARCH.md) · [查看分发范围](../../PUBLICATION_SCOPE.md) · [查看全部技能说明](../skills/INDEX.md)
