"""Pure 3+105 progression guard for the conditional Pilot."""
from __future__ import annotations

from .pilot_admission import MAX_CALLS, Stop


class StageProgress:
    """One outstanding slot. A failed or unresolved request has no continuation."""

    def __init__(self) -> None:
        self._outcomes = ["NOT_RUN"] * MAX_CALLS
        self._next = 0
        self._in_flight = False
        self._stopped = False

    @property
    def initial3_passed(self) -> bool:
        return self._outcomes[:3] == ["SUCCESS"] * 3

    @property
    def outcomes(self) -> tuple[str, ...]:
        return tuple(self._outcomes)

    def begin(self) -> int:
        if self._stopped or self._in_flight or self._next >= MAX_CALLS:
            raise Stop("STAGE_NO_FURTHER_SEND")
        if self._next >= 3 and not self.initial3_passed:
            raise Stop("INITIAL_THREE_NOT_PASSED")
        self._in_flight = True
        return self._next + 1

    def finish(self, ordinal: int, *, engineering_success: bool) -> None:
        if not self._in_flight or ordinal != self._next + 1:
            raise Stop("STAGE_RESULT_ORDER_DRIFT")
        self._outcomes[self._next] = "SUCCESS" if engineering_success else "FAIL"
        self._in_flight = False
        self._next += 1
        self._stopped = not engineering_success
