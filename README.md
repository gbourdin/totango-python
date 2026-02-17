# totango-python

Python client for Totango's HTTP tracking pixel API.

## Requirements

- Python 3.14+
- `requests`

## Installation

```bash
python -m pip install totango
```

From source:

```bash
git clone git@github.com:gbourdin/totango-python.git
cd totango-python
python -m pip install -e .
```

## Usage

```python
import totango

client = totango.Totango(
    "SP-XXXX-XX",
    user_id="user-123",
    user_name="Jane User",
    account_id="acct-1",
    account_name="Acme Inc",
)

# Track an activity event
client.track("dashboard", "opened", user_opts={"plan": "gold"})

# Send an identify-style update without activity module/action
client.send(account_opts={"tier": "enterprise"})
```

## JS-Style Tracker API

`TotangoTracker` mirrors the JavaScript `totango-tracker` API shape.

```python
import totango

tracker = totango.TotangoTracker("SP-XXXX-XX", "EU", "api-token-value")
tracker.trackActivity("billing", "opened", "user@example.com", "Acme")
tracker.setUserAttributes("user-1", "Jane User", {"plan": "enterprise"})
tracker.setAccountAttributes("acct-1", "Acme", {"tier": "gold"})
tracker.setAttributes(
    "acct-1",
    "Acme",
    "user-1",
    "Jane User",
    {"a.segment": "saas", "u.plan": "enterprise"},
)
```

## HTTP API Coverage Helpers

The Totango HTTP API supports `sdr_p` (system version/build) and additional raw fields.

```python
import totango

client = totango.Totango("SP-XXXX-XX", user_id="user-123", user_name="Jane User")

client.track(
    "dashboard",
    "opened",
    system_version="web@2026.02.17",
    raw_opts={"sdr_custom_flag": "true"},
)

# If only account_name is provided, it is used for both sdr_o and sdr_odn
client.send(account_name="Acme Inc")
```

## Development

Run tests:

```bash
python -m unittest discover -s tests -v
```

Lint and type-check (after installing `.[dev]`):

```bash
ruff check .
ty check .
```
