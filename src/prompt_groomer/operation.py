"""Base operation class for prompt processing."""

from abc import ABC, abstractmethod


class Operation(ABC):
    """Base class for all prompt grooming operations."""

    @abstractmethod
    def process(self, text: str) -> str:
        """
        Process the input text.

        Args:
            text: The input text to process

        Returns:
            The processed text
        """
        pass
