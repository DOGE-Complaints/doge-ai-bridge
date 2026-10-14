"""Bind / DP9 failure classes (arch). Wire strings = implement choice (Open in arch)."""

from __future__ import annotations

from enum import Enum


class BindFailureClass(str, Enum):
    """Logical DP9 classes used on fail-bind path (implement wire values)."""

    ACCEPT_UNAUTHORIZED = "accept_unauthorized"
    CORPUS_INSUFFICIENT = "corpus_insufficient"
    BRIEF_GENERATION_FAILED = "brief_generation_failed"
    IMAGE_GENERATION_FAILED = "image_generation_failed"
    STORAGE_UPLOAD_FAILED = "storage_upload_failed"
    BIND_REJECTED = "bind_rejected"
    INTERNAL_ERROR = "internal_error"


class BindFailure(Exception):
    def __init__(self, failure_class: BindFailureClass, message: str = "") -> None:
        self.failure_class = failure_class
        self.message = message or failure_class.value
        super().__init__(self.message)
