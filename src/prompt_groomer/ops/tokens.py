"""Token truncation operation."""

from typing import Literal

from ..operation import Operation


class TruncateTokens(Operation):
    """Truncate text to a maximum number of tokens."""

    def __init__(
        self,
        max_tokens: int,
        strategy: Literal["start", "end", "middle"] = "end",
    ):
        """
        Initialize the truncation operation.

        Args:
            max_tokens: Maximum number of tokens to keep
            strategy: Where to truncate - "start" (keep end), "end" (keep start),
                     or "middle" (keep start and end)
        """
        self.max_tokens = max_tokens
        self.strategy = strategy

    def process(self, text: str) -> str:
        """
        Truncate text to max_tokens.

        Note: Currently uses simple word-based approximation.
        Will be improved with actual tokenization later.

        Args:
            text: The input text

        Returns:
            Truncated text
        """
        words = text.split()

        # Simple approximation: ~1 token per word
        if len(words) <= self.max_tokens:
            return text

        if self.strategy == "end":
            # Keep the start
            return " ".join(words[: self.max_tokens])

        elif self.strategy == "start":
            # Keep the end
            return " ".join(words[-self.max_tokens :])

        elif self.strategy == "middle":
            # Keep start and end, truncate middle
            half = self.max_tokens // 2
            start_words = words[:half]
            end_words = words[-(self.max_tokens - half) :]
            return " ".join(start_words) + " ... " + " ".join(end_words)

        return text
