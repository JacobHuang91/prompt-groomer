"""Tests for Refiner pipeline."""

from prompt_refiner import NormalizeWhitespace, Refiner, StripHTML, TruncateTokens


def test_refiner_single_operation():
    """Test refiner with a single operation."""
    refiner = Refiner().pipe(NormalizeWhitespace())

    result = refiner.run("hello   world")
    assert result == "hello world"


def test_refiner_multiple_operations():
    """Test refiner with multiple chained operations."""
    refiner = Refiner().pipe(StripHTML()).pipe(NormalizeWhitespace())

    result = refiner.run("<div>  hello   world  </div>")
    assert result == "hello world"


def test_refiner_full_pipeline():
    """Test the full pipeline from the example."""
    refiner = (
        Refiner()
        .pipe(StripHTML())
        .pipe(NormalizeWhitespace())
        .pipe(TruncateTokens(max_tokens=10, strategy="head"))
    )

    raw_input = "<div>  User input with <b>lots</b> of   spaces... </div>"
    clean_prompt = refiner.run(raw_input)

    # Should strip HTML, normalize whitespace, and keep first 10 words
    assert "<" not in clean_prompt
    assert ">" not in clean_prompt
    assert "  " not in clean_prompt


def test_refiner_empty_pipeline():
    """Test refiner with no operations."""
    refiner = Refiner()

    result = refiner.run("unchanged")
    assert result == "unchanged"


def test_pipe_operator_two_operations():
    """Test pipe operator with two operations."""
    pipeline = StripHTML() | NormalizeWhitespace()

    result = pipeline.run("<div>  hello   world  </div>")
    assert result == "hello world"


def test_pipe_operator_multiple():
    """Test pipe operator with three operations chained."""
    pipeline = StripHTML() | NormalizeWhitespace() | TruncateTokens(max_tokens=3, strategy="head")

    result = pipeline.run("<div>  User input with <b>lots</b> of   spaces... </div>")
    assert result == "User input with"


def test_pipe_operator_full_pipeline():
    """Test pipe operator with realistic full pipeline."""
    pipeline = StripHTML() | NormalizeWhitespace() | TruncateTokens(max_tokens=10, strategy="head")

    raw_input = "<div>  User input with <b>lots</b> of   spaces... </div>"
    clean_prompt = pipeline.run(raw_input)

    # Should strip HTML, normalize whitespace, and keep first 10 words
    assert "<" not in clean_prompt
    assert ">" not in clean_prompt
    assert "  " not in clean_prompt
    assert len(clean_prompt) > 0


def test_refiner_immutability():
    """Test that pipe() creates new instances and doesn't mutate original."""
    # Create base pipeline
    base = StripHTML() | NormalizeWhitespace()
    assert len(base._operations) == 2

    # Create two different pipelines from base
    pipeline1 = base | TruncateTokens(max_tokens=100)
    pipeline2 = base | TruncateTokens(max_tokens=200)

    # Base should still have 2 operations
    assert len(base._operations) == 2

    # New pipelines should have 3 operations each
    assert len(pipeline1._operations) == 3
    assert len(pipeline2._operations) == 3

    # They should be different objects
    assert pipeline1 is not base
    assert pipeline2 is not base
    assert pipeline1 is not pipeline2

    # Verify operations work independently
    text = "<div>hello   world</div>"
    assert base.run(text) == "hello world"


def test_refiner_pipe_immutability():
    """Test that .pipe() method is also immutable."""
    base = Refiner().pipe(StripHTML())
    assert len(base._operations) == 1

    # Add another operation
    extended = base.pipe(NormalizeWhitespace())
    assert len(extended._operations) == 2

    # Original should still have 1
    assert len(base._operations) == 1

    # They should be different objects
    assert extended is not base
