# AC-AIB-12-04 — interview stub + live evidence gates (STORY-61 / REQ-12)

Thin runtime note. Arch SSOT: [`../architecture/req15-interview-providers/03-verify-evidence-coexistence.md`](../architecture/req15-interview-providers/03-verify-evidence-coexistence.md). Port/env: [`07-interview-provider-port-env.md`](./07-interview-provider-port-env.md).

**Honesty:** stub harness ≠ AC-AIB-12-04 **live Done**. Live Pass **per provider** only with ops evidence window + recorded path. This wave: live = **Explicit Partial** (both `deepseek` and `openai`). Do **not** invent Railway / live SUCCESS.

---

## 1) Stub evidence matrix (required · tech accept)

Runnable harness (Present):

- `tests/test_story_59_interview_port_env_fail_closed.py` (port/env · AC-01/02/05 · D4)
- `tests/test_story_60_openai_deepseek_interview_adapters.py` (adapters · AC-03)

| AC | Meaning | Stub harness (pytest) | Status |
|----|---------|----------------------|--------|
| **AC-AIB-12-01** | Config selects `deepseek` \| `openai` | `test_ac_12_01_settings_loads_interview_provider` · `test_openai_port_slot` | Present |
| **AC-AIB-12-02** | Worker env cannot select interview | `test_ac_12_02_worker_env_cannot_select_interview` · `test_port_home_not_under_providers` | Present |
| **AC-AIB-12-03** | Both adapters usable under harness | `test_t01_openai_adapter_keep_production_responses_client` · `test_t02_deepseek_adapter_chat_completions_l12_3` · `test_t08_story_gate_both_adapters_harness` | Present |
| **AC-AIB-12-05** | Unset/unknown/incomplete fail-closed | `test_ac_12_05_unset_empty_unknown_fail_closed` · `test_l12_3_openai_nest_incomplete` · `test_l12_3_deepseek_nest_required` · `test_d4_wire_fail_closed_no_recording_fallback` | Present |
| Soft §4.3 | No silent OpenAI when deepseek | `test_t04_no_silent_openai_when_deepseek` | Present (60) |

Command (from `doge-ai-bridge/`):

```bash
.venv/bin/python -m pytest tests/test_story_59_interview_port_env_fail_closed.py tests/test_story_60_openai_deepseek_interview_adapters.py -q
```

No claim of live vendor HTTP / Railway Pass from this matrix.

---

## 2) Live Pass runbook / checklist (per provider)

### Providers

| Provider id | Nest (L12-3) | Live Pass claim |
|-------------|--------------|-----------------|
| `deepseek` | `AIBRIDGE_INTERVIEW_DEEPSEEK_*` + selector | Only with ops window + recorded path |
| `openai` | `OPENAI_API_KEY` + `OPENAI_MODEL` + selector | Only with ops window + recorded path |

### Path (when ops window open)

`Channel Bearer → doge-ai-bridge interview wire → selected adapter → Engine turn`  
(≥1 recorded path **per provider** required to claim **live Pass / AC-AIB-12-04 Done** for that provider.)

### Checklist (ops · each provider)

| Step | Fact to record | Blocker if missing |
|------|----------------|--------------------|
| 1 | Ops evidence window calendar/env **open** for that provider | Without window → stay **Partial** |
| 2 | Real nest keys filled (`.env.example` §4b) — never invent secrets in docs | Incomplete nest → fail-closed (not live Pass) |
| 3 | `AIBRIDGE_INTERVIEW_PROVIDER` = target id | Wrong id → wrong adapter |
| 4 | Live turn succeeds via selected adapter (DeepSeek Completions or OpenAI Responses) | Transport fail → not live Pass |
| 5 | Evidence artifact path + UTC recorded in analysis/run-report | Absent record → cannot claim Done |
| 6 | L12-2 DeepSeek model confirm before deepseek live Pass | Unconfirmed model → residual |

### Wave status (STORY-61 / this implement)

| Field | Value |
|-------|-------|
| Ops evidence window | **Not open** (mandatory live not required this wave) |
| Live E2E evidence (`deepseek`) | **Unknown** / not claimed Done |
| Live E2E evidence (`openai`) | **Unknown** / not claimed Done |
| AC-AIB-12-04 live side | **Explicit Partial** (both providers) |
| Invented Railway / live SUCCESS | **Forbidden · Absent** |

---

## 3) Peer coexistence cites (no invent APIs)

| Peer | Cite | Stance |
|------|------|--------|
| Worker REQ-10 arch | [`../architecture/ai-provider-selection/00-overview.md`](../architecture/ai-provider-selection/00-overview.md) | Worker only; interview OOS |
| REQ-11 confirm Keep | [`../architecture/req15-dual-confirm-handoff/00-overview.md`](../architecture/req15-dual-confirm-handoff/00-overview.md) · [`04-confirm-gateway-keep-pipe.md`](./04-confirm-gateway-keep-pipe.md) | Provider change ≠ Send permission |
| REQ-13 | [`../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md`](../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) | Roles call interview port when Present |
| GPT UI REQ-48 | [`../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md`](../../../GPT%20UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md) | Instruction SSOT OOS |
| telegram / gateway | no model keys on channel/gateway path | Trust channel Bearer ≠ vendor keys |

---

## 4) Out of this note

Port/env invent (59 Done) · adapter bodies invent (60 Done) · opening ops window · worker live matrix body · gateway/SPA redesign · invent Railway SUCCESS.
