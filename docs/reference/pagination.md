# Pagination

!!! note "API Behavior"
    The FinWise API does not currently support pagination for list endpoints. All `list()` methods return all available items as a simple Python list.

## Basic Usage

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Get all accounts
accounts = client.accounts.list()
print(f"Found {len(accounts)} accounts")

# Iterate through items
for account in accounts:
    print(account.name)

# Access by index
first_account = accounts[0]
```

## List Methods

All list methods return a `list` of model objects:

| Method | Return Type |
|--------|-------------|
| `accounts.list()` | `list[Account]` |
| `transactions.list()` | `list[Transaction]` |
| `transaction_categories.list()` | `list[TransactionCategory]` |
| `account_balances.list()` | `list[AccountBalance]` |

## Filtering

While pagination is not supported, you can still filter results using available parameters:

```python
# Filter transactions by date range
transactions = client.transactions.list(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
    type="expense",
)

# Filter by account
transactions = client.transactions.list(account_id="acc_123")

# Filter account balances
balances = client.account_balances.list(account_id="acc_123")
```
