# totango-python

[![PyPI Version](https://img.shields.io/pypi/v/totango)](https://pypi.org/project/totango/)
[![PyPI License](https://img.shields.io/pypi/l/totango)](https://pypi.org/project/totango/)
[![Python Versions](https://img.shields.io/pypi/pyversions/totango)](https://pypi.org/project/totango/)
[![CI](https://github.com/gbourdin/totango-python/actions/workflows/ci.yml/badge.svg)](https://github.com/gbourdin/totango-python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/gbourdin/totango-python/graph/badge.svg?branch=master)](https://codecov.io/gh/gbourdin/totango-python)

Python client for Totango's HTTP tracking pixel API.

## Requirements

- Python 3.10+
- `requests`

## Installation

```bash
pip install totango
```

From source:

```bash
git clone git@github.com:gbourdin/totango-python.git
cd totango-python
pip install -e .
```

## Quick Usage

```python
import totango

tt = totango.Totango("SP-XXXX-XX", user_id="user-123")
tt.track_activity("module", "action")
```

## Usage

```python
import totango

tt = totango.Totango(
    "SP-XXXX-XX",
    user_id="user-123",
    user_name="Jane User",
    account_id="acct-1",
    account_name="Acme Inc",
)

# Track an activity event
tt.track_activity("dashboard", "opened", user_opts={"plan": "gold"})

# Send an identify-style update without activity module/action
tt.send(account_opts={"tier": "enterprise"})
```

## Tracker API (Parity On `Totango`)

Feature parity with the JavaScript tracker is available on `Totango` directly,
while preserving the existing constructor and methods.
When `region` is set, `api_token` is required.

```python
import totango

tt = totango.Totango(
    "SP-XXXX-XX",
    region="EU",
    api_token="api-token-value",
    user_id="user-1",
    user_name="Jane User",
)
tt.track_activity("billing", "opened", user_id="user@example.com", user_name="user@example.com")
tt.set_user_attributes("user-1", "Jane User", {"plan": "enterprise"})
tt.set_account_attributes("acct-1", "Acme", {"tier": "gold"})
tt.set_attributes(
    "acct-1",
    "Acme",
    "user-1",
    "Jane User",
    {"a.segment": "saas", "u.plan": "enterprise"},
)

# Legacy method (deprecated):
# tt.track("billing", "opened", user_id="user@example.com", user_name="user@example.com")
```

## Development

Run the default test suite:

```bash
python -m unittest discover -s tests -v
```

Run lint and type checks:

```bash
ruff check .
ty check .
```

Run the multi-version matrix with tox (3.10 through 3.15):

```bash
tox -e py310,py311,py312,py313,py314,py315
tox -e lint,type
```

Continuous integration also runs this matrix in GitHub Actions on each push and pull request.
