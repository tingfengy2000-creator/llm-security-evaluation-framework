from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RETRIEVAL = ROOT / "src" / "llmguard" / "domains" / "retrieval"


def test_evidence_and_citation_dtos_have_one_contract_owner() -> None:
    owners: dict[str, list[Path]] = {"EvidenceEnvelope": [], "CitationBinding": [], "CitationMode": []}
    for path in RETRIEVAL.rglob("*.py"):
        module = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(module):
            if isinstance(node, (ast.ClassDef,)) and node.name in owners:
                owners[node.name].append(path.relative_to(RETRIEVAL))

    assert owners == {
        "EvidenceEnvelope": [Path("contracts/evidence_envelope.py")],
        "CitationBinding": [Path("contracts/evidence_envelope.py")],
        "CitationMode": [Path("contracts/evidence_envelope.py")],
    }
    assert not (RETRIEVAL / "context" / "models.py").exists()
    assert (RETRIEVAL / "context" / "builder.py").exists()
    assert not any(path.name == "package.py" for path in (RETRIEVAL / "context").glob("*.py"))


def test_context_layer_does_not_depend_on_legacy_or_model_backends() -> None:
    forbidden = ("codeguarder", "chromadb", "sentence_transformers", "GroundTruth", "Evaluator")
    for path in (RETRIEVAL / "context").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert not any(token in text for token in forbidden), path


def test_only_factory_constructs_envelopes_and_context_builder_creates_bindings() -> None:
    envelope_calls: list[Path] = []
    binding_calls: list[Path] = []
    for path in RETRIEVAL.rglob("*.py"):
        module = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(module):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id == "EvidenceEnvelope":
                envelope_calls.append(path.relative_to(RETRIEVAL))
            if node.func.id == "CitationBinding":
                binding_calls.append(path.relative_to(RETRIEVAL))

    assert envelope_calls == [Path("context/envelope.py")]
    assert binding_calls == [Path("context/builder.py")]
