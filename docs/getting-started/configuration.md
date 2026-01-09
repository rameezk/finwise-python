# Configuration

## Client Options

```python
from finwise import FinWise

client = FinWise(
    api_key="your-api-key",
    base_url="https://api.finwiseapp.io",  # Default
    timeout=30.0,    # Request timeout in seconds
    max_retries=3,   # Automatic retries for transient errors
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `None` | Your FinWise API key. Falls back to `FINWISE_API_KEY` env var |
| `base_url` | `str` | `https://api.finwiseapp.io` | API base URL |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Number of retries for transient errors |

## Environment Variable

Set your API key via environment variable to avoid hardcoding it:

```bash
export FINWISE_API_KEY="your-api-key"
```

```python
from finwise import FinWise

# Automatically uses FINWISE_API_KEY
client = FinWise()
```

## Context Manager

Use the client as a context manager for automatic cleanup:

```python
from finwise import FinWise

with FinWise(api_key="your-api-key") as client:
    accounts = client.accounts.list()
    # Client is automatically closed when exiting the block
```

This ensures the underlying HTTP connection is properly closed when you're done.
