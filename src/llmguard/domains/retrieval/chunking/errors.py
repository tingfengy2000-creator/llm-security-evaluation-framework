"""Safe exception categories for deterministic chunking."""

from __future__ import annotations


class ChunkingError(ValueError):
    """Base class for chunking-domain validation failures."""


class ChunkingConfigurationError(ChunkingError):
    """Raised when a chunker receives an incompatible configuration."""


class ChunkingIntegrityError(ChunkingError):
    """Raised when a document's declared hash does not match its UTF-8 content."""


class ChunkingInputError(ChunkingError):
    """Raised when a chunking input is malformed without echoing sensitive text."""
