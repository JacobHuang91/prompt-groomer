# Prompt Groomer

A lightweight Python library for optimizing and cleaning LLM inputs. Reduce token usage, improve prompt quality, and lower API costs.

## Overview

Prompt Groomer helps you clean and optimize prompts before sending them to LLM APIs. By removing unnecessary whitespace, duplicate characters, and other inefficiencies, you can:

- Reduce token usage and API costs
- Improve prompt quality and consistency
- Process inputs more efficiently

## Status

This project is in early development. Features are being added iteratively.

## Installation

```bash
# Using uv (recommended)
uv pip install prompt-groomer

# Using pip
pip install prompt-groomer
```

## Quick Start

Build custom cleaning pipelines with a fluent API:

```python
from prompt_groomer import Groomer
from prompt_groomer.ops import StripHTML, NormalizeWhitespace, TruncateTokens

# Define a cleaning pipeline
groomer = (
    Groomer()
    .pipe(StripHTML())
    .pipe(NormalizeWhitespace())
    .pipe(TruncateTokens(max_tokens=1000, strategy="middle"))
)

raw_input = "<div>  User input with <b>lots</b> of   spaces... </div>"
clean_prompt = groomer.run(raw_input)
# Output: "User input with lots of spaces..."
```

**Available Operations:**
- `StripHTML()` - Remove HTML tags
- `NormalizeWhitespace()` - Collapse multiple spaces
- `TruncateTokens(max_tokens, strategy)` - Truncate to token limit
  - Strategies: `"start"`, `"end"`, `"middle"` (keeps both ends)

## Examples

Check out the [`examples/`](examples/) folder for more usage examples:
- Basic pipeline usage
- HTML cleaning
- Truncation strategies
- Creating custom operations

## Planned Features

- Remove excessive whitespace
- Normalize line breaks
- Remove duplicate characters
- Strip invalid Unicode characters
- Configurable cleaning strategies
- Token counting and optimization suggestions

## Development

This project uses `uv` for dependency management and `make` for common tasks.

```bash
# Install dependencies
make install

# Run tests
make test

# Format code
make format
```

## License

MIT