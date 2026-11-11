"""Template checks for the Owner28 review pack. No sealed labels."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_validator():
    path = Path(__file__).resolve().parents[2] / "scripts/research/validate_owner28_human_review.py"
    spec = importlib.util.spec_from_file_location("validate_owner28_human_review", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_template_and_ten_fictional_cases() -> None:
    module = load_validator()
    module.validate_schema_document(module.load_json(module.SCHEMA_PATH))
    module.validate_fixtures(module.load_json(module.FIXTURE_PATH))


def test_forbidden_review_key_is_rejected() -> None:
    module = load_validator()
    try:
        module.assert_no_forbidden_keys({"item_id": "r-0", "role": "P"})
    except SystemExit as exc:
        assert str(exc) == "FORBIDDEN_KEY role"
    else:
        raise AssertionError("forbidden key was accepted")
