"""Aggressive refining strategy for maximum token reduction."""

from typing import Literal

from ..cleaner import NormalizeWhitespace, StripHTML
from ..compressor import Deduplicate
from ..pipeline import Pipeline


class AggressiveStrategy(Pipeline):
    """
    Aggressive strategy: Maximum token reduction through aggressive deduplication.

    This strategy is itself a Pipeline, so you can use it directly or extend it.

    Refiners:
    - StripHTML: Remove HTML tags (optional)
    - NormalizeWhitespace: Collapse excessive whitespace
    - Deduplicate: Aggressively remove similar content (threshold: 0.7)

    Characteristics:
    - Token reduction: ~5-10% (higher with duplicate content)
    - Quality: 96-98% (cosine similarity)
    - Use case: Cost optimization with duplicate/redundant content
    - Latency: 0.25ms per 1k tokens

    Note: For token budget control, use Packer's max_tokens parameter instead.

    Example:
        >>> # Use with defaults
        >>> strategy = AggressiveStrategy()
        >>> cleaned = strategy.run(text)
        >>>
        >>> # Customize operator parameters
        >>> strategy = AggressiveStrategy(
        ...     strip_html_to_markdown=True,
        ...     deduplicate_method="levenshtein",
        ...     deduplicate_similarity_threshold=0.6,
        ...     deduplicate_granularity="paragraph"
        ... )
        >>> cleaned = strategy.run(text)
        >>>
        >>> # Extend with additional operators
        >>> extended = AggressiveStrategy().pipe(RedactPII())
        >>> cleaned = extended.run(text)
    """

    def __init__(
        self,
        # Parameters to configure StripHTML operator
        strip_html: bool = True,
        strip_html_to_markdown: bool = False,
        # Parameters to configure Deduplicate operator
        deduplicate_method: Literal["jaccard", "levenshtein"] = "jaccard",
        deduplicate_similarity_threshold: float = 0.7,
        deduplicate_granularity: Literal["sentence", "paragraph"] = "sentence",
    ):
        """
        Initialize aggressive strategy with configured operators.

        Args:
            strip_html: Whether to include StripHTML operator (default: True)
            strip_html_to_markdown: Convert HTML to Markdown instead of stripping (default: False)
            deduplicate_method: Deduplication method (default: "jaccard")
            deduplicate_similarity_threshold: Similarity threshold for aggressive deduplication
                (default: 0.7)
            deduplicate_granularity: Deduplication granularity (default: "sentence")
        """
        operations = []

        if strip_html:
            operations.append(StripHTML(to_markdown=strip_html_to_markdown))

        operations.append(NormalizeWhitespace())

        operations.append(
            Deduplicate(
                method=deduplicate_method,
                similarity_threshold=deduplicate_similarity_threshold,
                granularity=deduplicate_granularity,
            )
        )

        # Initialize Pipeline with the configured operators
        super().__init__(operations)
