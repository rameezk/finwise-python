# Transactions

Record and query financial transactions.

## Create a Transaction

```python
from decimal import Decimal
from datetime import date
from finwise import FinWise

client = FinWise(api_key="your-api-key")

transaction = client.transactions.create(
    account_id="acc_123",
    amount=Decimal("-50.00"),  # Negative for expenses
    transaction_date=date.today(),
    description="Grocery shopping",
    category_id="cat_groceries",
    type="expense",
)
```

### Transaction Types

| Type | Description |
|------|-------------|
| `income` | Money coming in |
| `expense` | Money going out |
| `transfer` | Transfer between accounts |

!!! tip "Amount Sign Convention"
    Use negative amounts for expenses and positive amounts for income. This makes calculations straightforward.

## List Transactions

```python
# Basic listing
transactions = client.transactions.list(account_id="acc_123")

# With date filters
transactions = client.transactions.list(
    account_id="acc_123",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
    type="expense",
)

for txn in transactions.data:
    print(f"{txn.transaction_date}: {txn.description} ({txn.amount})")
```

## Get Aggregated Summary

Get totals for a date range:

```python
summary = client.transactions.aggregated(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
)
print(f"Income: {summary.total_income}")
print(f"Expenses: {summary.total_expenses}")
print(f"Net: {summary.net_amount}")
```

## Archive a Transaction

```python
client.transactions.archive("txn_123")
```
