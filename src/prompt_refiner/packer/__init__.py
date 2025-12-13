"""Packer module for prompt composition and optimization."""

from .base import (
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_QUERY,
    PRIORITY_SYSTEM,
    ROLE_ASSISTANT,
    ROLE_CONTEXT,
    ROLE_QUERY,
    ROLE_SYSTEM,
    ROLE_USER,
    BasePacker,
    PackableItem,
    RoleType,
)
from .messages import MessagesPacker
from .text import TextFormat, TextPacker

__all__ = [
    # Packers
    "MessagesPacker",
    "TextPacker",
    "TextFormat",
    "BasePacker",
    "PackableItem",
    # Priority constants (for backward compatibility)
    "PRIORITY_SYSTEM",
    "PRIORITY_QUERY",
    "PRIORITY_HIGH",
    "PRIORITY_MEDIUM",
    "PRIORITY_LOW",
    # Role constants
    "ROLE_SYSTEM",
    "ROLE_QUERY",
    "ROLE_CONTEXT",
    "ROLE_USER",
    "ROLE_ASSISTANT",
    "RoleType",
]
