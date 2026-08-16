<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="Open Film Skills — AI映像制作のためのストーリー、デザイン、ショット、制作知能" />

# Open Film Skills

**Codex、Claude Code、TRAE、CodeBuddy、WorkBuddy、その他のAgentで再利用できるモジュール型の演出知能。**

[English](../../../README.md) · [简体中文](../zh-CN/README.md) · **日本語** · [한국어](../ko/README.md)

</div>

## GitHubで読む

19個のモジュールには、目的、設計原則、入力、ワークフロー、差し戻し、レビューゲート、合格条件、出力、境界、Agent要件を説明する個別ページがあります。現在、全38ページの詳細版は **English と简体中文のみ** です。この日本語ページはリポジトリ概要であり、19個の詳細ページが日本語化済みだとは主張しません。

- [English / 简体中文 の全モジュール索引](../../skills/INDEX.md)
- [共通の差し戻し・レビュー・合格ロジック](../../SKILL_DESIGN_SYSTEM.md)
- [19モジュール、実行用 `SKILL.md`、ZIP の比較](../../../SKILL_CATALOG.md)

## 目的から選ぶ

| 目的 | 設計ガイド | 実行用ファイル | ZIP |
|---|---|---|---|
| 脚本の作成・修正、人物因果、自然な台詞 | [`director-agent` (English)](../../skills/en/director-agent.md) | [`SKILL.md`](../../../skills/director-agent/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) |
| 承認済み脚本からショットと生成プロンプトを設計 | [`ai-storyboard-director` (English)](../../skills/en/ai-storyboard-director.md) | [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) |
| キャラクター・シーン・小道具の参照資産を定義 | [Asset guides (English)](../../../SKILL_CATALOG.md#asset-definition) | [Runtime index](../../skills/INDEX.md) | [Latest release](https://github.com/62656456/ai-film-skills/releases/latest) |
| 承認済み素材をAI映像として制作 | [`produce-ai-video` (English)](../../skills/en/produce-ai-video.md) | [`SKILL.md`](../../../skills/produce-ai-video/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) |
| Web UIを設計・実装・監査 | [`web-design-director` (English)](../../skills/en/web-design-director.md) | [`SKILL.md`](../../../skills/web-design-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) |

本リポジトリは、物語の因果、人物の目的、ブロッキング、空間連続性、物理的な動作、光、素材、制作ゲートを再利用可能な実行契約へ変換します。単なる流行語のプロンプト集ではありません。

各モジュールは、自らが明示した成果の範囲内で単独利用できます。ただし、スタイルモジュールが脚本まで書く、画像ツールなしで資産画像が生成済みになる、制作モジュールが費用・権利・公開権限を回避できる、という意味ではありません。

## インストール

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

同じ自己完結型フォルダーを Codex、Claude Code、TRAE、CodeBuddy に配置でき、WorkBuddy ではZIPをアップロードできます。その他のAgentでは `SKILL.md` とローカルリソースを指示として読み込めます。指示を読めることと、ホストがSkillをネイティブに検出・実行できることは同じではありません。詳細は [Compatibility](../../COMPATIBILITY.md) と [Installation](../../INSTALLATION.md) を参照してください。`experimental/` は既定の完全版に含まれません。

表示設計は [OmniRoute](https://github.com/diegosouzapw/OmniRoute) の明確なナビゲーション、多言語入口、図解、クイックスタート、状態表示を参考にしていますが、ブランド、画像、文章、コードは複製していません。

連絡先: [haldissita@gmail.com](mailto:haldissita@gmail.com)

## ライセンス

特記がない限り、個人制作部分は [Apache License 2.0](../../../LICENSE) です。
