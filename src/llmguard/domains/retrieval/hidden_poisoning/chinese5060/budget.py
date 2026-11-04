"""Pure admission check only; this is not a provider invoice or a new ledger."""
from __future__ import annotations

from decimal import Decimal


def admit_paid_batch(*, cumulative_usd: Decimal | None, pending_usd: Decimal | None,
                     account_remaining_usd: Decimal | None, next_upper_usd: Decimal,
                     billing_verified: bool) -> str:
    """Inputs include ALL prior generation/verification/judging/probes this round.

    Conversion into USD requires a separately frozen conservative currency rule.
    Uncertain invoice, missing usage, reserves or remaining funds block execution.
    One future request is one batch; an admitted batch still needs protocol gates.
    """
    values = (cumulative_usd, pending_usd, account_remaining_usd)
    if not billing_verified or any(v is None for v in values):
        return "BLOCKED_UNVERIFIED_BILLING_OR_BALANCE"
    assert cumulative_usd is not None and pending_usd is not None
    assert account_remaining_usd is not None
    amounts = (cumulative_usd, pending_usd, account_remaining_usd, next_upper_usd)
    if any(not v.is_finite() or v < 0 for v in amounts) or next_upper_usd == 0:
        raise ValueError("INVALID_MONEY_OR_UNBOUNDED_BATCH")
    projected = cumulative_usd + pending_usd + next_upper_usd
    if cumulative_usd + pending_usd >= Decimal("28") or projected >= Decimal("28"):
        return "STOP_NEW_BATCH_28_USD"
    if pending_usd + next_upper_usd > account_remaining_usd:
        return "BLOCKED_INSUFFICIENT_ACCOUNT_BALANCE"
    return "ADMIT_WITH_25_USD_WARNING" if projected >= Decimal("25") else "ADMIT_BUDGET_ONLY"
