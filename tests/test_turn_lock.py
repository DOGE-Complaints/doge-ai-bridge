"""t03 — per-session turn serialization."""

from __future__ import annotations

import threading
import time

from aibridge.interview import default_recording_engine
from aibridge.turn_lock import SessionTurnLock


def test_session_turn_lock_serializes_same_session() -> None:
    locks = SessionTurnLock()
    order: list[str] = []

    def worker(label: str) -> None:
        with locks.hold("sess-a"):
            order.append(f"{label}-enter")
            time.sleep(0.05)
            order.append(f"{label}-exit")

    t1 = threading.Thread(target=worker, args=("a",))
    t2 = threading.Thread(target=worker, args=("b",))
    t1.start()
    time.sleep(0.01)
    t2.start()
    t1.join()
    t2.join()
    assert order in (
        ["a-enter", "a-exit", "b-enter", "b-exit"],
        ["b-enter", "b-exit", "a-enter", "a-exit"],
    )


def test_interview_parallel_tool_calls_false() -> None:
    engine = default_recording_engine(tools=[{"type": "function", "function": {"name": "t"}}])
    engine.run_turn(session_id="s", user_text="hi")
    assert engine.client.calls[0]["parallel_tool_calls"] is False  # type: ignore[attr-defined]


def test_is_active_while_held() -> None:
    locks = SessionTurnLock()
    assert locks.is_active("x") is False
    with locks.hold("x"):
        assert locks.is_active("x") is True
    assert locks.is_active("x") is False
