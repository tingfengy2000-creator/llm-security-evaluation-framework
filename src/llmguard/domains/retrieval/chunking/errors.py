"""Backward-compatible error re-exports for deterministic chunking behavior."""

from __future__ import annotations

from ..contracts.errors import (
    ChunkingConfigurationError,
    ChunkingContractError,
    ChunkingInputError,
    ChunkingIntegrityError,
)

ChunkingError = ChunkingContractError

__all__ = [
    "ChunkingConfigurationError",
    "ChunkingContractError",
    "ChunkingError",
    "ChunkingInputError",
    "ChunkingIntegrityError",
]
