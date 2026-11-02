-- Semantic interview state — separate from conversation_history / confirm_session.
-- DDL implement choice for STORY-62 (REQ-13 Open); not a hash-format SSOT.
BEGIN;

CREATE TABLE IF NOT EXISTS semantic_state (
  session_id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;
