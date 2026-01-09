# FinWise Python SDK (Unofficial)

![Unofficial](https://img.shields.io/badge/Status-Unofficial-orange?style=for-the-badge)
![PyPI - Version](https://img.shields.io/pypi/v/finwise-python?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/finwise-python?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/finwise-python?style=for-the-badge&color=blue)

> **Note:** This is an unofficial, community-maintained Python SDK for the FinWise API. It is not affiliated with, endorsed by, or officially supported by FinWise.

A simple Python client for the [FinWise API](https://finwiseapp.io/docs/api).

## Installation

```bash
pip install finwise-python
```

## Quick Start

```python
from finwise import FinWise

# Initialize the client
client = FinWise(api_key="your-api-key")

# Or use the FINWISE_API_KEY environment variable
client = FinWise()

# List all accounts
accounts = client.accounts.list()
for account in accounts.data:
    print(f"{account.name}: {account.currency} {account.balance}")
```

## Features

- Automatic retries with exponential backoff
- Pagination support
- Context manager support
- Full type hints

## Documentation

For full documentation, see [rameezk.github.io/finwise-python](https://rameezk.github.io/finwise-python).

## Links

- [Documentation](https://rameezk.github.io/finwise-python)
- [Official FinWise API Docs](https://finwiseapp.io/docs/api)
- [PyPI](https://pypi.org/project/finwise-python/)
- [GitHub](https://github.com/rameezk/finwise-python)

## License

MIT License - see [LICENSE](LICENSE) for details.
