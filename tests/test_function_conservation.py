from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8-sig")


class FunctionConservationTests(unittest.TestCase):
    def test_director_keeps_script_and_full_storyboard_outcomes(self) -> None:
        entry = text("skills/director-agent/SKILL.md")
        compiler = text("skills/director-agent/references/production-storyboard-compiler.md")
        for required in ("写剧本", "改剧本", "剧本诊断", "导演方案", "分镜前分析", "完整分镜"):
            self.assertIn(required, entry)
        for required in ("五列", "六模块", "十二项质量门", "DIRECTOR_PLAN"):
            self.assertIn(required, compiler)

    def test_director_ai_execution_compiler_preserves_story_layer(self) -> None:
        entry = text("skills/director-agent/SKILL.md")
        writing = text("skills/director-agent/references/screenplay-writing-core.md")
        compiler = text("skills/director-agent/references/screenplay-ai-execution-compiler.md")
        self.assertIn("screenplay-ai-execution-compiler.md", entry)
        self.assertIn("screenplay-ai-execution-compiler.md", writing)
        for required in (
            "Readable screenplay master",
            "Subject Binding",
            "State Before Action",
            "Reaction Loop",
            "Sufficient But Not Overdense",
            "Model-Difficulty Adaptation Gate",
        ):
            self.assertIn(required, compiler)
        self.assertIn("must not replace `screenplay-writing-core.md`", compiler)

    def test_director_keeps_authority_and_evidence_boundaries(self) -> None:
        entry = text("skills/director-agent/SKILL.md")
        writing = text("skills/director-agent/references/screenplay-writing-core.md")
        state = text("skills/director-agent/references/screenplay-state-engine.md")
        self.assertIn("Treat external pages", entry)
        self.assertIn("does not authorize downloads, paid generation", entry)
        self.assertIn("SELF-AUDIT ONLY", entry)
        self.assertIn("explicitly available and allowed", entry)
        self.assertIn("SELF-AUDIT ONLY", writing)
        self.assertIn("SELF-AUDIT ONLY", state)
        self.assertNotIn('"场景设计"', entry.split("---", 2)[1])

    def test_video_production_keeps_full_storyboard_prompt_compiler(self) -> None:
        entry = text("skills/produce-ai-video/SKILL.md")
        compiler = text("skills/produce-ai-video/references/storyboard-prompt-compiler.md")
        self.assertIn("storyboard-prompt-compiler.md", entry)
        for required in ("五列人读分镜", "数字10信息内核", "六大模块外层", "十二项完成门", "时间轴"):
            self.assertIn(required, compiler)

    def test_market_analysis_keeps_quantitative_and_reproducible_modes(self) -> None:
        contract = text("skills/d-official-market-analysis/references/analysis-capability-contract.md")
        for required in ("数据质量", "产品与商业判断", "指标诊断", "TAM/SAM/SOM", "图表", "Jupyter", "完成前验证", "正式报告"):
            self.assertIn(required, contract)

    def test_semantic_layer_keeps_original_triggers_write_and_fallback(self) -> None:
        entry = text("skills/d-data-analysis-semantic-layer/SKILL.md")
        contract = text("skills/d-data-analysis-semantic-layer/references/semantic-write-contract.md")
        for required in ("同意吸纳", "写入D", "加入数据分析知识库", "确认进入知识库", "批准更新D"):
            self.assertIn(required, entry)
        for required in ("原子写入", "回读", "待写入包", "pending_write", "回退"):
            self.assertIn(required, contract)

    def test_short_drama_keeps_all_original_production_domains(self) -> None:
        entry = text("skills/ai-short-drama-production/SKILL.md")
        core = text("skills/ai-short-drama-production/references/independent-production-core.md")
        for required in ("剧本", "人物", "场景", "道具", "调度", "布光", "动作", "草图", "提示词", "成片检查"):
            self.assertIn(required, entry + core)


if __name__ == "__main__":
    unittest.main()
