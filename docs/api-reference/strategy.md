# Strategy Module API Reference

The Strategy module provides benchmark-tested preset strategies for token optimization. Use these when you want quick savings without manually configuring individual operations.

## Overview

**Version 0.1.5+** introduces three preset strategies optimized for different use cases:

| Strategy | Token Reduction | Quality | Use Case |
|----------|----------------|---------|----------|
| **Minimal** | 4.3% | 98.7% | Maximum quality, minimal risk |
| **Standard** | 4.8% | 98.4% | RAG contexts with duplicates |
| **Aggressive** | 15% | 96.4% | Cost optimization, long contexts |

All strategies return a `Refiner` instance, making them fully compatible with the existing API and extensible with `.pipe()`.

## MinimalStrategy

Basic cleaning with minimal token reduction, prioritizing quality preservation.

::: prompt_refiner.strategy.MinimalStrategy
    options:
      show_source: true
      members_order: source
      heading_level: 3

### Operations

- `StripHTML()` - Remove HTML tags
- `NormalizeWhitespace()` - Collapse excessive whitespace

### Example

```python
from prompt_refiner.strategy import MinimalStrategy

# Create strategy and refiner
refiner = MinimalStrategy().create_refiner()
cleaned = refiner.run("<div>  Your HTML content  </div>")
# Output: "Your HTML content"

# With Markdown conversion
refiner = MinimalStrategy(to_markdown=True).create_refiner()
cleaned = refiner.run("<strong>bold</strong> text")
# Output: "**bold** text"

# Extend with additional operations
from prompt_refiner import RedactPII
refiner = MinimalStrategy().create_refiner()
refiner.pipe(RedactPII(redact_types={"email"}))
```

## StandardStrategy

Enhanced cleaning with deduplication for RAG contexts with potential duplicates.

::: prompt_refiner.strategy.StandardStrategy
    options:
      show_source: true
      members_order: source
      heading_level: 3

### Operations

- `StripHTML()` - Remove HTML tags
- `NormalizeWhitespace()` - Collapse excessive whitespace
- `Deduplicate()` - Remove similar content (sentence-level, 0.8 threshold)

### Example

```python
from prompt_refiner.strategy import StandardStrategy

# Create strategy with defaults
refiner = StandardStrategy().create_refiner()
text = "<div>Hello world. Hello world. Goodbye world.</div>"
cleaned = refiner.run(text)
# Output: "Hello world. Goodbye world."  (duplicate removed)

# Custom similarity threshold
refiner = StandardStrategy(similarity_threshold=0.7).create_refiner()

# Alternative deduplication method
refiner = StandardStrategy(dedup_method="levenshtein").create_refiner()
```

## AggressiveStrategy

Maximum token reduction with deduplication and truncation for cost optimization.

::: prompt_refiner.strategy.AggressiveStrategy
    options:
      show_source: true
      members_order: source
      heading_level: 3

### Operations

- `StripHTML()` - Remove HTML tags
- `NormalizeWhitespace()` - Collapse excessive whitespace
- `Deduplicate()` - Remove similar content (sentence-level, 0.7 threshold)
- `TruncateTokens()` - Limit to max_tokens (default: 150)

### Example

```python
from prompt_refiner.strategy import AggressiveStrategy

# Create strategy with default max_tokens=150
refiner = AggressiveStrategy().create_refiner()
long_text = "word " * 100  # 100 words
cleaned = refiner.run(long_text)
# Output: Truncated to ~150 tokens with duplicates removed

# Custom max_tokens and truncation strategy
refiner = AggressiveStrategy(
    max_tokens=200,
    truncate_strategy="tail"  # Keep last 200 tokens
).create_refiner()

# More aggressive deduplication
refiner = AggressiveStrategy(
    max_tokens=100,
    similarity_threshold=0.6  # More aggressive duplicate detection
).create_refiner()
```

## BaseStrategy

Abstract base class for creating custom strategies.

::: prompt_refiner.strategy.BaseStrategy
    options:
      show_source: true
      members_order: source
      heading_level: 3

### Creating Custom Strategies

```python
from prompt_refiner.strategy import BaseStrategy
from prompt_refiner import StripHTML, NormalizeWhitespace, RedactPII

class CustomStrategy(BaseStrategy):
    def __init__(self, redact_pii: bool = True):
        self.redact_pii = redact_pii

    def get_operations(self):
        operations = [StripHTML(), NormalizeWhitespace()]
        if self.redact_pii:
            operations.append(RedactPII(redact_types={"email", "phone"}))
        return operations

# Use custom strategy
refiner = CustomStrategy(redact_pii=True).create_refiner()
```

## Usage Patterns

### Basic Usage

```python
from prompt_refiner.strategy import MinimalStrategy, StandardStrategy, AggressiveStrategy

# Quick start with minimal
refiner = MinimalStrategy().create_refiner()
cleaned = refiner.run(text)

# Standard for RAG with duplicates
refiner = StandardStrategy().create_refiner()
cleaned = refiner.run(rag_context)

# Aggressive for cost optimization
refiner = AggressiveStrategy(max_tokens=200).create_refiner()
cleaned = refiner.run(long_context)
```

### Composition with Additional Operations

Strategies return `Refiner` instances, so you can extend them with additional operations:

```python
from prompt_refiner.strategy import MinimalStrategy
from prompt_refiner import RedactPII, Deduplicate

# Start with minimal, add PII redaction
refiner = MinimalStrategy().create_refiner()
refiner.pipe(RedactPII(redact_types={"email"}))

# Start with standard, add more aggressive deduplication
from prompt_refiner.strategy import StandardStrategy
refiner = StandardStrategy().create_refiner()
refiner.pipe(Deduplicate(similarity_threshold=0.6))  # More aggressive
```

### Direct Strategy Calling

Strategies also support direct calling for quick one-off processing:

```python
from prompt_refiner.strategy import MinimalStrategy

strategy = MinimalStrategy()
cleaned = strategy(text)  # Equivalent to: strategy.create_refiner().run(text)
```

## Choosing a Strategy

### Minimal Strategy
✅ **Use when:**
- Quality is paramount
- Minimal risk tolerance
- Processing structured content
- First time optimizing prompts

❌ **Avoid when:**
- Budget constraints are tight
- Dealing with very long contexts
- Content has significant duplication

### Standard Strategy
✅ **Use when:**
- RAG contexts with potential duplicates
- Balanced quality and savings needed
- Processing web-scraped content
- General-purpose optimization

❌ **Avoid when:**
- Context is already clean and unique
- Maximum quality preservation required
- Very tight token budgets

### Aggressive Strategy
✅ **Use when:**
- Cost optimization is priority
- Token budgets are tight
- Processing very long contexts
- Quality tolerance is lenient

❌ **Avoid when:**
- Quality cannot be compromised
- Context is already short
- Truncation would remove critical info

## Configuration Reference

### MinimalStrategy Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strip_html` | `bool` | `True` | Whether to strip HTML tags |
| `to_markdown` | `bool` | `False` | Convert HTML to Markdown instead of stripping |

### StandardStrategy Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strip_html` | `bool` | `True` | Whether to strip HTML tags |
| `to_markdown` | `bool` | `False` | Convert HTML to Markdown instead of stripping |
| `similarity_threshold` | `float` | `0.8` | Threshold for deduplication (0.0-1.0) |
| `dedup_method` | `Literal["jaccard", "levenshtein"]` | `"jaccard"` | Deduplication algorithm |

### AggressiveStrategy Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_tokens` | `int` | `150` | Maximum tokens to keep |
| `strip_html` | `bool` | `True` | Whether to strip HTML tags |
| `to_markdown` | `bool` | `False` | Convert HTML to Markdown instead of stripping |
| `similarity_threshold` | `float` | `0.7` | Threshold for deduplication (0.0-1.0) |
| `dedup_method` | `Literal["jaccard", "levenshtein"]` | `"jaccard"` | Deduplication algorithm |
| `truncate_strategy` | `Literal["head", "tail", "middle_out"]` | `"head"` | Which part of text to keep |

## See Also

- [Examples](../examples/index.md) - Comprehensive examples
- [Benchmark Results](../benchmark.md) - Performance and quality metrics
- [Refiner API](refiner.md) - Pipeline composition
