"""Synthetic checks for the RD-zh source adapter, independent of local model assets."""
from hashlib import sha256

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import rd_zh_tfidf

SOURCE = b"""class Grouping:
    def lexical_vote(self, passages):
        stop_words = list(_text.ENGLISH_STOP_WORDS)
        tfidf = _text.TfidfVectorizer(stop_words=stop_words)
        return tfidf.fit_transform(passages)
"""
PATCHED = b"""class Grouping:
    def lexical_vote(self, passages):
        tfidf = _text.TfidfVectorizer(analyzer="char", ngram_range=(2, 2), stop_words=None)
        return tfidf.fit_transform(passages)
"""


@pytest.mark.parametrize("newline", [b"\n", b"\r\n"])
def test_only_the_vectorizer_site_changes(monkeypatch: pytest.MonkeyPatch, newline: bytes) -> None:
    monkeypatch.setattr(rd_zh_tfidf, "_PINNED_SOURCE_SHA256", sha256(SOURCE).hexdigest())
    source = SOURCE.replace(b"\n", newline)
    adapted = rd_zh_tfidf.adapt_clustering_source(source)

    assert adapted == PATCHED.replace(b"\n", newline)
    compile(adapted, "<synthetic rd-zh>", "exec")


def test_unpinned_source_is_rejected() -> None:
    with pytest.raises(ValueError, match="RD_ZH_UPSTREAM_CLUSTERING_SOURCE_MISMATCH"):
        rd_zh_tfidf.adapt_clustering_source(SOURCE)


def test_duplicate_patch_site_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    source = SOURCE + SOURCE
    monkeypatch.setattr(rd_zh_tfidf, "_PINNED_SOURCE_SHA256", sha256(source).hexdigest())
    with pytest.raises(ValueError, match="RD_ZH_VECTORIZER_SITE_MISMATCH"):
        rd_zh_tfidf.adapt_clustering_source(source)
