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


class RetrievalContractError(ValueError):
    """Base error for retrieval runtime contracts without input echoing."""

    error_code = "RETRIEVAL_CONTRACT_ERROR"

    def __init__(self, message: str, *, error_code: str | None = None) -> None:
        if error_code is not None:
            self.error_code = error_code
        super().__init__(f"{message} [{self.error_code}]")


class RetrievalConfigurationError(RetrievalContractError):
    """Raised when immutable retrieval configuration is invalid."""

    error_code = "RETRIEVAL_CONFIGURATION_INVALID"


class RetrievalInputError(RetrievalContractError):
    """Raised when a runtime record is malformed or unsafe."""

    error_code = "RETRIEVAL_INPUT_INVALID"


class RetrievalIntegrityError(RetrievalContractError):
    """Raised when a derived retrieval identity does not match its inputs."""

    error_code = "RETRIEVAL_INTEGRITY_ERROR"


class RetrievalProjectionError(RetrievalInputError):
    """Raised when evaluator-facing query data crosses the runtime boundary."""

    error_code = "UNSAFE_QUERY_PROJECTION"


class ContentRefError(RetrievalInputError):
    """Raised when an opaque content reference is not safe to persist."""

    error_code = "INVALID_CONTENT_REF"
