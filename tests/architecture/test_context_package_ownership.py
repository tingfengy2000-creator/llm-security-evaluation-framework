from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "src" / "llmguard" / "domains" / "retrieval" / "contracts"
CONTEXT = ROOT / "src" / "llmguard" / "domains" / "retrieval" / "context"


def test_context_package_dtos_have_one_canonical_contract_owner() -> None:
    owners: dict[str, list[Path]] = {
        "ContextBuildConfig": [],
        "ContextBuildTrace": [],
        "RetrievedContextPackage": [],
    }
    for path in (CONTRACTS, CONTEXT):
        for source in path.rglob("*.py"):
            module = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(module):
                if isinstance(node, ast.ClassDef) and node.name in owners:
                    owners[node.name].append(source)

    for name, paths in owners.items():
        assert paths == [CONTRACTS / "context_package.py"], name


def test_context_implementation_does_not_import_forbidden_runtime_dependencies() -> None:
    combined = "\n".join(
        source.read_text(encoding="utf-8")
        for source in CONTEXT.rglob("*.py")
    )
    for forbidden in (
        "chromadb",
        "EmbeddingProvider",
        "VectorStore",
        "TrustAggregator",
        "RetrievalPolicy",
        "GroundTruthVault",
        "openai",
        "groq",
    ):
        assert forbidden not in combined
