"""Stable, redacted exceptions shared by chunking contracts and behavior."""

from __future__ import annotations


class ChunkingContractError(ValueError):
    """Base error for chunking contracts without sensitive input echoing."""

    error_code = "CHUNKING_CONTRACT_ERROR"

    def __init__(self, message: str, *, error_code: str | None = None) -> None:
        super().__init__(message)
        if error_code is not None:
            self.error_code = error_code


class ChunkingConfigurationError(ChunkingContractError):
    """Raised when a strategy configuration is invalid or incompatible."""

    error_code = "CHUNKING_CONFIGURATION_INVALID"


class ChunkingIntegrityError(ChunkingContractError):
    """Raised when a declared hash or canonical identity does not match data."""

    error_code = "CHUNKING_INTEGRITY_ERROR"


class ChunkingInputError(ChunkingContractError):
    """Raised when a contract input is malformed or unsafe for public use."""

    error_code = "CHUNKING_INPUT_INVALID"
