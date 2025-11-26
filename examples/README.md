# Examples

This folder contains examples demonstrating various features of prompt-groomer.

## Running Examples

```bash
# From the project root
python examples/basic_pipeline.py
python examples/html_cleaning.py
python examples/truncation_strategies.py
python examples/custom_operation.py
```

## Examples Overview

### basic_pipeline.py
Demonstrates the basic pipeline API with multiple operations chained together.
- Strips HTML tags
- Normalizes whitespace
- Truncates to token limit

### html_cleaning.py
Shows how to clean HTML content by removing tags and normalizing whitespace.

### truncation_strategies.py
Demonstrates the three truncation strategies:
- `"end"` - Keep the beginning of the text
- `"start"` - Keep the end of the text
- `"middle"` - Keep both start and end, truncate the middle

### custom_operation.py
Shows how to create your own custom operations by extending the `Operation` base class.
