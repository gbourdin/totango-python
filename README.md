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
tt.track("module", "action")
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
tt.track("dashboard", "opened", user_opts={"plan": "gold"})

# Send an identify-style update without activity module/action
tt.send(account_opts={"tier": "enterprise"})
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
