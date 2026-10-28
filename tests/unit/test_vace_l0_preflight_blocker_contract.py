"""Static blocked-attempt provenance tests; never model/CUDA correctness claims."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_HARDWARE_PREFLIGHT_BLOCKER_V1.md'


def test_twelve_field_owner_escalation_record() -> None:
    text = DOC.read_text('utf-8')
    for n in range(1, 13):
        assert f'## {n}.' in text
    for word in ('OBSERVED_FACT', 'SOURCE_DERIVED_FACT', 'INFERENCE', 'UNKNOWN'):
        assert word in text


def test_requested_device_and_visible_device_not_conflated() -> None:
    text = DOC.read_text('utf-8')
    assert 'RTX5090 32GB' in text and 'RTX5060' in text and '8151 MiB' in text
    assert 'CUDA软件故障诊断' in text and '是否可用尚未判定' in text


def test_no_fabricated_model_freeze_or_scores() -> None:
    text = DOC.read_text('utf-8')
    assert 'L0-F5：NOT_EXECUTED' in text and 'L0-Oracle：NOT_EXECUTED' in text
    assert '不能填0' in text and '模型revision/tokenizer/weights SHA' in text
    assert '下载=0字节' in text and '安装=0字节' in text


def test_stopped_gate_and_originals_preserved() -> None:
    text = DOC.read_text('utf-8')
    assert 'L0_STRONG_BASELINE_PREFLIGHT_BLOCKED / HUMAN_DECISION_REQUIRED' in text
    assert '40组120条13事实家族' in text and '8组24条HOLD' in text
    assert '不自行联系/控制另一台GPU机器' in text
    assert '数据和历史不改' in text
