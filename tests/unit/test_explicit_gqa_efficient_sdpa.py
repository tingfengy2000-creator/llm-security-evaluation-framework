"""CPU checks for the R05 explicit GQA repeat. No model, labels, or GPU comparison."""
from __future__ import annotations

import inspect

import torch
from transformers.integrations.sdpa_attention import repeat_kv

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.explicit_gqa_efficient_sdpa import (
    NUMERICAL_ACCEPTANCE,
    assert_contiguous_repeat,
    explicit_gqa_efficient_attention_forward,
    kernel_correspondence,
    repeat_kv_contiguous,
)


def test_repeat_matches_transformers_457_and_not_a_whole_group_tile() -> None:
    source = torch.arange(4, dtype=torch.float32).view(1, 4, 1, 1).expand(1, 4, 3, 2).contiguous()
    ours = repeat_kv_contiguous(source, 7)
    official = repeat_kv(source, 7)
    assert torch.equal(ours, official)
    for head in range(4):
        for repeat in range(7):
            assert torch.equal(ours[:, head * 7 + repeat], source[:, head])
    tiled = source.repeat(1, 7, 1, 1)
    assert not torch.equal(tiled, ours)
    assert_contiguous_repeat(source, ours, 7)


def test_acceptance_window_is_fixed_before_comparison() -> None:
    assert NUMERICAL_ACCEPTANCE["fixed_before_first_comparison"] is True
    assert NUMERICAL_ACCEPTANCE["head_mapping_math_vs_math"]["max_abs_max"] == 1e-5
    assert NUMERICAL_ACCEPTANCE["efficient_vs_expanded_math"]["max_abs_max"] == 2e-2
    assert NUMERICAL_ACCEPTANCE["capacity_minimum_contract_headroom_bytes"] == 1073741824
    assert NUMERICAL_ACCEPTANCE["determinism_token_ids"] == "exact_equal"


def test_model_adapter_source_allows_only_efficient_attention() -> None:
    source = inspect.getsource(explicit_gqa_efficient_attention_forward)
    assert "SDPBackend.EFFICIENT_ATTENTION" in source
    assert "enable_gqa=False" in source
    assert "SDPBackend.MATH" not in source
    assert "SDPBackend.CUDNN_ATTENTION" not in source
    assert "repeat_kv_contiguous" in source


def test_dispatcher_wrapper_without_a_kernel_does_not_hide_the_launcher() -> None:
    proved = kernel_correspondence(
        [
            ("aten::_scaled_dot_product_efficient_attention", []),
            ("aten::_efficient_attention_forward", ["fmha_cutlassF_bf16_PyTorchMemEffAttention"]),
        ]
    )
    assert proved["efficient_kernel_proved"] is True


def test_wrapper_alone_or_math_softmax_does_not_prove_efficient_attention() -> None:
    wrapper_only = kernel_correspondence([("aten::_scaled_dot_product_efficient_attention", [])])
    math_fallback = kernel_correspondence(
        [("aten::_efficient_attention_forward", ["softmax_warp_forward"])]
    )
    assert wrapper_only["efficient_kernel_proved"] is False
    assert math_fallback["efficient_kernel_proved"] is False
