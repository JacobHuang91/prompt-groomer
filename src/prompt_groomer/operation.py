"""Base operation class for prompt processing."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .groomer import Groomer


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

    def __or__(self, other: "Operation") -> "Groomer":
        """
        Support pipe operator syntax for composing operations.

        Enables LangChain-style pipeline composition: op1 | op2 | op3

        Args:
            other: The operation to chain with this operation

        Returns:
            A Groomer pipeline containing both operations

        Example:
            >>> from prompt_groomer import StripHTML, NormalizeWhitespace
            >>> pipeline = StripHTML() | NormalizeWhitespace()
            >>> result = pipeline.run("<div>  hello  </div>")
            >>> # Returns: "hello"
        """
        from .groomer import Groomer

        return Groomer().pipe(self).pipe(other)
