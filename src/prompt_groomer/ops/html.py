"""HTML stripping operation."""

import re

from ..operation import Operation


class StripHTML(Operation):
    """Remove HTML tags from text."""

    def process(self, text: str) -> str:
        """
        Remove HTML tags from the input text.

        Args:
            text: The input text containing HTML

        Returns:
            Text with HTML tags removed
        """
        # Simple regex to strip HTML tags
        return re.sub(r"<[^>]+>", "", text)
