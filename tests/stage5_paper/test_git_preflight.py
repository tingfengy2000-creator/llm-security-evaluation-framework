import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


class GitPreflightTests(unittest.TestCase):
    def test_gitignore_excludes_environment_not_experiment_logs(self):
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".venv/", text)
        self.assertIn("__pycache__/", text)
        self.assertNotIn("deliverables/**/logs/**", text)

    def test_registry_covers_all_experiments(self):
        registry = json.loads(
            (ROOT / "experiments" / "registry.json").read_text(encoding="utf-8")
        )
        stages = {item["stage_id"] for item in registry["experiments"]}
        self.assertTrue(
            {
                "stage1",
                "stage2",
                "stage3",
                "stage4",
                "stage4.1",
                "stage5",
                "stage5-paper",
            }.issubset(stages)
        )

    def test_regression_script_is_offline(self):
        text = (
            ROOT / "scripts" / "run_stage5_paper_regression.ps1"
        ).read_text(encoding="utf-8")
        self.assertIn("-Provider mock", text)
        self.assertNotIn("-Provider groq", text)

    def test_smoke_and_single_attack_contracts(self):
        smoke = (ROOT / "scripts" / "run_stage5_paper_smoke.ps1").read_text(
            encoding="utf-8"
        )
        single = (
            ROOT / "scripts" / "run_stage5_paper_single_attack.ps1"
        ).read_text(encoding="utf-8")
        self.assertIn("[int]$Seed = 42", smoke)
        self.assertIn('"A1", "A2", "A3", "A4", "A5", "A6"', single)

    def test_chinese_interview_bundle_has_curated_copies(self):
        bundle = ROOT / "interview_prep"
        required = {
            "README.md",
            "01_知识地图.md",
            "02_项目完整实现过程.md",
            "03_面试话术.md",
            "04_高频追问.md",
            "05_实验结果与结论边界.md",
            "06_复现命令.md",
        }
        self.assertTrue(required <= {path.name for path in bundle.iterdir()})
        copies = bundle / "source_copies"
        self.assertGreaterEqual(len(list(copies.glob("*.md"))), 6)
        text = (bundle / "README.md").read_text(encoding="utf-8")
        self.assertIn("面试", text)
        self.assertIn("学习", text)

    def test_file_manifest_excludes_runtime_and_environment(self):
        manifest = json.loads(
            (ROOT / "provenance" / "file_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        paths = [item["path"] for item in manifest]
        forbidden = (".venv/", "__pycache__/", "xdg_data/", "xdg_config/", "tmp_create_test/")
        self.assertFalse(
            any(marker in path for path in paths for marker in forbidden)
        )
        self.assertNotIn("provenance/file_manifest.json", paths)


if __name__ == "__main__":
    unittest.main()
