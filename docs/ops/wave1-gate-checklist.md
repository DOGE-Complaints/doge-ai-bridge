# Wave-1 gate checklist (executable)

**Story:** STORY-AIBRIDGE-06 · **Arch:** [00-overview.md §7](../architecture/runtime/00-overview.md) · [04-ops-security.md §6](../architecture/runtime/04-ops-security.md)

Live n8n call is **manual ops proof** (not required in CI). Automated parts: `/readyz`, 401 smoke, `/metrics` privacy tests.

**Full R3-P1-09 / §6.1 live gate (STORY-AIBRIDGE-15):** [n8n-channel-workflow/r3-p1-09-live-gate-checklist.md](./n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) — this wave-1 file stays the shorter façade smoke.

**R3-P1-08 SPA HTTPS continuation (STORY-AIBRIDGE-17 tracker):** [r3-p1-08-spa-https-continuation-gate.md](./r3-p1-08-spa-https-continuation-gate.md) — spa owns device evidence; aibridge does not invent spa UI.

## Checklist

1. [ ] Image / process up; migrations + current content bundle registered (when content configured).
2. [ ] `GET /readyz` → `200` `{"status":"ready"}` with distinct channel vs gateway Bearers.
3. [ ] Smoke: `POST /v1/channel/turns` **without** Bearer → **401**.
4. [ ] Live n8n → `POST /v1/channel/turns` with channel Bearer (private net):
   - Interview / dry-run path only.
   - **No** real gateway stash (`AIBRIDGE_DRY_RUN=true` or do not consume Send).
5. [ ] `GET /metrics` (private) returns Prometheus series **without** narrative/PII/secrets.
6. [ ] Budget / gateway env **names** present in `.env.example` (numeric values may stay unset).

## Automated smoke (dev)

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_ops_wave1.py
```

## Manual n8n proof (ops)

1. Confirm n8n Header Auth = `AIBRIDGE_CHANNEL_BEARER_TOKEN` only.
2. Trigger Telegram message → workflow → `/v1/channel/turns`.
3. Confirm reply envelope; confirm no `POST /story-drafts` when dry-run.
4. Record proof in ops notes (outside git secrets).
