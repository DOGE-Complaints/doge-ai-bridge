# LF triage — telegram-ops-turn-redact-summary (2026-11-06)

**Prompt:** [`lightweight-followup-triage.md`](../methodology/Zeya888-builder-queue/prompts/operator/lightweight-followup-triage.md)  
**Guide:** [`lightweight-followup.md`](../methodology/Zeya888-builder-queue/guides/lightweight-followup.md) §3  
**builder_project:** `telegram`  
**$gap:** Soft §4.6 — cannot rebuild dialogue from ops logs (Pille UX gap)  
**$parentStoryOrPkg:** STORY-TELEGRAM-01…04 Done (channel transport)  
**UX triage:** [`req15-tg-interviewer-ux-gap-triage-2026-11-06.md`](./req15-tg-interviewer-ux-gap-triage-2026-11-06.md)

## Restate ask

Append **redacted, length-capped** turn/outbound summary fields to Present telegram ops log lines so future G4 transcripts need less copy-paste. No new API, no full message body dump, no PII.

## Hard HIT

| HIT | Verdict | Evidence |
|-----|---------|----------|
| 1 | clear | No new STORY — post-Done transport hygiene |
| 2 | clear | No new route/schema/API; enrich Present `logger.info` ops |
| 3 | clear | Append on existing poller/outbound log path |
| 4 | clear | Single concern: ops observability |
| 5 | clear | Redaction lock — no secrets/full bodies |
| 6 | clear | Parent TG stories Done |
| 7 | clear | No P2–P7 required |
| 8 | clear | `telegram` only |
| 9 | clear | Lock: prefix + max length; no invent full transcript store |
| 10 | clear | Touch ≤ poller/outbound (+ tests) |

## Verdict

**PASS** — author dual plans under doge-telegram analysis.  
**Plans:** [`doge-telegram/docs/analysis/telegram-ops-turn-redact-summary.md`](../../doge-telegram/docs/analysis/telegram-ops-turn-redact-summary.md) · [`…-validate.md`](../../doge-telegram/docs/analysis/telegram-ops-turn-redact-summary-validate.md) · [LAUNCH](../../doge-telegram/docs/tasks/prompts/telegram-ops-turn-redact-summary-LAUNCH.md)
