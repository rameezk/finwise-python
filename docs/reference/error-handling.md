# Error Handling

The SDK provides a comprehensive exception hierarchy for handling errors.

## Exception Hierarchy

```
FinWiseError (base)
├── FinWiseAPIError (API returned an error)
│   ├── AuthenticationError (401)
│   ├── PermissionDeniedError (403)
│   ├── NotFoundError (404)
│   ├── ValidationError (400, 422)
│   ├── ConflictError (409)
│   ├── RateLimitError (429)
│   └── ServerError (5xx)
├── FinWiseConnectionError (connection failed)
└── FinWiseTimeoutError (request timed out)
```

## Usage Example

```python
from finwise import (
    FinWise,
    FinWiseError,
    FinWiseAPIError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ValidationError,
    ConflictError,
    RateLimitError,
    ServerError,
    FinWiseConnectionError,
    FinWiseTimeoutError,
)

client = FinWise(api_key="your-api-key")

try:
    account = client.accounts.retrieve("invalid_id")
except NotFoundError as e:
    print(f"Not found: {e.message}")
    print(f"Request ID: {e.request_id}")  # For debugging
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
except FinWiseAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
except FinWiseConnectionError as e:
    print(f"Connection failed: {e.message}")
except FinWiseError as e:
    print(f"Error: {e.message}")
```

## Error Properties

### FinWiseAPIError

| Property | Type | Description |
|----------|------|-------------|
| `message` | `str` | Error message from the API |
| `status_code` | `int` | HTTP status code |
| `request_id` | `str` | Unique request ID for debugging |

### RateLimitError

| Property | Type | Description |
|----------|------|-------------|
| `retry_after` | `int` | Seconds to wait before retrying |

## Best Practices

1. **Catch specific exceptions first**, then broader ones
2. **Log the `request_id`** when reporting issues to support
3. **Handle `RateLimitError`** by waiting `retry_after` seconds
4. **Use `FinWiseError`** as a catch-all for SDK errors
