# Category Budgets

Retrieve aggregated budget information by category.

## Get Aggregated Budgets

Get budget totals aggregated by category and transaction type:

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

budgets = client.category_budgets.aggregated(
    currency_code="ZAR",
)

for budget in budgets:
    print(f"Category {budget.category_id}: {budget.amount} ({budget.transaction_type})")
```

### With Date Filter

Filter budgets by budget period:

```python
from datetime import datetime

budgets = client.category_budgets.aggregated(
    currency_code="ZAR",
    from_budget_period_to=datetime(2024, 3, 1),
)
```

### Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `currency_code` | `str` | *required* | Currency for aggregation (e.g., "ZAR", "USD") |
| `aggregate_by` | `list[str]` | `["transactionCategoryId", "transactionType"]` | Fields to aggregate by |
| `from_budget_period_to` | `datetime` | `None` | End date for budget period filter |

## Response Model

Each `AggregatedCategoryBudget` contains:

| Field | Type | Description |
|-------|------|-------------|
| `amount` | `Decimal` | Budget amount for this category/type |
| `category_id` | `str` | Transaction category ID |
| `transaction_type` | `str` | Transaction type (e.g., "debit", "credit") |
