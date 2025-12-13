"""Base class for refining strategies."""

from abc import ABC, abstractmethod

from ..refiner import Refiner


class BaseStrategy(ABC):
    """Abstract base class for all refining strategies."""

    @abstractmethod
    def get_operations(self) -> list:
        """
        Get the list of operations for this strategy.

        Returns:
            List of Operation instances to be applied in sequence
        """
        pass

    def create_refiner(self) -> Refiner:
        """
        Create a Refiner instance with this strategy's operations.

        Returns:
            Configured Refiner instance
        """
        refiner = Refiner()
        for operation in self.get_operations():
            refiner = refiner.pipe(operation)  # Capture new instance (immutable)
        return refiner

    def __call__(self, text: str) -> str:
        """
        Apply strategy directly to text (convenience method).

        Args:
            text: Input text to process

        Returns:
            Processed text
        """
        return self.create_refiner().run(text)
