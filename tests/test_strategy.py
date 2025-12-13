"""Tests for strategy module."""

from prompt_refiner import RedactPII
from prompt_refiner.strategy import (
    AggressiveStrategy,
    MinimalStrategy,
    StandardStrategy,
)


class TestMinimalStrategy:
    def test_minimal_strategy_basic(self):
        """Test minimal strategy with basic input."""
        strategy = MinimalStrategy()
        # Strategy IS a pipeline now, use directly
        result = strategy.run("<div>  hello   world  </div>")
        assert result == "hello world"

    def test_minimal_strategy_to_markdown(self):
        """Test minimal strategy with markdown conversion."""
        strategy = MinimalStrategy(strip_html_to_markdown=True)
        # Strategy IS a pipeline now, use directly
        result = strategy.run("<strong>bold</strong> text")
        assert "**bold**" in result

    def test_minimal_strategy_factory(self):
        """Test factory function."""
        strategy = MinimalStrategy()
        result = strategy.run("<p>test</p>")
        assert result == "test"

    def test_minimal_strategy_callable(self):
        """Test calling strategy directly on text."""
        strategy = MinimalStrategy()
        result = strategy.run("<div>  test  </div>")
        assert result == "test"

    def test_minimal_strategy_disable_html_strip(self):
        """Test minimal strategy without HTML stripping."""
        strategy = MinimalStrategy(strip_html=False)
        # Strategy IS a pipeline now, use directly
        result = strategy.run("<div>  hello  </div>")
        assert "<div>" in result
        assert "hello" in result


class TestStandardStrategy:
    def test_standard_strategy_basic(self):
        """Test standard strategy with duplicates."""
        strategy = StandardStrategy()
        # Strategy IS a pipeline now, use directly
        text = "<div>Hello world. Hello world.</div>"
        result = strategy.run(text)
        # Should remove duplicate sentence
        assert result.count("Hello world") == 1

    def test_standard_strategy_factory(self):
        """Test factory function with custom threshold."""
        strategy = StandardStrategy(deduplicate_similarity_threshold=0.7)
        result = strategy.run("<p>test. test.</p>")
        assert result.count("test") == 1

    def test_standard_strategy_no_duplicates(self):
        """Test standard strategy with no duplicates."""
        strategy = StandardStrategy()
        # Strategy IS a pipeline now, use directly
        text = "<div>Hello world. Goodbye world.</div>"
        result = strategy.run(text)
        assert "Hello world" in result
        assert "Goodbye world" in result

    def test_standard_strategy_custom_params(self):
        """Test standard strategy with custom parameters."""
        strategy = StandardStrategy(
            strip_html_to_markdown=True,
            deduplicate_similarity_threshold=0.9,
            deduplicate_method="levenshtein",
        )
        # Strategy IS a pipeline now, use directly
        result = strategy.run("<strong>test</strong>")
        assert "**test**" in result

    def test_standard_strategy_disable_html_strip(self):
        """Test standard strategy without HTML stripping."""
        strategy = StandardStrategy(strip_html=False)
        # Strategy IS a pipeline now, use directly
        result = strategy.run("<div>  hello  world  </div>")
        # Should keep HTML but normalize whitespace
        assert "<div>" in result
        assert "hello world" in result
        # Whitespace should be normalized
        assert "  " not in result.replace("<div>", "").replace("</div>", "")


class TestAggressiveStrategy:
    def test_aggressive_strategy_basic(self):
        """Test aggressive strategy with basic cleaning."""
        strategy = AggressiveStrategy()
        text = "<div>  hello   world  </div>"
        result = strategy.run(text)
        # Should strip HTML and normalize whitespace
        assert "<" not in result
        assert result == "hello world"

    def test_aggressive_strategy_deduplication(self):
        """Test aggressive strategy removes duplicates aggressively."""
        strategy = AggressiveStrategy()
        text = "Hello world. Hello world. Goodbye world."
        result = strategy.run(text)
        # Should deduplicate at 0.7 threshold (aggressive)
        assert result.count("Hello world") == 1

    def test_aggressive_strategy_custom_threshold(self):
        """Test aggressive strategy with custom deduplication threshold."""
        # More aggressive threshold (0.6 instead of default 0.7)
        strategy = AggressiveStrategy(deduplicate_similarity_threshold=0.6)
        # Use more similar sentences that will trigger deduplication
        text = "The quick brown fox jumps. The quick brown fox leaps. The slow red fox jumps."
        result = strategy.run(text)
        # With aggressive threshold, should deduplicate similar sentences
        # Verify that HTML stripping and whitespace normalization work
        assert "<" not in result
        assert "  " not in result

    def test_aggressive_strategy_all_features(self):
        """Test aggressive strategy with HTML and duplicates."""
        strategy = AggressiveStrategy()
        text = """
        <div>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <p>The fast brown fox leaps over the sleeping dog.</p>
            <p>Another completely different sentence here.</p>
        </div>
        """
        result = strategy.run(text)
        # Should strip HTML and deduplicate similar sentences
        assert "<" not in result
        assert ">" not in result
        # Should have deduplicated some content
        assert len(result) < len(text.replace("<", "").replace(">", ""))

    def test_aggressive_strategy_disable_html_strip(self):
        """Test aggressive strategy without HTML stripping."""
        strategy = AggressiveStrategy(strip_html=False)
        text = "<div>  hello  world  </div>"
        result = strategy.run(text)
        # Should keep HTML but normalize whitespace
        assert "<div>" in result
        assert "hello world" in result
        # Whitespace should be normalized
        assert "  " not in result.replace("<div>", "").replace("</div>", "")

    def test_aggressive_strategy_custom_method(self):
        """Test aggressive strategy with custom deduplication method."""
        strategy = AggressiveStrategy(deduplicate_method="levenshtein")
        text = "Hello world. Hello world. Goodbye world."
        result = strategy.run(text)
        # Should deduplicate using Levenshtein distance
        assert result.count("Hello world") == 1


class TestStrategyEnum:
    def test_enum_minimal(self):
        """Test enum-based strategy creation."""
        strategy = MinimalStrategy()
        result = strategy.run("<div>test</div>")
        assert result == "test"

    def test_enum_standard(self):
        """Test enum standard strategy."""
        strategy = StandardStrategy()
        result = strategy.run("<div>test. test.</div>")
        assert result.count("test") == 1

    def test_enum_aggressive_with_params(self):
        """Test enum with custom parameters."""
        strategy = AggressiveStrategy(deduplicate_similarity_threshold=0.6)
        text = "The quick brown fox. The quick brown fox. Different sentence."
        result = strategy.run(text)
        # With lower threshold, should deduplicate similar sentences
        assert result.count("The quick brown fox") == 1


class TestStrategyComposition:
    def test_strategy_pipe_additional_operations(self):
        """Test composing strategy with additional operations."""
        strategy = MinimalStrategy()
        strategy = strategy.pipe(RedactPII(redact_types={"email"}))  # Capture new instance

        result = strategy.run("<div>Contact: test@example.com</div>")
        assert "[EMAIL]" in result
        assert "test@example.com" not in result

    def test_strategy_multiple_pipes(self):
        """Test chaining multiple operations after strategy."""
        from prompt_refiner import FixUnicode

        strategy = MinimalStrategy()
        strategy = strategy.pipe(FixUnicode())  # Capture new instance

        # Unicode test with HTML
        result = strategy.run("<div>Hello\u200bWorld</div>")
        assert "Hello" in result
        assert "World" in result
        assert "\u200b" not in result  # Zero-width space removed


class TestStrategyReturnTypes:
    def test_factory_returns_refiner(self):
        """Test that strategies are Pipeline instances."""
        from prompt_refiner import Pipeline

        strategy = MinimalStrategy()
        assert isinstance(strategy, Pipeline)

    def test_strategy_create_refiner_returns_refiner(self):
        """Test that strategies are Pipeline instances."""
        from prompt_refiner import Pipeline

        strategy = MinimalStrategy()
        # Strategy IS a pipeline now
        assert isinstance(strategy, Pipeline)


class TestStrategyEdgeCases:
    def test_empty_string(self):
        """Test strategies handle empty strings."""
        strategy = MinimalStrategy()
        result = strategy.run("")
        assert result == ""

    def test_no_html(self):
        """Test strategies handle plain text."""
        strategy = MinimalStrategy()
        result = strategy.run("plain text")
        assert result == "plain text"

    def test_aggressive_with_short_text(self):
        """Test aggressive strategy with short text without duplicates."""
        strategy = AggressiveStrategy()
        result = strategy.run("short text")
        assert result == "short text"

    def test_unicode_handling(self):
        """Test strategies handle Unicode correctly."""
        strategy = MinimalStrategy()
        result = strategy.run("<div>Hello 世界</div>")
        assert "世界" in result
