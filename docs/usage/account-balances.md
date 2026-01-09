# Account Balances

Track point-in-time balance snapshots for accounts.

## Create a Balance Record

```python
from decimal import Decimal
from datetime import date
from finwise import FinWise

client = FinWise(api_key="your-api-key")

balance = client.account_balances.create(
    account_id="acc_123",
    balance=Decimal("5000.00"),
    balance_date=date(2024, 1, 15),
)
```

!!! tip "When to Use Balance Records"
    Balance records are useful for:

    - Tracking account balances over time
    - Reconciling with bank statements
    - Building net worth history

## List Balance Records

```python
balances = client.account_balances.list(account_id="acc_123")

for balance in balances.data:
    print(f"{balance.balance_date}: {balance.balance}")
```

## Get Aggregated Balance

Get the total balance across all accounts:

```python
summary = client.account_balances.aggregated()
print(f"Total: {summary.currency} {summary.total_balance}")
print(f"Across {summary.account_count} accounts")
```

You can also get the balance as of a specific date:

```python
summary = client.account_balances.aggregated(
    as_of_date=date(2024, 1, 31)
)
```

## Archive a Balance Record

```python
client.account_balances.archive("bal_123")
```
