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
        refiner = strategy.create_refiner()
        result = refiner.run("<div>  hello   world  </div>")
        assert result == "hello world"

    def test_minimal_strategy_to_markdown(self):
        """Test minimal strategy with markdown conversion."""
        strategy = MinimalStrategy(to_markdown=True)
        refiner = strategy.create_refiner()
        result = refiner.run("<strong>bold</strong> text")
        assert "**bold**" in result

    def test_minimal_strategy_factory(self):
        """Test factory function."""
        refiner = MinimalStrategy().create_refiner()
        result = refiner.run("<p>test</p>")
        assert result == "test"

    def test_minimal_strategy_callable(self):
        """Test calling strategy directly on text."""
        strategy = MinimalStrategy()
        result = strategy("<div>  test  </div>")
        assert result == "test"

    def test_minimal_strategy_disable_html_strip(self):
        """Test minimal strategy without HTML stripping."""
        strategy = MinimalStrategy(strip_html=False)
        refiner = strategy.create_refiner()
        result = refiner.run("<div>  hello  </div>")
        assert "<div>" in result
        assert "hello" in result


class TestStandardStrategy:
    def test_standard_strategy_basic(self):
        """Test standard strategy with duplicates."""
        strategy = StandardStrategy()
        refiner = strategy.create_refiner()
        text = "<div>Hello world. Hello world.</div>"
        result = refiner.run(text)
        # Should remove duplicate sentence
        assert result.count("Hello world") == 1

    def test_standard_strategy_factory(self):
        """Test factory function with custom threshold."""
        refiner = StandardStrategy(similarity_threshold=0.7).create_refiner()
        result = refiner.run("<p>test. test.</p>")
        assert result.count("test") == 1

    def test_standard_strategy_no_duplicates(self):
        """Test standard strategy with no duplicates."""
        strategy = StandardStrategy()
        refiner = strategy.create_refiner()
        text = "<div>Hello world. Goodbye world.</div>"
        result = refiner.run(text)
        assert "Hello world" in result
        assert "Goodbye world" in result

    def test_standard_strategy_custom_params(self):
        """Test standard strategy with custom parameters."""
        strategy = StandardStrategy(
            to_markdown=True, similarity_threshold=0.9, dedup_method="levenshtein"
        )
        refiner = strategy.create_refiner()
        result = refiner.run("<strong>test</strong>")
        assert "**test**" in result

    def test_standard_strategy_disable_html_strip(self):
        """Test standard strategy without HTML stripping."""
        strategy = StandardStrategy(strip_html=False)
        refiner = strategy.create_refiner()
        result = refiner.run("<div>  hello  world  </div>")
        # Should keep HTML but normalize whitespace
        assert "<div>" in result
        assert "hello world" in result
        # Whitespace should be normalized
        assert "  " not in result.replace("<div>", "").replace("</div>", "")


class TestAggressiveStrategy:
    def test_aggressive_strategy_truncation(self):
        """Test aggressive strategy truncates long text."""
        strategy = AggressiveStrategy(max_tokens=5)
        refiner = strategy.create_refiner()
        text = "word " * 20  # 20 words
        result = refiner.run(text)
        # Should truncate to ~5 words (allowing small buffer for estimation)
        assert len(result.split()) <= 7

    def test_aggressive_strategy_factory(self):
        """Test factory function with custom max_tokens."""
        refiner = AggressiveStrategy(max_tokens=10).create_refiner()
        text = "word " * 100
        result = refiner.run(text)
        assert len(result.split()) <= 12  # Allow small buffer

    def test_aggressive_strategy_tail(self):
        """Test aggressive strategy with tail truncation."""
        strategy = AggressiveStrategy(max_tokens=5, truncate_strategy="tail")
        refiner = strategy.create_refiner()
        text = "first second third fourth fifth sixth seventh eighth"
        result = refiner.run(text)
        # Should keep last ~5 words
        assert "eighth" in result

    def test_aggressive_strategy_deduplication(self):
        """Test aggressive strategy removes duplicates."""
        strategy = AggressiveStrategy(max_tokens=100)
        refiner = strategy.create_refiner()
        text = "Hello world. Hello world. Goodbye world."
        result = refiner.run(text)
        # Should deduplicate at 0.7 threshold
        assert result.count("Hello world") == 1

    def test_aggressive_strategy_all_features(self):
        """Test aggressive strategy with HTML, duplicates, and truncation."""
        strategy = AggressiveStrategy(max_tokens=10)
        refiner = strategy.create_refiner()
        text = """
        <div>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <p>The fast brown fox leaps over the sleeping dog.</p>
            <p>Another completely different sentence here.</p>
        </div>
        """
        result = refiner.run(text)
        # Should strip HTML, deduplicate, and truncate
        assert "<" not in result
        assert ">" not in result
        assert len(result.split()) <= 12  # Allow small buffer

    def test_aggressive_strategy_disable_html_strip(self):
        """Test aggressive strategy without HTML stripping."""
        strategy = AggressiveStrategy(max_tokens=100, strip_html=False)
        refiner = strategy.create_refiner()
        text = "<div>  hello  world  </div>"
        result = refiner.run(text)
        # Should keep HTML but normalize whitespace and truncate
        assert "<div>" in result
        assert "hello world" in result
        # Whitespace should be normalized
        assert "  " not in result.replace("<div>", "").replace("</div>", "")


class TestStrategyEnum:
    def test_enum_minimal(self):
        """Test enum-based strategy creation."""
        refiner = MinimalStrategy().create_refiner()
        result = refiner.run("<div>test</div>")
        assert result == "test"

    def test_enum_standard(self):
        """Test enum standard strategy."""
        refiner = StandardStrategy().create_refiner()
        result = refiner.run("<div>test. test.</div>")
        assert result.count("test") == 1

    def test_enum_aggressive_with_params(self):
        """Test enum with custom parameters."""
        refiner = AggressiveStrategy(max_tokens=10).create_refiner()
        text = "word " * 50
        result = refiner.run(text)
        assert len(result.split()) <= 12


class TestStrategyComposition:
    def test_strategy_pipe_additional_operations(self):
        """Test composing strategy with additional operations."""
        refiner = MinimalStrategy().create_refiner()
        refiner.pipe(RedactPII(redact_types={"email"}))

        result = refiner.run("<div>Contact: test@example.com</div>")
        assert "[EMAIL]" in result
        assert "test@example.com" not in result

    def test_strategy_multiple_pipes(self):
        """Test chaining multiple operations after strategy."""
        from prompt_refiner import FixUnicode

        refiner = MinimalStrategy().create_refiner()
        refiner.pipe(FixUnicode())

        # Unicode test with HTML
        result = refiner.run("<div>Hello\u200bWorld</div>")
        assert "Hello" in result
        assert "World" in result
        assert "\u200b" not in result  # Zero-width space removed


class TestStrategyReturnTypes:
    def test_factory_returns_refiner(self):
        """Test that factory functions return Refiner instances."""
        from prompt_refiner import Refiner

        refiner = MinimalStrategy().create_refiner()
        assert isinstance(refiner, Refiner)

    def test_strategy_create_refiner_returns_refiner(self):
        """Test that create_refiner returns Refiner instances."""
        from prompt_refiner import Refiner

        strategy = MinimalStrategy()
        refiner = strategy.create_refiner()
        assert isinstance(refiner, Refiner)


class TestStrategyEdgeCases:
    def test_empty_string(self):
        """Test strategies handle empty strings."""
        strategy = MinimalStrategy()
        result = strategy("")
        assert result == ""

    def test_no_html(self):
        """Test strategies handle plain text."""
        strategy = MinimalStrategy()
        result = strategy("plain text")
        assert result == "plain text"

    def test_aggressive_with_short_text(self):
        """Test aggressive strategy with text shorter than max_tokens."""
        strategy = AggressiveStrategy(max_tokens=100)
        result = strategy("short text")
        assert result == "short text"

    def test_unicode_handling(self):
        """Test strategies handle Unicode correctly."""
        strategy = MinimalStrategy()
        result = strategy("<div>Hello 世界</div>")
        assert "世界" in result
