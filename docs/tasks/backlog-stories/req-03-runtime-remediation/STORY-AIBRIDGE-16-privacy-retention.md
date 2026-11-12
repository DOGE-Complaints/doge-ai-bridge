# STORY-AIBRIDGE-16 — Privacy retention enforcement

## Meta
- **Key:** `STORY-AIBRIDGE-16-privacy-retention`
- **Status:** 🟢 Done (P8 · next STORY-17)
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.2 R3-P1-10 · [privacy-pilot.md](../../../runbooks/privacy-pilot.md)
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [14](STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Operator decision:** session-delete = **ops-only**, authenticated, authorized, fail-closed, audit-logged. **HTTP path Unknown** — do **not** invent channel OpenAPI fields; fix path in a later explicit decision / privacy addendum.
- **Active pkg (wave):** `pkg-000014-20260913-epic-aibridge-02-story-16-privacy-retention.yaml`
- **P1 materialize:** 2026-09-13T17:43:00Z
- **P3 Done:** 2026-09-13T17:49:14Z
- **Pipeline:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-16-privacy-retention/STORY-AIBRIDGE-16-privacy-retention.md)

## Scope
- Session/narrative/Responses-item TTL = configured; pilot default **604800** s; slides only on legitimate activity.
- Expired narrative deleted or irreversibly minimized; expired action tokens purged per audit policy.
- Operator session-delete mechanism (ops-only) tested; covers history, pending intents, action tokens.
- Deletion/expiry must **never** make an already consumed action token usable.
- Minimized non-PII replay tombstone may be retained for security/audit window.
- Redacted audit metadata may follow separate retention; n8n execution retention verified separately before residents.

## Вне scope
- Changing channel OpenAPI for delete (forbidden without operator decision).
- Inventing delete URL/method before path is agreed.

## Verified current state
- Privacy runbook + ops-only session-delete CLI (`python -m aibridge.ops_session_delete`); HTTP path still **Unknown**.
- Pilot TTL default **604800**; narrative minimize + consumed-token invariant covered by `tests/test_story_16_privacy_retention.py`.

## Target / AC
- [x] §6.2 bullets proven with tests and/or ops evidence.
- [x] Consumed token remains non-usable after delete/expiry (tombstone OK).
- [x] Delete surface documented as ops-only once path is decided — fail-closed until then.

## Dependencies
- [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [14](STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
