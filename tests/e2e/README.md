# End-to-End Tests

This directory contains end-to-end tests that verify the library works correctly when installed via pip (as a real user would install it).

## Purpose

E2E tests ensure:
- The package installs correctly via pip
- All imports work as expected
- Core functionality works in a production-like environment
- No dependencies are missing from package configuration

## Running Locally

### 1. With Development Environment

```bash
uv run python tests/e2e/test_basic_usage.py
```

### 2. With Local Build (simulates package installation)

```bash
# Build the package
uv build

# Install in a fresh virtual environment
python3 -m venv /tmp/test-env
source /tmp/test-env/bin/activate
pip install dist/llm_prompt_refiner-*.whl

# Run e2e tests
python tests/e2e/test_basic_usage.py
```

### 3. With PyPI (simulates real user experience)

```bash
# Create fresh environment
python3 -m venv /tmp/pypi-test
source /tmp/pypi-test/bin/activate

# Install from PyPI (what users do!)
pip install llm-prompt-refiner

# Clone repo to get test script
git clone https://github.com/JacobHuang91/prompt-refiner.git /tmp/prompt-refiner
cd /tmp/prompt-refiner

# Run e2e tests
python tests/e2e/test_basic_usage.py
```

## Testing Strategy

We use **three stages** to ensure quality at different points in the development lifecycle:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         E2E Testing Strategy                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STAGE 1: Development    STAGE 2: Pre-Publish    STAGE 3: Post-Publish │
│  ───────────────────     ──────────────────       ─────────────────    │
│  e2e.yml                 publish.yml              e2e-pypi.yml          │
│  ↓                       ↓                        ↓                     │
│  1. uv build             1. uv build              1. Wait for           │
│  2. pip install          2. pip install              publish ✓          │
│     dist/*.whl              dist/*.whl            2. Wait 60s           │
│  3. Test                 3. Test                     for PyPI           │
│                          4. If ✓ → Publish        3. pip install        │
│                             to PyPI                  llm-prompt-        │
│                                                      refiner            │
│  When: Every push/PR     When: Before publish     4. Test               │
│  Tests: Changes work     Tests: Package works                           │
│  Gate: Must pass         Gate: Must pass to       When: After publish   │
│        to merge                publish             Tests: Users can     │
│                                                           install        │
│                                                    Gate: Verification    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## GitHub Actions

We have **three separate workflows** that test at different stages:

### 1. **Development Tests** (`.github/workflows/e2e.yml`)

**Trigger:** Every push and PR

**Purpose:** Test changes during development

**What it does:**
```bash
uv build                      # Build from current code
pip install dist/*.whl        # Install local wheel
python tests/e2e/...          # Run e2e tests
```

**Gate:** Must pass to merge PR

---

### 2. **Pre-Publish Tests** (`.github/workflows/publish.yml`)

**Trigger:** Part of publish workflow, runs BEFORE publishing

**Purpose:** Final safety check before publishing to PyPI

**What it does:**
```bash
uv build                      # Build package
pip install dist/*.whl        # Test local wheel
python tests/e2e/...          # Run e2e tests
# Only if tests pass ✓
uv publish                    # Publish to PyPI
```

**Sequential Execution:**
```
pre-publish-test ✓ → publish job → PyPI
```

**Gate:** Must pass to publish to PyPI

**Why:**
- Last chance to catch bugs before publishing
- Tests on Python 3.9, 3.10, 3.11, 3.12
- Prevents bad releases

---

### 3. **Post-Publish Verification** (`.github/workflows/e2e-pypi.yml`)

**Trigger:** After "Publish to PyPI" workflow completes successfully

**Purpose:** Verify users can install from PyPI

**What it does:**
```bash
# Waits for publish.yml to complete
sleep 60                         # Wait for PyPI propagation
pip install llm-prompt-refiner   # Install from PyPI (what users do!)
python tests/e2e/...             # Run e2e tests
```

**Sequential Execution:**
```
publish.yml completes ✓ → e2e-pypi.yml starts → Tests from PyPI
```

**Gate:** Verification only (already published)

**Why:**
- Verify the published version works for users
- Catch PyPI-specific issues (broken dependencies, missing files)
- Ensure successful upload

**Manual Testing:** You can also test a specific version:
```
GitHub Actions → E2E Tests (PyPI) → Run workflow → Enter version
```

## Tests Included

- **test_imports**: Verify all core components can be imported
- **test_messages_packer**: Test MessagesPacker with default strategies
- **test_text_packer**: Test TextPacker with different formats
- **test_pipeline**: Test pipeline composition with | operator
- **test_strategies**: Test preset strategies (Minimal, Standard, Aggressive)
- **test_token_counting**: Test token counting functionality

## Adding New E2E Tests

When adding new features, consider adding e2e tests if:
1. The feature is user-facing (part of public API)
2. The feature requires specific dependencies
3. The feature might break in installation scenarios

Keep e2e tests simple and focused on real-world usage patterns.
