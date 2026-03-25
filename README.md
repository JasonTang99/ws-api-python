Unofficial Wealthsimple API Library for Python
==============================================

This library allows you to access your own Wealthsimple account using the Wealthsimple (GraphQL) API.

> **Python 3.10+ required**

Features
--------

- Retrieve all accounts (RRSP, TFSA, FHSA, cash, margin, crypto, credit card)
- Get account balances and positions
- Fetch historical performance (net value, deposits, gains)
- Access transaction/activity history
- Search securities and get market data
- Historical price quotes
- Handle 2FA (TOTP) authentication
- Automatic session refresh
- Optional security data caching

Installation
------------

```bash
uv add ws-api
# or
pip install ws-api
```

### Basic Example

```python
from ws_api import WealthsimpleAPI

# Login (will prompt for username/password/TOTP)
session = WealthsimpleAPI.login(username="you@example.com", password="yourpassword")
ws = WealthsimpleAPI.from_token(session)

# Get your accounts
accounts = ws.get_accounts()
for account in accounts:
    print(f"{account['description']}: {account['number']}")
```

### Full Example

Note: You'll need the keyring package to run the code below. Install with: `uv add keyring` (or `pip install keyring`)

See [tests/test_full_example.py](https://github.com/gboudreau/ws-api-python/blob/main/tests/test_full_example.py)


Projects Using It
-----------------

- [wealthgrabber](https://github.com/ebastos/wealthgrabber) - Wealthsimple portfolio analytics
