"""Poster / storage failure classes (arch DP9). Wire strings = implement choice."""

from __future__ import annotations

from enum import Enum


class PosterFailureClass(str, Enum):
    """Logical classes — values are implement wire strings for this wave."""

    IMAGE_GENERATION_FAILED = "image_generation_failed"
    STORAGE_UPLOAD_FAILED = "storage_upload_failed"


class PosterFailure(Exception):
    def __init__(self, failure_class: PosterFailureClass, message: str = "") -> None:
        self.failure_class = failure_class
        self.message = message or failure_class.value
        super().__init__(self.message)
