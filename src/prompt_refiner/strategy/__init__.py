"""Preset refining strategies for common use cases."""

from .aggressive import AggressiveStrategy
from .base import BaseStrategy
from .minimal import MinimalStrategy
from .standard import StandardStrategy

__all__ = [
    # Base class
    "BaseStrategy",
    # Preset classes
    "MinimalStrategy",
    "StandardStrategy",
    "AggressiveStrategy",
]
