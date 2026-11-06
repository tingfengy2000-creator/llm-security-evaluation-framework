"""Build the isolated RD-zh Stage 1 source from the fixed B2 checkout."""
from __future__ import annotations

from hashlib import sha256

# SecAI-Lab/RAGDefender ba2a17efba165d45409114df2d70b030ade1e1b8.
_PINNED_SOURCE_SHA256 = "2daadad505f95f682cd311d03b2119201fcf8dbca30e9948b1bdf968c95d1658"
_B2_VECTORIZER = (
    b"        stop_words = list(_text.ENGLISH_STOP_WORDS)\n"
    b"        tfidf = _text.TfidfVectorizer(stop_words=stop_words)\n"
)
_RD_ZH_VECTORIZER = b'        tfidf = _text.TfidfVectorizer(analyzer="char", ngram_range=(2, 2), stop_words=None)\n'


def adapt_clustering_source(source: bytes) -> bytes:
    """Return a one-site patch without loading RAGDefender or an encoder."""
    if sha256(source.replace(b"\r\n", b"\n")).hexdigest() != _PINNED_SOURCE_SHA256:
        raise ValueError("RD_ZH_UPSTREAM_CLUSTERING_SOURCE_MISMATCH")
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    original = _B2_VECTORIZER.replace(b"\n", newline)
    if source.count(original) != 1:
        raise ValueError("RD_ZH_VECTORIZER_SITE_MISMATCH")
    return source.replace(original, _RD_ZH_VECTORIZER.replace(b"\n", newline), 1)
