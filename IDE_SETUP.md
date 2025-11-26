# IDE Setup Guide

This project uses a `src` layout for better package organization. IDEs need to be configured to recognize the `src` directory for import resolution.

## PyCharm Setup (Required)

**You must mark the `src` folder as a Sources Root:**

1. In the Project view, right-click the `src` folder
2. Select **"Mark Directory as"** → **"Sources Root"**
3. The `src` folder icon should turn blue
4. If imports still show errors, do: **File → Invalidate Caches → Invalidate and Restart**

That's it! PyCharm will now resolve all imports correctly.

## VS Code

The project includes `.vscode/settings.json` which automatically configures import resolution. If you still see import errors:

1. Reload the window: `Cmd+Shift+P` → "Developer: Reload Window"
2. Select the correct Python interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"

## Verifying Installation

Run these commands to verify the package is installed correctly:

```bash
# Check package is installed
pip show prompt-groomer

# Test imports work
python -c "from prompt_groomer import Groomer; print('✓ Imports work')"

# Run examples
python examples/basic_pipeline.py

# Run tests
pytest tests/ -v
```

If these commands work, the package is installed correctly and any remaining IDE warnings can be ignored.

## Installing in Development Mode

```bash
# Using pip
pip install -e .

# Using uv (recommended)
uv pip install -e .
```

This installs the package in editable mode, so changes to the code are immediately reflected without reinstalling.
