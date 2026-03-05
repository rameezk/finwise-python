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
balances = client.account_balances.list()

for balance in balances:
    if balance.amount:
        print(f"{balance.date}: {balance.amount.format()}")
```

## Get Aggregated Balance History

Get balance history over time for a specific currency:

```python
snapshots = client.account_balances.aggregated(currency="ZAR")

for snapshot in snapshots[-5:]:  # Last 5 snapshots
    print(f"{snapshot.date}: {snapshot.amount.format()}")
```

!!! note "Currency Parameter"
    The `currency` parameter is required and specifies which currency to aggregate balances for (e.g., "USD", "EUR", "ZAR").

## Archive a Balance Record

```python
client.account_balances.archive("bal_123")
```
