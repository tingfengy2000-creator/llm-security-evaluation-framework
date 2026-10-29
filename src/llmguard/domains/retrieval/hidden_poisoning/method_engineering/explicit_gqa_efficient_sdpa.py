"""Local explicit-GQA memory-efficient SDPA adapter for the R05 precheck.

The persistent KV cache stays at the model's native head count. Each attention
call repeats those heads with the Transformers 4.57.1 contiguous ``repeat_kv``
pattern and then allows only ``SDPBackend.EFFICIENT_ATTENTION``.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

import torch
import torch.nn.functional as F
from torch.nn.attention import SDPBackend, sdpa_kernel

ATTN_KEY = "explicit_gqa_efficient_r05"
CONTRACT_RESERVED_BYTES = 32212254720
CONTRACT_HEADROOM_BYTES = 1073741824

# Fixed before any numerical comparison. Do not edit these after the first run.
NUMERICAL_ACCEPTANCE: dict[str, Any] = {
    "fixed_before_first_comparison": True,
    "version": "r05_precheck_v1",
    "rationale": (
        "Head mapping compares float32 MATH SDPA with enable_gqa against the same MATH kernel after a contiguous "
        "per-head repeat. A correct mapping is the same attention up to float32 rounding, so max_abs and relative_L2 "
        "must stay at or below 1e-5. Tiling the whole KV group instead of repeating each head assigns the wrong key "
        "head to a query head and produces an O(1) difference. The efficient-versus-expanded-MATH check uses bfloat16 "
        "inputs. Memory-efficient attention reduces differently from the math kernel, so the window is max_abs <= 2e-2, "
        "mean_abs <= 5e-3 and relative_L2 <= 2e-2, with no NaN or Inf. That window checks attention outputs, not token "
        "identity, and is not revised after the first comparison."
    ),
    "head_mapping_math_vs_math": {"dtype": "float32", "max_abs_max": 1e-5, "relative_l2_max": 1e-5},
    "efficient_vs_expanded_math": {"dtype": "bfloat16", "max_abs_max": 2e-2, "mean_abs_max": 5e-3, "relative_l2_max": 2e-2},
    "determinism_token_ids": "exact_equal",
    "capacity_reserved_bytes_max": CONTRACT_RESERVED_BYTES,
    "capacity_minimum_contract_headroom_bytes": CONTRACT_HEADROOM_BYTES,
    "efficient_operator_substrings": ["_efficient_attention_forward", "_scaled_dot_product_efficient_attention"],
    "math_kernel_forbidden_substring": "softmax_warp_forward",
    "forbidden_backend_substrings": ["_scaled_dot_product_flash_attention", "cudnn_attention", "_scaled_dot_product_cudnn"],
}

CALLS: Counter[tuple] = Counter()
FIRST_PREFILL: dict[str, Any] | None = None
FIRST_DECODE: dict[str, Any] | None = None


def repeat_kv_contiguous(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    """Repeat each KV head ``n_rep`` times in head order. This is the 4.57.1 ``repeat_kv`` pattern."""
    batch, heads, seq, dim = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    return hidden_states[:, :, None, :, :].expand(batch, heads, n_rep, seq, dim).reshape(batch, heads * n_rep, seq, dim)


def assert_contiguous_repeat(source: torch.Tensor, expanded: torch.Tensor, n_rep: int) -> None:
    if n_rep == 1:
        return
    for head in (0, source.shape[1] - 1):
        for repeat in (0, n_rep - 1):
            got = expanded[:, head * n_rep + repeat, :1]
            expected = source[:, head, :1]
            if not torch.equal(got, expected):
                raise RuntimeError("HEAD_REPEAT_MAPPING")


def kernel_correspondence(named_events: list[tuple[str, list[str]]]) -> dict[str, Any]:
    """Require the launching efficient op to have a CUDA kernel.

    The dispatcher aten::_scaled_dot_product_efficient_attention does not launch
    a kernel itself. An empty kernel list on that wrapper is not a math fallback.
    """
    matched: list[dict[str, Any]] = []
    forbidden: list[str] = []
    math_hits: list[Any] = []
    for name, kernels in named_events:
        if any(token in name for token in NUMERICAL_ACCEPTANCE["efficient_operator_substrings"]):
            matched.append({"op": name, "kernels": list(kernels)})
        if any(token in name for token in NUMERICAL_ACCEPTANCE["forbidden_backend_substrings"]):
            forbidden.append(name)
        if NUMERICAL_ACCEPTANCE["math_kernel_forbidden_substring"] in name or any(
            NUMERICAL_ACCEPTANCE["math_kernel_forbidden_substring"] in kernel for kernel in kernels
        ):
            math_hits.append(name or kernels)
    launchers = [item for item in matched if str(item["op"]).endswith("_efficient_attention_forward")]
    proved = bool(launchers) and all(item["kernels"] for item in launchers) and not forbidden and not math_hits
    return {
        "efficient_ops": matched,
        "forbidden_backend_ops": forbidden,
        "math_kernel_hits": math_hits,
        "efficient_kernel_proved": proved,
    }


def difference_stats(actual: torch.Tensor, reference: torch.Tensor) -> dict[str, float | bool]:
    delta = (actual.float() - reference.float()).abs()
    denom = reference.float().norm().clamp_min(1e-12)
    return {
        "max_abs": float(delta.max()),
        "mean_abs": float(delta.mean()),
        "relative_l2": float(delta.pow(2).sum().sqrt() / denom),
        "nan_inf": not bool(torch.isfinite(actual).all() and torch.isfinite(reference).all()),
    }


def _math_attention(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, *, enable_gqa: bool, is_causal: bool, attn_mask: torch.Tensor | None, scale: float) -> torch.Tensor:
    with sdpa_kernel(SDPBackend.MATH):
        return F.scaled_dot_product_attention(query, key, value, attn_mask=attn_mask, dropout_p=0.0, is_causal=is_causal, scale=scale, enable_gqa=enable_gqa)


def _efficient_attention(query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, *, is_causal: bool, attn_mask: torch.Tensor | None, scale: float) -> torch.Tensor:
    with sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION):
        return F.scaled_dot_product_attention(query, key, value, attn_mask=attn_mask, dropout_p=0.0, is_causal=is_causal, scale=scale, enable_gqa=False)


def synthetic_parity(device: torch.device | str = "cuda") -> dict[str, Any]:
    """Compare mapping and backends on synthetic tensors. Uses the pre-registered windows."""
    generator = torch.Generator(device="cpu")
    generator.manual_seed(20261029)
    cases = []
    specs = [
        {"name": "causal_prefill", "q_len": 32, "k_len": 32, "mask": None, "is_causal": True},
        {"name": "single_token_decode", "q_len": 1, "k_len": 32, "mask": None, "is_causal": False},
        {"name": "cached_multistep_decode", "q_len": 1, "k_len": 36, "mask": None, "is_causal": False},
        {"name": "explicit_causal_mask", "q_len": 16, "k_len": 16, "mask": "causal4d", "is_causal": False},
    ]
    passed = True
    for spec in specs:
        q = torch.randn(1, 28, spec["q_len"], 128, generator=generator)
        k = torch.randn(1, 4, spec["k_len"], 128, generator=generator)
        v = torch.randn(1, 4, spec["k_len"], 128, generator=generator)
        mask = None
        if spec["mask"] == "causal4d":
            positions = torch.arange(spec["k_len"])
            allowed = positions[None, :] <= torch.arange(spec["q_len"])[:, None]
            mask = torch.zeros(1, 1, spec["q_len"], spec["k_len"])
            mask = mask.masked_fill(~allowed[None, None], float("-inf"))
        scale = 128 ** -0.5
        try:
            q32, k32, v32 = q.to(device), k.to(device), v.to(device)
            mask32 = None if mask is None else mask.to(device)
            native = _math_attention(q32, k32, v32, enable_gqa=True, is_causal=spec["is_causal"], attn_mask=mask32, scale=scale)
            expanded_k = repeat_kv_contiguous(k32, 7).contiguous()
            expanded_v = repeat_kv_contiguous(v32, 7).contiguous()
            assert_contiguous_repeat(k32, expanded_k, 7)
            expanded = _math_attention(q32, expanded_k, expanded_v, enable_gqa=False, is_causal=spec["is_causal"], attn_mask=mask32, scale=scale)
            mapping = difference_stats(expanded, native)
            q16 = q.to(device=device, dtype=torch.bfloat16)
            k16 = k.to(device=device, dtype=torch.bfloat16)
            v16 = v.to(device=device, dtype=torch.bfloat16)
            mask16 = None if mask is None else mask.to(device=device, dtype=torch.bfloat16)
            ek = repeat_kv_contiguous(k16, 7).contiguous()
            ev = repeat_kv_contiguous(v16, 7).contiguous()
            reference = _math_attention(q16, ek, ev, enable_gqa=False, is_causal=spec["is_causal"], attn_mask=mask16, scale=scale)
            efficient = _efficient_attention(q16, ek, ev, is_causal=spec["is_causal"], attn_mask=mask16, scale=scale)
            backend = difference_stats(efficient, reference)
        except Exception as exc:  # noqa: BLE001 — one original failure stops this phase; no second algorithm
            cases.append({"name": spec["name"], "error": f"{type(exc).__name__}: {exc}"})
            return {"pass": False, "acceptance": NUMERICAL_ACCEPTANCE, "cases": cases}
        mapping_gate = NUMERICAL_ACCEPTANCE["head_mapping_math_vs_math"]
        backend_gate = NUMERICAL_ACCEPTANCE["efficient_vs_expanded_math"]
        mapping_pass = (not mapping["nan_inf"]) and mapping["max_abs"] <= mapping_gate["max_abs_max"] and mapping["relative_l2"] <= mapping_gate["relative_l2_max"]
        backend_pass = (not backend["nan_inf"]) and backend["max_abs"] <= backend_gate["max_abs_max"] and backend["mean_abs"] <= backend_gate["mean_abs_max"] and backend["relative_l2"] <= backend_gate["relative_l2_max"]
        cases.append({"name": spec["name"], "mapping": mapping, "mapping_pass": mapping_pass, "efficient_vs_expanded_math": backend, "efficient_pass": backend_pass})
        if not (mapping_pass and backend_pass):
            return {"pass": False, "acceptance": NUMERICAL_ACCEPTANCE, "cases": cases}
    return {"pass": passed, "acceptance": NUMERICAL_ACCEPTANCE, "cases": cases}


def _reset_call_log() -> None:
    global FIRST_PREFILL, FIRST_DECODE
    CALLS.clear()
    FIRST_PREFILL = None
    FIRST_DECODE = None


def explicit_gqa_efficient_attention_forward(module: torch.nn.Module, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, attention_mask: torch.Tensor | None, dropout: float = 0.0, scaling: float | None = None, is_causal: bool | None = None, **kwargs: Any) -> tuple[torch.Tensor, None]:
    global FIRST_PREFILL, FIRST_DECODE
    if kwargs.get("output_attentions") or kwargs.get("head_mask") is not None:
        raise RuntimeError("OUTPUT_ATTENTIONS_OR_HEAD_MASK_NOT_SUPPORTED")
    sliding = kwargs.get("sliding_window", getattr(module, "sliding_window", None))
    if sliding is not None:
        raise RuntimeError("SLIDING_WINDOW_PRESENT_STOP")
    groups = int(module.num_key_value_groups)
    if key.shape[1] * groups != query.shape[1] or value.shape != key.shape:
        raise RuntimeError("GQA_HEAD_COUNT")
    key_expanded = repeat_kv_contiguous(key, groups).contiguous()
    value_expanded = repeat_kv_contiguous(value, groups).contiguous()
    assert_contiguous_repeat(key, key_expanded, groups)
    if attention_mask is not None and attention_mask.ndim == 4:
        attention_mask = attention_mask[:, :, :, : key_expanded.shape[-2]]
    if is_causal is None:
        is_causal = bool(query.shape[2] > 1 and attention_mask is None and getattr(module, "is_causal", True))
    signature = (int(query.shape[2]), int(key.shape[-2]), int(key.shape[1]), int(key_expanded.shape[1]), False, attention_mask is None, bool(is_causal), str(query.dtype), "EFFICIENT_ATTENTION")
    CALLS[signature] += 1
    record = {
        "query": list(query.shape), "key": list(key.shape), "value": list(value.shape),
        "expanded_key": list(key_expanded.shape), "enable_gqa": False,
        "attn_mask": None if attention_mask is None else {"shape": list(attention_mask.shape), "dtype": str(attention_mask.dtype)},
        "is_causal": bool(is_causal), "dtype": str(query.dtype), "dropout": float(dropout), "scale": None if scaling is None else float(scaling),
        "backend": "EFFICIENT_ATTENTION",
    }
    if query.shape[2] > 1 and FIRST_PREFILL is None:
        FIRST_PREFILL = record
    if query.shape[2] == 1 and FIRST_DECODE is None:
        FIRST_DECODE = record
    with sdpa_kernel(SDPBackend.EFFICIENT_ATTENTION):
        output = F.scaled_dot_product_attention(query, key_expanded, value_expanded, attn_mask=attention_mask, dropout_p=dropout, scale=scaling, is_causal=bool(is_causal), enable_gqa=False)
    return output.transpose(1, 2).contiguous(), None


def install(model: torch.nn.Module) -> str:
    from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS

    sliding = [layer.self_attn.sliding_window for layer in model.model.layers]
    if any(window is not None for window in sliding):
        raise RuntimeError("SLIDING_WINDOW_PRESENT_STOP")
    previous = model.config._attn_implementation
    ALL_ATTENTION_FUNCTIONS[ATTN_KEY] = explicit_gqa_efficient_attention_forward
    model.config._attn_implementation = ATTN_KEY
    _reset_call_log()
    return str(previous)


def uninstall(model: torch.nn.Module, previous: str) -> None:
    from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS

    model.config._attn_implementation = previous
    if ATTN_KEY in ALL_ATTENTION_FUNCTIONS:
        del ALL_ATTENTION_FUNCTIONS[ATTN_KEY]


def call_summary() -> dict[str, Any]:
    return {
        "signatures": [{"query_len": k[0], "key_len": k[1], "kv_heads": k[2], "expanded_heads": k[3], "enable_gqa": k[4], "mask_is_none": k[5], "is_causal": k[6], "dtype": k[7], "backend": k[8], "count": v} for k, v in sorted(CALLS.items())],
        "first_prefill": FIRST_PREFILL,
        "first_decode": FIRST_DECODE,
    }


def cache_head_counts(past: Any) -> list[int]:
    layers = getattr(past, "layers", None)
    if not layers:
        raise RuntimeError("CACHE_LAYOUT_UNKNOWN")
    counts = []
    for layer in layers:
        keys = getattr(layer, "keys", None)
        if keys is None or keys.ndim != 4:
            raise RuntimeError("CACHE_LAYOUT_UNKNOWN")
        counts.append(int(keys.shape[1]))
    return counts
