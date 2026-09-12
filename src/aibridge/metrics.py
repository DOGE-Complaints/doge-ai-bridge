"""Prometheus-compatible metrics — no PII / narrative / secrets (story 06)."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


# Coarse label allowlist — never free-form resident text.
_ALLOWED_BUDGET_REASONS = frozenset(
    {
        "budget_session_turns",
        "budget_openai_timeout",
        "budget_responses_calls",
        "budget_tool_calls",
        "budget_input_tokens",
        "budget_output_tokens",
    }
)


@dataclass
class MetricsRegistry:
    """In-process counters for pilot /metrics (private network assumed)."""

    _lock: Lock = field(default_factory=Lock)
    channel_turns_total: int = 0
    channel_actions_total: int = 0
    channel_http_errors_total: int = 0
    gateway_posts_total: int = 0
    openai_calls_total: int = 0
    budget_stops_total: dict[str, int] = field(default_factory=dict)

    def inc_turns(self) -> None:
        with self._lock:
            self.channel_turns_total += 1

    def inc_actions(self) -> None:
        with self._lock:
            self.channel_actions_total += 1

    def inc_http_errors(self) -> None:
        with self._lock:
            self.channel_http_errors_total += 1

    def inc_gateway_posts(self) -> None:
        with self._lock:
            self.gateway_posts_total += 1

    def inc_openai_calls(self) -> None:
        with self._lock:
            self.openai_calls_total += 1

    def record_budget_stop(self, reason: str) -> None:
        """Record redacted budget-stop reason only (allowlisted)."""
        key = reason if reason in _ALLOWED_BUDGET_REASONS else "budget_other"
        with self._lock:
            self.budget_stops_total[key] = self.budget_stops_total.get(key, 0) + 1

    def render_prometheus(self) -> str:
        """Prometheus text exposition — labels are coarse enums only."""
        with self._lock:
            lines = [
                "# HELP aibridge_channel_turns_total Channel turn requests processed.",
                "# TYPE aibridge_channel_turns_total counter",
                f"aibridge_channel_turns_total {self.channel_turns_total}",
                "# HELP aibridge_channel_actions_total Channel action requests processed.",
                "# TYPE aibridge_channel_actions_total counter",
                f"aibridge_channel_actions_total {self.channel_actions_total}",
                "# HELP aibridge_channel_http_errors_total Channel HTTP error responses.",
                "# TYPE aibridge_channel_http_errors_total counter",
                f"aibridge_channel_http_errors_total {self.channel_http_errors_total}",
                "# HELP aibridge_gateway_posts_total Gateway stash HTTP posts attempted.",
                "# TYPE aibridge_gateway_posts_total counter",
                f"aibridge_gateway_posts_total {self.gateway_posts_total}",
                "# HELP aibridge_openai_calls_total OpenAI Responses calls.",
                "# TYPE aibridge_openai_calls_total counter",
                f"aibridge_openai_calls_total {self.openai_calls_total}",
                "# HELP aibridge_budget_stops_total LLM budget stop events by reason.",
                "# TYPE aibridge_budget_stops_total counter",
            ]
            if not self.budget_stops_total:
                lines.append('aibridge_budget_stops_total{reason="none"} 0')
            else:
                for reason, count in sorted(self.budget_stops_total.items()):
                    lines.append(
                        f'aibridge_budget_stops_total{{reason="{reason}"}} {count}'
                    )
            lines.append("")
            return "\n".join(lines)

    def contains_forbidden_text(self, needle: str) -> bool:
        """True if needle appears in rendered metrics (must stay False for narratives)."""
        if not needle:
            return False
        return needle in self.render_prometheus()


_default_metrics: MetricsRegistry | None = None


def get_metrics() -> MetricsRegistry:
    global _default_metrics
    if _default_metrics is None:
        _default_metrics = MetricsRegistry()
    return _default_metrics


def reset_metrics(registry: MetricsRegistry | None = None) -> MetricsRegistry:
    global _default_metrics
    _default_metrics = registry if registry is not None else MetricsRegistry()
    return _default_metrics


def assert_no_narrative_in_metrics(text: str, *, sample: str) -> None:
    """Test helper — narrative sample must not appear in metrics body."""
    if sample and sample in text:
        raise AssertionError("narrative/PII sample leaked into /metrics")
