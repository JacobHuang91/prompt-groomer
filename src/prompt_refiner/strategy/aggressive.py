"""Aggressive refining strategy for maximum token reduction."""

from typing import List, Literal

from ..cleaner import NormalizeWhitespace, StripHTML
from ..compressor import Deduplicate, TruncateTokens
from ..operation import Operation
from .base import BaseStrategy


class AggressiveStrategy(BaseStrategy):
    """
    Aggressive strategy: Maximum token reduction with truncation.

    Operations:
    - StripHTML: Remove HTML tags
    - NormalizeWhitespace: Collapse excessive whitespace
    - Deduplicate: Remove similar content (sentence-level, 0.7 threshold)
    - TruncateTokens: Limit to max_tokens (default: 150)

    Characteristics:
    - Token reduction: ~15% (up to 74% on long contexts)
    - Quality: 96.4% (cosine similarity)
    - Use case: Cost optimization, long contexts, lenient quality requirements
    - Latency: 0.25ms per 1k tokens
    """

    def __init__(
        self,
        max_tokens: int = 150,
        strip_html: bool = True,
        to_markdown: bool = False,
        similarity_threshold: float = 0.7,
        dedup_method: Literal["jaccard", "levenshtein"] = "jaccard",
        truncate_strategy: Literal["head", "tail", "middle_out"] = "head",
    ):
        """
        Initialize aggressive strategy.

        Args:
            max_tokens: Maximum tokens to keep (default: 150)
            strip_html: Whether to strip HTML tags (default: True)
            to_markdown: Convert HTML to Markdown instead of stripping (default: False)
            similarity_threshold: Threshold for deduplication (default: 0.7)
            dedup_method: Deduplication method: "jaccard" or "levenshtein" (default: "jaccard")
            truncate_strategy: "head", "tail", or "middle_out" (default: "head")
        """
        self.max_tokens = max_tokens
        self.strip_html = strip_html
        self.to_markdown = to_markdown
        self.similarity_threshold = similarity_threshold
        self.dedup_method = dedup_method
        self.truncate_strategy = truncate_strategy

    def get_operations(self) -> List[Operation]:
        """Get operations for aggressive strategy."""
        operations = []
        if self.strip_html:
            operations.append(StripHTML(to_markdown=self.to_markdown))
        operations.append(NormalizeWhitespace())
        operations.append(
            Deduplicate(
                similarity_threshold=self.similarity_threshold,
                method=self.dedup_method,
                granularity="sentence",
            )
        )
        operations.append(
            TruncateTokens(max_tokens=self.max_tokens, strategy=self.truncate_strategy)
        )
        return operations
