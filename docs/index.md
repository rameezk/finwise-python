# FinWise Python SDK

**Unofficial Python SDK for the FinWise API**

!!! warning "Unofficial SDK"
    This is an unofficial, community-maintained Python SDK for the FinWise API. It is not affiliated with, endorsed by, or officially supported by FinWise.

A simple, type-safe Python client for the [FinWise API](https://finwiseapp.io/docs/api).

For the official API documentation, see [finwiseapp.io/docs/api](https://finwiseapp.io/docs/api).

## Features

- **Type-safe**: Full type hints and Pydantic models
- **Automatic retries**: Exponential backoff for transient errors
- **Pagination support**: Easy iteration through paginated results
- **Context manager**: Automatic resource cleanup

## Quick Example

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# List all accounts
accounts = client.accounts.list()
for account in accounts.data:
    print(f"{account.name}: {account.currency} {account.balance}")
```

## Requirements

- Python 3.9+
- httpx
- pydantic

## License

MIT License - see [LICENSE](https://github.com/rameezk/finwise-python/blob/main/LICENSE) for details.
