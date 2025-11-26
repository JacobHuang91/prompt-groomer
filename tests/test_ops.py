"""Tests for individual operations."""

from prompt_groomer.ops import NormalizeWhitespace, StripHTML, TruncateTokens


def test_strip_html_basic():
    """Test basic HTML stripping."""
    op = StripHTML()
    assert op.process("<div>hello</div>") == "hello"
    assert op.process("<b>bold</b> text") == "bold text"


def test_strip_html_nested():
    """Test nested HTML stripping."""
    op = StripHTML()
    assert op.process("<div><span>nested</span></div>") == "nested"


def test_normalize_whitespace():
    """Test whitespace normalization."""
    op = NormalizeWhitespace()
    assert op.process("hello   world") == "hello world"
    assert op.process("  spaces  ") == "spaces"
    assert op.process("line\n\nbreaks") == "line breaks"


def test_truncate_tokens_end():
    """Test truncation keeping the start."""
    op = TruncateTokens(max_tokens=3, strategy="end")
    result = op.process("one two three four five")
    assert result == "one two three"


def test_truncate_tokens_start():
    """Test truncation keeping the end."""
    op = TruncateTokens(max_tokens=3, strategy="start")
    result = op.process("one two three four five")
    assert result == "three four five"


def test_truncate_tokens_middle():
    """Test truncation keeping start and end."""
    op = TruncateTokens(max_tokens=4, strategy="middle")
    result = op.process("one two three four five six")
    assert "one two" in result
    assert "five six" in result
    assert "..." in result


def test_truncate_tokens_no_truncation():
    """Test that short text is not truncated."""
    op = TruncateTokens(max_tokens=10, strategy="end")
    result = op.process("short text")
    assert result == "short text"
