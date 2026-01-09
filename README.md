# FinWise Python SDK

![PyPI - Version](https://img.shields.io/pypi/v/finwise-python?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/finwise-python?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/finwise-python?style=for-the-badge&color=blue)

A simple Python client for the [FinWise API](https://finwiseapp.io/docs/api).

## Installation

```bash
pip install finwise-python
```

For development:

```bash
pip install finwise-python[dev]
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

## Usage

### Accounts

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Create an account
account = client.accounts.create(
    name="Savings Account",
    type="savings",  # checking, savings, credit, investment, loan, other
    currency="USD",
    description="Emergency fund",
    initial_balance=10000.00,
)
print(f"Created: {account.id}")

# Get a specific account
account = client.accounts.retrieve("acc_123")
print(f"{account.name}: {account.balance}")

# Update an account
account = client.accounts.update(
    "acc_123",
    name="Renamed Account",
    description="Updated description",
)

# List accounts with pagination
accounts = client.accounts.list(page_number=1, page_size=50)
print(f"Total accounts: {accounts.total_count}")

for account in accounts.data:
    print(f"  - {account.name}")

if accounts.has_next:
    next_page = client.accounts.list(page_number=2, page_size=50)

# Archive an account
archived = client.accounts.archive("acc_123")
print(f"Archived at: {archived.archived_at}")
```

### Transactions

```python
from decimal import Decimal
from datetime import date
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Create a transaction
transaction = client.transactions.create(
    account_id="acc_123",
    amount=Decimal("-50.00"),  # Negative for expenses
    transaction_date=date.today(),
    description="Grocery shopping",
    category_id="cat_groceries",
    type="expense",  # income, expense, transfer
)

# List transactions with filters
transactions = client.transactions.list(
    account_id="acc_123",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
    type="expense",
)

for txn in transactions.data:
    print(f"{txn.transaction_date}: {txn.description} ({txn.amount})")

# Get aggregated summary
summary = client.transactions.aggregated(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
)
print(f"Income: {summary.total_income}")
print(f"Expenses: {summary.total_expenses}")
print(f"Net: {summary.net_amount}")

# Archive a transaction
client.transactions.archive("txn_123")
```

### Account Balances

```python
from decimal import Decimal
from datetime import date
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Create a balance record (point-in-time snapshot)
balance = client.account_balances.create(
    account_id="acc_123",
    balance=Decimal("5000.00"),
    balance_date=date(2024, 1, 15),
)

# List balance records
balances = client.account_balances.list(account_id="acc_123")

# Get aggregated balance across all accounts
summary = client.account_balances.aggregated()
print(f"Total: {summary.currency} {summary.total_balance}")
print(f"Across {summary.account_count} accounts")
```

### Transaction Categories

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Create a category
category = client.transaction_categories.create(
    name="Groceries",
    color="#4CAF50",
    icon="shopping_cart",
)

# Create a subcategory
subcategory = client.transaction_categories.create(
    name="Organic Food",
    color="#8BC34A",
    parent_id=category.id,
)

# List categories
categories = client.transaction_categories.list()
for cat in categories.data:
    prefix = "  " if cat.is_subcategory else ""
    print(f"{prefix}{cat.name}")

# Delete a category
client.transaction_categories.delete("cat_123")
```

## Error Handling

The SDK provides a comprehensive exception hierarchy:

```python
from finwise import (
    FinWise,
    FinWiseError,          # Base exception
    FinWiseAPIError,       # API returned an error
    AuthenticationError,   # Invalid/missing API key (401)
    PermissionDeniedError, # Permission denied (403)
    NotFoundError,         # Resource not found (404)
    ValidationError,       # Invalid request data (400, 422)
    ConflictError,         # Conflict error (409)
    RateLimitError,        # Rate limit exceeded (429)
    ServerError,           # Server error (5xx)
    FinWiseConnectionError,# Connection failed
    FinWiseTimeoutError,   # Request timed out
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

## Configuration

```python
from finwise import FinWise

client = FinWise(
    api_key="your-api-key",
    base_url="https://api.finwiseapp.io",  # Default
    timeout=30.0,    # Request timeout in seconds
    max_retries=3,   # Automatic retries for transient errors
)
```

### Environment Variable

Set your API key via environment variable:

```bash
export FINWISE_API_KEY="your-api-key"
```

```python
from finwise import FinWise

# Automatically uses FINWISE_API_KEY
client = FinWise()
```

### Context Manager

Use as a context manager for automatic cleanup:

```python
from finwise import FinWise

with FinWise(api_key="your-api-key") as client:
    accounts = client.accounts.list()
    # Client is automatically closed when exiting the block
```

## Pagination

All list methods return a `PaginatedResponse` object:

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Get first page
accounts = client.accounts.list(page_number=1, page_size=50)

print(f"Page {accounts.page_number} of {accounts.total_pages}")
print(f"Showing {len(accounts)} of {accounts.total_count} accounts")

# Iterate through items on this page
for account in accounts.data:
    print(account.name)

# Access by index
first_account = accounts[0]  # or accounts.data[0]

# Check for more pages
if accounts.has_next:
    next_page = client.accounts.list(
        page_number=accounts.page_number + 1,
        page_size=50,
    )
```

## API Reference

### Client

| Method | Description |
|--------|-------------|
| `FinWise(api_key, ...)` | Create a new client |
| `client.close()` | Close the client |

### Accounts (`client.accounts`)

| Method | Description |
|--------|-------------|
| `create(name, type, ...)` | Create a new account |
| `retrieve(account_id)` | Get an account by ID |
| `update(account_id, ...)` | Update an account |
| `list(page_number, page_size)` | List all accounts |
| `archive(account_id)` | Archive an account |

### Transactions (`client.transactions`)

| Method | Description |
|--------|-------------|
| `create(account_id, amount, ...)` | Create a transaction |
| `list(account_id, start_date, ...)` | List transactions |
| `aggregated(start_date, end_date, ...)` | Get aggregated summary |
| `archive(transaction_id)` | Archive a transaction |

### Account Balances (`client.account_balances`)

| Method | Description |
|--------|-------------|
| `create(account_id, balance, ...)` | Create a balance record |
| `list(account_id, ...)` | List balance records |
| `aggregated(as_of_date, ...)` | Get aggregated balance |
| `archive(balance_id)` | Archive a balance record |

### Transaction Categories (`client.transaction_categories`)

| Method | Description |
|--------|-------------|
| `create(name, color, ...)` | Create a category |
| `list(parent_id, ...)` | List categories |
| `delete(category_id)` | Delete a category |

## Requirements

- Python 3.9+
- httpx
- pydantic

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [FinWise App](https://finwiseapp.io)
- [API Documentation](https://finwiseapp.io/docs/api)
