"""REQ-13 roles / coordinator policy / assembly (STORY-63). OOS 62 DDL / 64 live."""

from aibridge.roles.assembly import (
    AssembledRolePrompt,
    assemble_role_prompt,
    assert_manifest_covers_v1,
    load_roles_manifest,
    session_pin_hex,
)
from aibridge.roles.invoke import bind_role_interview_engine
from aibridge.roles.policy import (
    DEFAULT_POLICY_ROWS,
    PolicyRow,
    PolicySelectionError,
    select_next_role,
)
from aibridge.roles.registry import (
    DEFAULT_ROLE_REGISTRY,
    DEFAULT_ROLE_VERSION,
    V1_ROLE_IDS,
    RoleRegistry,
    RoleSpec,
)

__all__ = [
    "AssembledRolePrompt",
    "DEFAULT_POLICY_ROWS",
    "DEFAULT_ROLE_REGISTRY",
    "DEFAULT_ROLE_VERSION",
    "PolicyRow",
    "PolicySelectionError",
    "RoleRegistry",
    "RoleSpec",
    "V1_ROLE_IDS",
    "assemble_role_prompt",
    "assert_manifest_covers_v1",
    "bind_role_interview_engine",
    "load_roles_manifest",
    "select_next_role",
    "session_pin_hex",
]
