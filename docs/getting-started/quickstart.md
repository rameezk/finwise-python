# Quick Start

## Initialize the Client

```python
from finwise import FinWise

# Using an API key directly
client = FinWise(api_key="your-api-key")

# Or use the FINWISE_API_KEY environment variable
client = FinWise()
```

## Basic Operations

### List Accounts

```python
accounts = client.accounts.list()
for account in accounts.data:
    print(f"{account.name}: {account.currency} {account.balance}")
```

### Create a Transaction

```python
from decimal import Decimal
from datetime import date

transaction = client.transactions.create(
    account_id="acc_123",
    amount=Decimal("-50.00"),
    transaction_date=date.today(),
    description="Grocery shopping",
    type="expense",
)
```

### Handle Errors

```python
from finwise import FinWise, NotFoundError

client = FinWise()

try:
    account = client.accounts.retrieve("invalid_id")
except NotFoundError as e:
    print(f"Account not found: {e.message}")
```

## Next Steps

- [Configuration](configuration.md) - Learn about client configuration options
- [Accounts](../usage/accounts.md) - Full account management guide
- [Transactions](../usage/transactions.md) - Working with transactions
