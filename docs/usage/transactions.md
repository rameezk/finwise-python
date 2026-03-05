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

for txn in transactions.data:
    print(f"{txn.transaction_date}: {txn.description} ({txn.amount.format()})")
```

### Filtering

Filter transactions by date range, type, or category:

```python
from datetime import datetime

# Filter by date range
transactions = client.transactions.list(
    from_date=datetime(2024, 1, 1),
    to_date=datetime(2024, 12, 31, 23, 59, 59),
)

# Filter by transaction type
debits = client.transactions.list(transaction_types=["debit"])

# Filter by category
groceries = client.transactions.list(category_ids=["cat_groceries"])

# Combine filters
filtered = client.transactions.list(
    from_date=datetime(2024, 1, 1),
    transaction_types=["debit"],
    exclude_transfers=True,
)
```

### Filter Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `from_date` | `datetime` | `None` | Filter transactions from this date |
| `to_date` | `datetime` | `None` | Filter transactions up to this date |
| `transaction_types` | `list[str]` | `None` | Filter by types (e.g., `["debit", "credit"]`) |
| `category_ids` | `list[str]` | `None` | Filter by category IDs |
| `exclude_archived` | `bool` | `True` | Exclude archived transactions |
| `exclude_transfers` | `bool` | `False` | Exclude transfer transactions |
| `exclude_excluded_transactions` | `bool` | `True` | Exclude manually excluded transactions |
| `exclude_parent_transactions` | `bool` | `True` | Exclude parent/split transactions |

### Pagination

```python
# Get first page
page1 = client.transactions.list(page_number=1, page_size=50)

print(f"Page {page1.page_number} of {page1.total_pages}")
print(f"Total transactions: {page1.total_count}")

# Get next page if available
if page1.has_next:
    page2 = client.transactions.list(page_number=2, page_size=50)
```

## Get Aggregated Totals

Get transaction totals aggregated by category and type:

```python
# Get spending by category
aggregated = client.transactions.aggregated(
    currency_code="ZAR",
    time_zone="Africa/Johannesburg",
)

for item in aggregated:
    print(f"Category {item.category_id}: {item.amount} ({item.transaction_type})")
```

### Aggregation Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `currency_code` | `str` | *required* | Currency for aggregation (e.g., "ZAR", "USD") |
| `time_zone` | `str` | `"UTC"` | Time zone for date calculations |
| `aggregate_by` | `list[str]` | `["transactionCategoryId", "transactionType"]` | Fields to aggregate by |
| `budget_start_date` | `int` | `1` | Day of month when budget period starts |
| `to_date` | `datetime` | `None` | End date for aggregation period |
| `exclude_archived` | `bool` | `True` | Exclude archived transactions |
| `exclude_transfers` | `bool` | `True` | Exclude transfer transactions |
| `exclude_excluded_transactions` | `bool` | `True` | Exclude manually excluded transactions |
| `exclude_parent_transactions` | `bool` | `True` | Exclude parent/split transactions |

## Archive a Transaction

```python
client.transactions.archive("txn_123")
```
