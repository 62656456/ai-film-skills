<div align="center">

<img src="../../assets/hero.svg" width="100%" alt="Open Film Skills — AI映像制作のためのストーリー、デザイン、ショット、制作知能" />

# Open Film Skills

**Codex、Claude Code、TRAE、CodeBuddy、WorkBuddy、その他のAgentで再利用できるモジュール型の演出知能。**

[English](../../../README.md) · [简体中文](../zh-CN/README.md) · **日本語** · [한국어](../ko/README.md)

</div>

## 目的から選ぶ

| 目的 | Skill |
|---|---|
| 脚本の作成・修正、人物因果、自然な台詞 | [`director-agent`](../../../skills/director-agent/) |
| 承認済み脚本からショットと生成プロンプトを設計 | [`ai-storyboard-director`](../../../skills/ai-storyboard-director/) |
| キャラクター・シーン・小道具の参照資産を定義 | [`character-asset`](../../../skills/character-asset/) · [`scene-asset`](../../../skills/scene-asset/) · [`prop-asset`](../../../skills/prop-asset/) |
| 承認済み素材をAI映像として制作 | [`produce-ai-video`](../../../skills/produce-ai-video/) |
| Web UIを設計・実装・監査 | [`web-design-director`](../../../skills/web-design-director/) |

本リポジトリは、物語の因果、人物の目的、ブロッキング、空間連続性、物理的な動作、光、素材、制作ゲートを再利用可能な実行契約へ変換します。単なる流行語のプロンプト集ではありません。

## インストール

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

同じ自己完結型フォルダーを Codex、Claude Code、TRAE、CodeBuddy に配置でき、WorkBuddy ではZIPをアップロードできます。その他のAgentでは `SKILL.md` とローカルリソースを指示として読み込めます。詳細は [Compatibility](../../COMPATIBILITY.md) と [Installation](../../INSTALLATION.md) を参照してください。`experimental/` は既定の完全版に含まれません。

表示設計は [OmniRoute](https://github.com/diegosouzapw/OmniRoute) の明確なナビゲーション、多言語入口、図解、クイックスタート、状態表示を参考にしていますが、ブランド、画像、文章、コードは複製していません。

連絡先: [haldissita@gmail.com](mailto:haldissita@gmail.com)

## ライセンス

特記がない限り、個人制作部分は [Apache License 2.0](../../../LICENSE) です。
