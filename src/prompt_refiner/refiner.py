"""Main Refiner class for building prompt processing pipelines."""

from typing import List

from .operation import Operation


class Refiner:
    """A pipeline builder for prompt refining operations."""

    def __init__(self):
        """Initialize an empty refiner pipeline."""
        self._operations: List[Operation] = []

    def pipe(self, operation: Operation) -> "Refiner":
        """
        Add an operation to the pipeline.

        Returns a new Refiner instance with the operation added, leaving the
        original unchanged (immutable).

        Args:
            operation: The operation to add

        Returns:
            A new Refiner instance with the operation added

        Example:
            >>> base = Refiner().pipe(StripHTML())
            >>> pipeline1 = base.pipe(NormalizeWhitespace())
            >>> pipeline2 = base.pipe(TruncateTokens(100))
            >>> # base still has 1 operation, pipeline1 and pipeline2 each have 2
        """
        new_refiner = Refiner()
        new_refiner._operations = self._operations.copy()
        new_refiner._operations.append(operation)
        return new_refiner

    def run(self, text: str) -> str:
        """
        Execute the pipeline on the input text.

        Args:
            text: The input text to process

        Returns:
            The processed text after all operations
        """
        result = text
        for operation in self._operations:
            result = operation.process(result)
        return result

    def __or__(self, other: Operation) -> "Refiner":
        """
        Support pipe operator syntax for adding operations to the pipeline.

        Returns a new Refiner instance, leaving the original unchanged (immutable).
        Enables continued chaining: (op1 | op2) | op3

        Args:
            other: The operation to add to the pipeline

        Returns:
            A new Refiner instance with the operation added

        Example:
            >>> from prompt_refiner import StripHTML, NormalizeWhitespace, TruncateTokens
            >>> base = StripHTML() | NormalizeWhitespace()
            >>> pipeline1 = base | TruncateTokens(max_tokens=100)
            >>> pipeline2 = base | TruncateTokens(max_tokens=200)
            >>> # base has 2 ops, pipeline1 and pipeline2 each have 3 different ops
        """
        return self.pipe(other)
