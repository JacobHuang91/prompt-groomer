"""Main Groomer class for building prompt processing pipelines."""

from typing import List

from .operation import Operation


class Groomer:
    """A pipeline builder for prompt grooming operations."""

    def __init__(self):
        """Initialize an empty groomer pipeline."""
        self._operations: List[Operation] = []

    def pipe(self, operation: Operation) -> "Groomer":
        """
        Add an operation to the pipeline.

        Args:
            operation: The operation to add

        Returns:
            Self for method chaining
        """
        self._operations.append(operation)
        return self

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
