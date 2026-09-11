# AI Storyboard Director 5.6.0 Preview

**独立测试更新 · Explicit-only prerelease · 5.4.4 remains the daily baseline**

5.6.0-rc.1 用于测试镜头设计的保存、局部恢复和连续性检查。它与日常 `ai-storyboard-director` 分开，安装目录和Skill名称均为 `ai-storyboard-director-preview`。是否采用新版，须等待实际制作结果与使用者的明确决定。

## 这次改了什么

分镜经过多轮讨论、局部修改或对话中断后，助手可能丢掉先前的导演意图、镜头决定和人物道具状态。本候选把这些决定实际保存在选定作品目录中；续接时读取当前场景、必要前场与全片意图，减少对长对话摘要的依赖。

- 保存导演意图、选中镜头及简短依据、用户锁定事实、场景进入与退出状态。
- 按本场设计问题读取包内构图、机位、调度、光学、运动与轴线知识。
- 检查源剧本变化、旧版本覆盖、已存场景遗漏、明确的状态断裂、时间缺口与固定二维轴上的机位错误。
- 复杂几何仍可保留为明确未验证的候选，避免为了过检查强迫简化拍法。

这不是完美记忆或更高摄影水平的保证。程序不判断构图是否动人，也不证明自然语言已完整落实导演意图。最终交付仍是分镜表和视频提示词，内部工作记录不应混入创作正文。

## 单独安装与调用

1. 下载本次预发布的 `ai-storyboard-director-preview-5.6.0-rc.1.zip`，解压后取得 `ai-storyboard-director-preview` 文件夹。
2. 在现有助手中将这个文件夹单独安装到Skill目录，与 `ai-storyboard-director` 并列；**不要改名为主版，也不要覆盖主版目录**。支持调用策略的宿主会读取 `allow_implicit_invocation: false`；其他环境也应只在明确测试时手动启用。
3. 使用作品副本测试，并明确调用：

```text
使用 $ai-storyboard-director-preview，为这份剧本设计镜头。
测试作品目录为我指定的副本目录。先完整理解剧本，按场景保存导演决定。
保留已锁定的剧情与摄影要求；不要修改我的日常Skill。
```

跨对话续接时，显式调用同一测试包并指向同一作品副本，要求从实际保存的工作记录恢复。新的创作阶段可以改变本轮工作范围；“上一轮只做第一段”不能被当成长久故事锁。

需要支持Skill、本地文件读写和Python的助手环境；建议Python 3.12或更高。本包运行程序只使用标准库，不联网、不调用模型、不要求另买API。视频制作沿用你现有的流程和账户。

## 希望你测试的真实问题

选一段你确实准备制作的剧本：完成分镜和提示词，经过多轮局部修改，再换新对话续接下一段。检查早先镜头有没有被意外改写、最新要求有没有正确采用、关键动作与人物关系是否清楚，以及记录步骤是否让创作变得繁琐或机械。

随后用日常制作流程生成或剪辑一段可观看视频。把文本方案与实际画面逐镜比较；如果方便，也与5.4.4在同一输入上的结果对照。不要仅以表格齐全或程序通过判断值得采用。

请到仓库Issues提交反馈，标题注明 `5.6 Preview`，包括以下五项；只分享你愿意公开且有权分享的材料：

1. 助手环境、所用版本、剧本或片段长度。
2. 是否已实际制作视频；成功或失败的具体镜头/时间点。
3. 经历多少轮修改、是否换对话；恢复时保留和遗漏了什么。
4. 一次明确修改的“要求改什么 / 实际改了什么 / 无关内容是否保留”。
5. 与主版比较后愿意采用哪份方案，最值得修复的一个问题。

## 已验证与未验证

- 原5.6.0实现：9个运行文件、19处引用闭合；空目录24项程序测试通过。
- 一个新造文本用例完成两个独立上下文的18秒与8秒镜头设计续接，第一段场景数据保持不变。执行者知道使用该Skill，不属于无提示自动路由盲测。
- 本Preview仅调整隔离名称、明确调用策略和发布说明，运行程序与原5.6.0保持一致；发布前另行复跑包闭包与24项程序测试。
- 长篇、多轮使用的稳定性、摄影审美提升、真实视频效果及用户实际制作接受仍待验证。不会因上传、CI通过或下载量自动晋升为主版。

---

## English

**5.6.0-rc.1 is a separate test update. The daily baseline remains 5.4.4.** Install the folder named `ai-storyboard-director-preview` alongside the main `ai-storyboard-director` folder, and explicitly invoke `$ai-storyboard-director-preview`. Do not rename it to the main Skill or overwrite the daily installation. Implicit invocation is disabled on hosts that support this policy.

The preview stores directing intent, selected shots with brief rationales, locked facts, and scene entry/exit states in a chosen project folder. Scene-focused recovery reads the relevant saved material, while deterministic checks catch source drift, stale writes, missing scenes, explicitly recorded continuity errors, timing gaps, and fixed 2D axis violations. Framing and axis guidance supports the directing process without assigning a fixed camera technique to an emotion.

Use a project copy in an existing assistant environment with local file access and Python, preferably 3.12 or newer. The runtime uses only the standard library and makes no network or model calls. It does not require a separate API purchase.

Please test real production and continuation: design a scene, make focused revisions, reopen the same project copy in a fresh conversation, and produce a watchable clip using your normal workflow. Report what survived, what was lost, whether unrelated shots changed, and whether the result is worth keeping compared with the daily version.

The underlying runtime passed 24 isolated program tests and one original two-segment continuation scenario. The preview package is revalidated before release. These results do not establish better cinematography, long-project reliability, perfect memory, or successful video generation. Adoption depends on real production feedback and an explicit user decision.

For feedback, open an issue titled `5.6 Preview` and include: environment and scene length; actual production result with optional timestamps; conversation/revision history and recovery behavior; one requested versus actual revision; and your adoption decision with the first issue you would fix.
