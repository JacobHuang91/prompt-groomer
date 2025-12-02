"""Standard refining strategy with deduplication."""

from typing import List, Literal

from ..cleaner import NormalizeWhitespace, StripHTML
from ..compressor import Deduplicate
from ..operation import Operation
from .base import BaseStrategy


class StandardStrategy(BaseStrategy):
    """
    Standard strategy: Cleaning plus deduplication.

    Operations:
    - StripHTML: Remove HTML tags
    - NormalizeWhitespace: Collapse excessive whitespace
    - Deduplicate: Remove similar content (sentence-level, 0.8 threshold)

    Characteristics:
    - Token reduction: ~4.8%
    - Quality: 98.4% (cosine similarity)
    - Use case: RAG contexts with potential duplicates
    - Latency: 0.25ms per 1k tokens
    """

    def __init__(
        self,
        strip_html: bool = True,
        to_markdown: bool = False,
        similarity_threshold: float = 0.8,
        dedup_method: Literal["jaccard", "levenshtein"] = "jaccard",
    ):
        """
        Initialize standard strategy.

        Args:
            strip_html: Whether to strip HTML tags (default: True)
            to_markdown: Convert HTML to Markdown instead of stripping (default: False)
            similarity_threshold: Threshold for deduplication (default: 0.8)
            dedup_method: Deduplication method: "jaccard" or "levenshtein" (default: "jaccard")
        """
        self.strip_html = strip_html
        self.to_markdown = to_markdown
        self.similarity_threshold = similarity_threshold
        self.dedup_method = dedup_method

    def get_operations(self) -> List[Operation]:
        """Get operations for standard strategy."""
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
        return operations
