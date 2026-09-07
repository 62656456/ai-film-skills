<div align="center">

# Open Film Skills

**アイデアと脚本から、演出、ビジュアル資産、ショット、プロンプト、映像制作、確認まで。**

[English](../../../README.md#english-overview) · [简体中文](../zh-CN/README.md) · **日本語** · [한국어](../ko/README.md)

</div>

![映像制作の全体ワークフロー](../../assets/workflow-overview.svg)

[全ノード・受け渡し・Mermaid原図](../../WORKFLOW.md) · [承認済み14画像](../../../README.md#本轮14张用户接受成图) · [モジュール一覧](../../../SKILL_CATALOG.md)

## 現在のソースと公開済みアーカイブ

現在のソースには **通常18＋実験2＝20モジュール** があり、詳細ガイドはEnglishと简体中文の計40ページです。この日本語ページは概要であり、20の詳細ガイドの日本語訳ではありません。

- 現在のStoryboard Directorソースは **5.6**。明示された作品ディレクトリ内で演出意図、選択ショット、場面状態を保存・復元します。
- 公開済み **v1.3.0** は **5.4.4** を含む過去のスナップショットです。ソース更新で既存ZIPは変わりません。
- 別途ラベル付けされた5.6単体Previewも独立した配布物です。この更新は新しい完全版Releaseの公開を意味しません。

[ソースとZIPの選び方](../../INSTALLATION.md) · [40ガイド](../../skills/INDEX.md)

## 必要な成果から選ぶ

| 成果 | モジュール |
|---|---|
| 脚本・台詞の修正、演出判断 | [director-agent](../../skills/en/director-agent.md) |
| カメラ、ショット、完全な生成プロンプト | [ai-storyboard-director](../../skills/en/ai-storyboard-director.md) |
| キャラクター・場所・小道具 | [資産モジュール](../../../SKILL_CATALOG.md#asset-definition) |
| ジャンルの光・色・構図・素材 | [8通常ジャンル](../../../SKILL_CATALOG.md#genre-visual-language)と[ハードSF実験](../../skills/en/hard-sci-fi-visual-director.md) |
| 基礎的な3Dカメラ・動線プレビュー | [whitebox-previs-executor](../../skills/en/whitebox-previs-executor.md)、実験配布 |
| 実際の生成・編集・音・全編確認 | [produce-ai-video](../../skills/en/produce-ai-video.md) |

既存の素材があれば該当段階から続けます。外部の[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director)は仙侠ワークフロー用のリンクのみで、再配布許可が確認できないためソースやZIPには含めません。リポジトリの19映像モジュール＋Web補助1に外部仙侠を加えると、全体図は映像20の役割＋Web補助1になります。

## ソースからインストール

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
git log -1 --oneline
python scripts/install_skill.py ai-storyboard-director --platform codex
```

実際にチェックアウトした版を確認してください。未公開のローカル変更は公開ブランチには含まれません。実験パッケージは明示的な`--experimental`が必要です。[Installation](../../INSTALLATION.md)と[Compatibility](../../COMPATIBILITY.md)を参照してください。

## 実例と限界

14枚のオリジナル生成画像はユーザーが明示的に承認しています。全画角のプレビューと原PNG、出所と状態を[公開マニフェスト](../../showcase/manifest.json)で確認できます。旧版との同一プロンプトA/B比較は実施しておらず、一般的な成功率や動画品質を保証しません。

構図、光、素材、色は場面ごとに選択し、夕景、浅い被写界深度、ネオンを必須にはしません。白箱プレビューは実装済みの主体と個別に合格した動作に限られ、任意の長い格闘を保証しません。5.6の状態チェックは美的判断の代わりにはなりません。

[設計・確認原則](../../SKILL_DESIGN_SYSTEM.md) · [公開範囲](../../../PUBLICATION_SCOPE.md) · [Apache License 2.0](../../../LICENSE) · [フィードバック](https://github.com/62656456/ai-film-skills/issues)
