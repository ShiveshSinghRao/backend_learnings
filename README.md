# learn-backend

A step-by-step learning repo for backend concepts, mapped to [dubbing-service](../dubbing-service/).

Each PR introduces one backend concept with working code, tests, and a detailed explainer doc.

## Setup

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate   # macOS/Linux

# Install the package in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify it works
python -c "import learn_backend; print('Success!')"

# Run tests
pytest
```

## Structure

- `learn_backend/` -- Main application package
- `tests/` -- Test suite
- `docs/explainers/` -- Concept explainer docs for each PR
