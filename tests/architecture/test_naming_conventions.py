from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNAKE_CASE = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")
CANONICAL_STAGE_DIRECTORIES = frozenset(
    {
        "stage1_garak_baseline",
        "stage2_openai_mock_api",
        "stage3_real_model_scan",
        "stage4_guard_ab",
        "stage4_1_guard_ablation",
        "stage5_runtime_attack_matrix",
        "stage5_paper_baseline",
        "stage6_rag_security",
        "stage6_1_hidden_knowledge_poisoning",
        "stage6_2_trustworthy_retrieval",
        "stage7_agent_security",
    }
)


class NamingConventionTests(unittest.TestCase):
    def test_distribution_and_canonical_namespace_are_frozen(self) -> None:
        with (ROOT / "pyproject.toml").open("rb") as handle:
            project = tomllib.load(handle)["project"]

        self.assertEqual("llmguard-research-framework", project["name"])
        self.assertIn("LLM, RAG, and agent security evaluation", project["description"])
        self.assertTrue((ROOT / "src" / "llmguard" / "__init__.py").is_file())

    def test_stage_navigation_uses_only_canonical_slugs(self) -> None:
        stage_directories = {
            path.name for path in (ROOT / "stages").iterdir() if path.is_dir()
        }
        self.assertEqual(CANONICAL_STAGE_DIRECTORIES, stage_directories)

    def test_each_stage_readme_declares_required_metadata(self) -> None:
        required_fields = (
            "stage_id",
            "canonical_name",
            "canonical_slug",
            "legacy_paths",
            "status",
            "objective",
            "source_locations",
            "data_locations",
            "test_locations",
            "script_locations",
            "deliverable_locations",
            "evidence_locations",
            "conclusion_boundary",
            "next_stage",
        )
        for stage_slug in CANONICAL_STAGE_DIRECTORIES:
            readme_path = ROOT / "stages" / stage_slug / "README.md"
            readme = readme_path.read_text(encoding="utf-8")
            with self.subTest(stage_slug=stage_slug):
                self.assertIn("## Metadata", readme)
                for field in required_fields:
                    self.assertIn(field, readme)

    def test_new_llmguard_paths_use_snake_case(self) -> None:
        canonical_root = ROOT / "src" / "llmguard"
        for path in canonical_root.rglob("*"):
            if path.name == "__pycache__":
                continue
            stem = path.stem if path.is_file() else path.name
            if path.is_file() and path.suffix != ".py":
                continue
            if stem == "__init__":
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertRegex(stem, SNAKE_CASE)

    def test_legacy_allowlist_is_path_specific(self) -> None:
        allowlist = (ROOT / "config" / "naming_legacy_allowlist.yaml").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("*", allowlist)
        paths = [
            line.strip()[2:]
            for line in allowlist.splitlines()
            if line.startswith("  - ")
        ]
        self.assertTrue(paths)
        for relative_path in paths:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).exists())


if __name__ == "__main__":
    unittest.main()
