"""Evaluator/control-plane D1 inputs: exact paths and hashes; no discovery API."""
from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType


@dataclass(frozen=True)
class Binding:
    relative_path: str
    sha256: str


_PREP = ".worktrees/paper1-rag-defense-reconstruction-01/experiments/rag_defense_reconstruction_01/"
_BUNDLE = ".worktrees/stage6-rag/experiments/vace_l0_handoff_20261029_run01/private_input_v2/"
D1_BINDINGS: Mapping[str, Binding] = MappingProxyType({
    "queries_v2": Binding(_PREP + "ai_adjudication_01/prepared_drafts_v2/QUERY_DRAFTS_WITHOUT_ANSWERS.json",
        "d7b4656a6985e7375df71281713b1f6b73f745c9ac37296878eb0bac6002e500"),
    "answer_proposals_v2": Binding(_PREP + "ai_adjudication_01/prepared_drafts_v2/EVALUATOR_ANSWER_PROPOSALS_PRIVATE.json",
        "b5c7a2af6d3f30d5da68bfb553293ff9b1fe76ac7d93defba61da3cdacfeb14e"),
    "question_versions": Binding(_PREP + "ai_adjudication_01/prepared_drafts_v2/QUESTION_VERSION_CHANGELOG_EVALUATOR_ONLY.json",
        "f3254411b8f7be6b273d7cf4f634b019aeca0e5e0606e514dab825be614a8831"),
    "sources": Binding(_PREP + "ai_adjudication_01/input/SOURCES.json",
        "ad38ee7ca018f89e801f70a6e985b1f4194b940badeef92accd9305f7462d458"),
    "query_mapping": Binding(_PREP + "adjudication_review_01/CONTROL_MAPPING_EVALUATOR_ONLY.json",
        "70a7d03559c5e2a20f6e8c7777ec32fc7d789559430d866a9ff4a8745283b9dc"),
    "selection": Binding(_PREP + "pilot_freeze/SELECTION_EVALUATOR_ONLY.json",
        "2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689"),
    "bundle_manifest": Binding(_BUNDLE + "BUNDLE_MANIFEST.json",
        "a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60"),
    "f5": Binding(_BUNDLE + "runtime/f5.jsonl",
        "c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c"),
})


class D1Reader:
    """No glob/listdir/rglob. Unlisted requests fail BEFORE filesystem lookup.

    This controls this code's file access, not the agent or operating system.
    The immutable source-reviewed bindings are the authority; input content
    cannot add another path. Evaluation-only files stay out of model packets.
    """
    def __init__(self, workspace: Path, bindings: Mapping[str, Binding] = D1_BINDINGS):
        self.workspace = workspace.resolve()
        self.bindings = MappingProxyType(dict(bindings))
        self.events: list[dict[str, str]] = []

    def read(self, key: str) -> bytes:
        if key not in self.bindings:
            self.events.append({"request": "UNLISTED_KEY", "status": "DENIED_BEFORE_IO"})
            raise PermissionError("D1_PATH_NOT_ALLOWLISTED")
        return self.read_relative(self.bindings[key].relative_path)

    def read_relative(self, relative: str) -> bytes:
        matches = [(k, b) for k, b in self.bindings.items() if b.relative_path == relative]
        pure = PurePosixPath(relative)
        if (not matches or pure.is_absolute() or ".." in pure.parts or ":" in relative
                or "\\" in relative or str(pure) != relative):
            self.events.append({"request": "UNLISTED_PATH", "status": "DENIED_BEFORE_IO"})
            raise PermissionError("D1_PATH_NOT_ALLOWLISTED")
        key, binding = matches[0]
        path = self.workspace.joinpath(*pure.parts)
        # Only ancestors of an already allowlisted file are inspected.
        current = path
        while current != self.workspace:
            if current.is_symlink() or current.is_junction():
                raise PermissionError("D1_LINK_NOT_ALLOWED")
            current = current.parent
        if not path.resolve().is_relative_to(self.workspace):
            raise PermissionError("D1_PATH_ESCAPES_WORKSPACE")
        value = path.read_bytes()
        if hashlib.sha256(value).hexdigest() != binding.sha256:
            self.events.append({"request": key, "status": "HASH_MISMATCH"})
            raise ValueError("D1_PIN_MISMATCH")
        self.events.append({"request": key, "status": "PINNED_READ"})
        return value
