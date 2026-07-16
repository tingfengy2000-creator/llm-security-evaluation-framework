"""Pinned SentenceTransformers provider with lazy, explicit model loading."""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable, Mapping, Sequence
from types import MappingProxyType
from typing import Protocol, cast

from .base import (
    EmbeddingBatch,
    EmbeddingConfigurationError,
    EmbeddingDimensionError,
    EmbeddingInputError,
    EmbeddingModelLoadError,
    EmbeddingRuntimeError,
    EmbeddingVector,
    validate_embedding_batch,
    validate_text_batch,
)
from .model_spec import EmbeddingModelSpec


class _SentenceTransformerModel(Protocol):
    def encode(self, texts: Sequence[str], **kwargs: object) -> object:
        """Return one embedding per requested text."""


ModelLoader = Callable[..., _SentenceTransformerModel]


def _load_sentence_transformer(**kwargs: object) -> _SentenceTransformerModel:
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as error:
        raise EmbeddingModelLoadError(
            "sentence-transformers dependency is unavailable"
        ) from error
    return cast(_SentenceTransformerModel, SentenceTransformer(**kwargs))


class SentenceTransformerEmbeddingProvider:
    """Embed text with an immutable SentenceTransformers model specification."""

    def __init__(
        self,
        model_spec: EmbeddingModelSpec,
        *,
        model_loader: ModelLoader | None = None,
    ) -> None:
        if model_spec.provider != "sentence_transformers":
            raise EmbeddingConfigurationError(
                "SentenceTransformerEmbeddingProvider requires "
                "model_spec.provider='sentence_transformers'"
            )
        self._model_spec = model_spec
        self._model_loader = model_loader or _load_sentence_transformer
        self._model: _SentenceTransformerModel | None = None

    @property
    def model_spec(self) -> EmbeddingModelSpec:
        return self._model_spec

    @property
    def dimension(self) -> int:
        return self._model_spec.dimension

    def embed_documents(self, texts: Sequence[str]) -> EmbeddingBatch:
        validated_texts = validate_text_batch(texts)
        return self._embed_batch(
            tuple(f"{self.model_spec.document_prefix}{text}" for text in validated_texts)
        )

    def embed_query(self, text: str) -> EmbeddingVector:
        if not isinstance(text, str) or not text.strip():
            raise EmbeddingInputError("query text must be nonblank")
        return self._embed_batch((f"{self.model_spec.query_prefix}{text}",))[0]

    def runtime_metadata(self) -> Mapping[str, str | int | bool]:
        """Return safe reproducibility metadata without cache paths or input content."""

        try:
            dependency_version = importlib.metadata.version("sentence-transformers")
        except importlib.metadata.PackageNotFoundError:
            dependency_version = "unavailable"
        return MappingProxyType(
            {
                "dependency_version": dependency_version,
                "dimension": self.dimension,
                "implementation_version": self.model_spec.implementation_version,
                "model_id": self.model_spec.model_id,
                "normalize_embeddings": self.model_spec.normalize_embeddings,
                "provider": self.model_spec.provider,
                "revision": self.model_spec.revision,
            }
        )

    def _embed_batch(self, prepared_texts: tuple[str, ...]) -> EmbeddingBatch:
        if not prepared_texts:
            return ()
        model = self._get_model()
        try:
            output = model.encode(
                list(prepared_texts),
                batch_size=self.model_spec.batch_size,
                show_progress_bar=False,
                precision=self.model_spec.expected_output_dtype,
                convert_to_numpy=True,
                convert_to_tensor=False,
                normalize_embeddings=self.model_spec.normalize_embeddings,
                device=self.model_spec.device,
            )
        except Exception as error:
            raise EmbeddingRuntimeError("SentenceTransformers embedding execution failed") from error
        try:
            return validate_embedding_batch(
                self._to_numeric_rows(output),
                expected_count=len(prepared_texts),
                expected_dimension=self.dimension,
            )
        except (EmbeddingDimensionError, EmbeddingRuntimeError):
            raise
        except Exception as error:
            raise EmbeddingRuntimeError("SentenceTransformers returned invalid embeddings") from error

    def _get_model(self) -> _SentenceTransformerModel:
        if self._model is not None:
            return self._model
        try:
            model = self._model_loader(
                model_name_or_path=self.model_spec.model_id,
                revision=self.model_spec.revision,
                device=self.model_spec.device,
                trust_remote_code=False,
                local_files_only=self.model_spec.local_files_only,
            )
        except EmbeddingModelLoadError:
            raise
        except Exception as error:
            raise EmbeddingModelLoadError(
                "unable to load the configured SentenceTransformers model"
            ) from error
        self._model = model
        return model

    @staticmethod
    def _to_numeric_rows(output: object) -> Sequence[Sequence[float]]:
        raw_output: object = output.tolist() if hasattr(output, "tolist") else output
        if not isinstance(raw_output, Sequence) or isinstance(
            raw_output,
            (str, bytes, bytearray),
        ):
            raise EmbeddingRuntimeError("SentenceTransformers output must be a vector batch")
        rows: list[Sequence[float]] = []
        for row in raw_output:
            numeric_row: object = row.tolist() if hasattr(row, "tolist") else row
            if not isinstance(numeric_row, Sequence) or isinstance(
                numeric_row,
                (str, bytes, bytearray),
            ):
                raise EmbeddingRuntimeError("SentenceTransformers output row is invalid")
            rows.append(cast(Sequence[float], numeric_row))
        return rows


__all__ = ["SentenceTransformerEmbeddingProvider"]
