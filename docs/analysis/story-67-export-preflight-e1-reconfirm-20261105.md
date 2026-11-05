# STORY-67 t01 — Export preflight reconfirm (GPT E1)

**UTC:** 2026-11-05T12:02:38Z  
**Peer evidence:** `GPT UI/docs/analysis/req-48-export-parity-evidence.md` (as-of 2026-11-02T14:39:55Z)  
**Hash wire:** GPT E1 only (`normalize_text` + `sha256_hex`) — no invent alternate.

## Labels

| Label | Value |
|-------|--------|
| Export Pass claim from this reconfirm | **Explicit Block** |
| Honesty | **stale evidence ≠ Export Pass** |
| Consume Pass | **No** — not claimed |
| Invent bodies / alternate hash | **Forbidden · Absent** |

## Path reconfirm

| Path | Fact |
|------|------|
| Evidence sibling `GPT UI/instructions-roles-req15/` | **Absent** |
| Present export tree `GPT UI/instructions-roles/` | **Present** (roles.manifest.json + core + five roles) |
| Path drift | Evidence cites Absent path → **stale** |

## Hash reconfirm (Present tree vs evidence table)

Method: UTF-8 decode → newlines LF → SHA-256 hex (E1 / `content.py`).

| File | Evidence sha256 | Live `instructions-roles/` | Fact |
|------|-----------------|----------------------------|------|
| `roles.manifest.json` | `b92039c3…067c89f` | match | Present |
| `core.md` | `e905700d…cf97d32` | `c67eb95b…` | **DRIFT** |
| `communication_setup.md` | match | match | Present |
| `interviewer.md` | match | match | Present |
| `extractor.md` | match | match | Present |
| `normalizer.md` | match | match | Present |
| `checker.md` | match | match | Present |
| `bundle_version` | `req15-roles-v1` | `req15-roles-v1` | Present |

## Disposition

- **Block** any Export Pass / Consume Pass claim that cites the 2026-11-02 evidence artifact as current.
- Operator must refresh GPT E1 evidence against Present `instructions-roles/` (or restore matching tree) before live AC-05 Pass.
- aibridge adopts E1 **wire semantics** (t02); does **not** invent refreshed GPT hashes as Export Pass.

## Evidence paths

- This file  
- Peer: `GPT UI/docs/analysis/req-48-export-parity-evidence.md`  
- Peer arch: `GPT UI/docs/architecture/req-48-role-oriented-instruction-line/03-publish-verify-parity.md` §E1
