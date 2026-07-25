"""Behavior-layer ports and deterministic test-only implementations for content resolution."""

from .errors import (
    ContentResolutionError,
    ContentResolutionIntegrityError,
    ContentResolutionLookupError,
    ContentResolutionRuntimeError,
)
from .in_memory import (
    InMemoryCorpusSnapshotReader,
    StaticApprovedCorpusSnapshotRegistry,
    StaticLegacyContentRefAdapter,
)
from .protocols import (
    ApprovedCorpusSnapshotRegistry,
    ContentResolver,
    CorpusSnapshotReader,
    LegacyContentRefAdapter,
)
from .resolver import CorpusContentResolver

__all__ = [
    "ApprovedCorpusSnapshotRegistry",
    "ContentResolutionError",
    "ContentResolutionIntegrityError",
    "ContentResolutionLookupError",
    "ContentResolutionRuntimeError",
    "ContentResolver",
    "CorpusContentResolver",
    "CorpusSnapshotReader",
    "InMemoryCorpusSnapshotReader",
    "LegacyContentRefAdapter",
    "StaticApprovedCorpusSnapshotRegistry",
    "StaticLegacyContentRefAdapter",
]
