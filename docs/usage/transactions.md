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
transactions = client.transactions.list()

for txn in transactions:
    print(f"{txn.transaction_date}: {txn.description} ({txn.amount.format()})")
```

!!! note "No Filtering"
    The API does not support filtering. All transactions are returned.

## Archive a Transaction

```python
client.transactions.archive("txn_123")
```
