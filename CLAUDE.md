# Prompt Groomer - Project Context

This document provides context for Claude Code and developers working on this project.

## Project Purpose

Prompt Groomer is a Python library designed to optimize LLM prompts by cleaning and reducing unnecessary tokens. This helps users:

- Lower API costs by reducing token count
- Improve prompt quality through normalization
- Maintain consistent input formatting

## Architecture

The library uses a simple, modular design:

- **Core module**: Contains the main cleaning functions
- **Utilities**: Helper functions for text processing
- **Strategies**: Different cleaning approaches users can apply

## Development Philosophy

- Keep it lightweight - minimal dependencies
- Focus on performance - cleaning should be fast
- Make it configurable - users should control cleaning behavior
- Start simple - add features incrementally

## Key Considerations

1. **Unicode handling**: Be careful with non-ASCII characters
2. **Whitespace**: Different types (spaces, tabs, newlines) need different handling
3. **Performance**: Process large prompts efficiently
4. **Backward compatibility**: Don't break existing functionality when adding features

## Technology Stack

- Python 3.8+
- uv for package management
- pytest for testing
- ruff for linting and formatting

## Code Style

- Follow PEP 8
- Use type hints
- Keep functions small and focused
- Write clear docstrings

## Testing

- Unit tests for all cleaning functions
- Edge case testing (empty strings, Unicode, very long inputs)
- Performance benchmarks for large inputs

## Future Vision

This will eventually become a product offering prompt optimization as a service. The library is the foundation for that product.
