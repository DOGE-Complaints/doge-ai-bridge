-- aibridge SSOT schema — versioned migration 0001
-- Production schema MUST come from migrations, not boot CREATE TABLE IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content_bundle (
  bundle_hash TEXT PRIMARY KEY,
  source_commit TEXT NOT NULL,
  bundle_version TEXT NOT NULL,
  instructions_hash TEXT NOT NULL,
  wire_oas_hash TEXT NOT NULL,
  pack_hash TEXT NOT NULL,
  tool_schema_hash TEXT NOT NULL,
  verified_at TIMESTAMPTZ NOT NULL,
  components_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session (
  session_id TEXT PRIMARY KEY,
  content_bundle_hash TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

-- Unique (channel, event_id); store HTTP status + body for transport replay
CREATE TABLE IF NOT EXISTS event_dedupe (
  channel TEXT NOT NULL,
  event_id TEXT NOT NULL,
  http_status INTEGER NOT NULL,
  response_body JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (channel, event_id)
);

CREATE TABLE IF NOT EXISTS action_token (
  token_hash TEXT PRIMARY KEY,
  action TEXT NOT NULL,
  session_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  chat_id TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  revision INTEGER NOT NULL,
  issued_at DOUBLE PRECISION NOT NULL,
  expires_at DOUBLE PRECISION NOT NULL,
  expected_state TEXT NOT NULL,
  state TEXT NOT NULL,
  operation_id TEXT NOT NULL DEFAULT 'postStoryDraftStash',
  draft_hash TEXT,
  nonce TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS session_call (
  session_id TEXT NOT NULL,
  call_id TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (session_id, call_id)
);

-- At most one gateway attempt per authorized revision
CREATE TABLE IF NOT EXISTS gateway_attempt (
  session_id TEXT NOT NULL,
  revision INTEGER NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  outcome TEXT,
  PRIMARY KEY (session_id, revision)
);

CREATE TABLE IF NOT EXISTS session_turn_lock (
  session_id TEXT PRIMARY KEY,
  holder TEXT NOT NULL,
  acquired_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS conversation_history (
  session_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  item JSONB NOT NULL,
  PRIMARY KEY (session_id, seq)
);

CREATE TABLE IF NOT EXISTS confirm_session (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  chat_id TEXT NOT NULL,
  state_json JSONB NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
