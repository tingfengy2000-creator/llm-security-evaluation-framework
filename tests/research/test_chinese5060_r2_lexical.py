"""Regression tests for the R2 lexical-only intervention."""
import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.r2_lexical import lexical_view

TOOLBAR = "首页 首页 > 正文阅读 下载Word 下载PDF 扫码下载"


def test_mask_has_reversible_offsets_and_preserves_facts() -> None:
    before = "规范原文 " + TOOLBAR + " 历史沿革 2024-01-01 第十二条 20% 不得修改适用版本"
    status, masked, spans, unsafe = lexical_view(before)
    begin, end = spans[0]
    assert status == "WEB_CHROME_CONFIDENT" and unsafe == 0
    assert before[begin:end] == TOOLBAR and len(masked) == len(before)
    assert masked[:begin].encode() == before[:begin].encode()
    assert masked[end:].encode() == before[end:].encode()
    assert masked[begin:end] == " " * (end - begin)


@pytest.mark.parametrize("text", [
    "第九条不得下载 PDF 版本的历史沿革附件",
    "首页修订时间为2024年3月15日",
    "技术规范规定应下载PDF，版本不得低于2.5",
    "下载Word 下载PDF 扫码下载",
    "历史沿革 收起 1994-02-03 1995-03-25",
])
def test_ambiguous_text_is_preserved(text: str) -> None:
    assert lexical_view(text) == ("AMBIGUOUS", text, [], 0)


def test_no_mask_on_empty_lexical_result() -> None:
    assert lexical_view(TOOLBAR) == ("AMBIGUOUS", TOOLBAR, [], 1)


def test_plain_text_preserved() -> None:
    text = "建立作业制度与管理责任体系"
    assert lexical_view(text) == ("NONE", text, [], 0)
