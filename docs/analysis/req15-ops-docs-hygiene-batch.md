# Implement — req15-ops-docs-hygiene-batch

**Project:** DOGEstonia root (cross-project)  
**Execute in:** monorepo / root workspace chat  
**builder_project:** `n/a` (docs span aibridge + telegram + root analysis)  
**Triage:** PASS — [`req15-lf-triage-ops-docs-hygiene-batch-2026-11-03.md`](./req15-lf-triage-ops-docs-hygiene-batch-2026-11-03.md)  
**Validate:** [`req15-ops-docs-hygiene-batch-validate.md`](./req15-ops-docs-hygiene-batch-validate.md)  
**LAUNCH:** [`req15-ops-docs-hygiene-batch-LAUNCH.md`](./req15-ops-docs-hygiene-batch-LAUNCH.md)  
**MODE:** docs/config-comment only. No runtime code. No secrets in files. [analysis.mdc](../../.cursor/rules/analysis.mdc).

## Todos

- [x] bearer-notes — Add Bearer pairing notes (names only) on both sides runtime/docs
- [x] env-example-primary — Honesty comment on `AIBRIDGE_INTERVIEW_PROVIDER` in `.env.example`
- [x] index-lag — Cascade aibridge README/INDEX Todo→Done where package Done
- [x] openapi-n8n — Relabel aibridge-channel OpenAPI client framing to doge-telegram-channel
- [x] stale-export — Grep/fix remaining export Absent / stitch S5 echoes

## Locks

- Document: telegram `CHANNEL_BEARER` **value** must equal bridge `AIBRIDGE_CHANNEL_BEARER_TOKEN` (names differ).
- Product primary = DeepSeek once enabled; `.env.example` may keep openai as Keep nest **with explicit comment**.
- OpenAPI: target client = `doge-telegram-channel`; n8n = historical optional.

## Touch list (candidates)

- `doge-ai-bridge/.env.example` (comment near `AIBRIDGE_INTERVIEW_PROVIDER` / channel bearer)
- `doge-ai-bridge/docs/requirements/README.md` (56…58 Todo → Done if still stale)
- `doge-ai-bridge/docs/tasks/backlog-stories/INDEX.md` (already partially fixed; verify 62–64 Done)
- `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml` (header/description n8n → telegram-channel)
- `doge-telegram` runtime-docs or `example.env` comment for Bearer pairing
- Grep fix: stale «export Absent» / stitch S5 in analysis/REQ docs if still present

## OOS

- Editing live `.env` secrets; starting services; V1 code; STORY implement; Railway.

## Prove

- Grep shows no contradictory «56 Todo» / «62 Todo» where package INDEX Done.
- OpenAPI mentions `doge-telegram-channel`.
- `.env.example` documents DeepSeek-primary product lock vs nest default.
