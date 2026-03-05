# Pagination

All list endpoints support pagination and return a `PaginatedResponse` object.

## Basic Usage

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Get first page of accounts
result = client.accounts.list(page_number=1, page_size=50)

print(f"Page {result.page_number} of {result.total_pages}")
print(f"Total items: {result.total_count}")

# Iterate through items on this page
for account in result.data:
    print(account.name)

# Access by index
first_account = result[0]
```

## Paginated Response

The `PaginatedResponse[T]` object contains:

| Property | Type | Description |
|----------|------|-------------|
| `data` | `list[T]` | Items on the current page |
| `page_number` | `int` | Current page number |
| `page_size` | `int` | Items per page |
| `total_count` | `int` | Total items across all pages |
| `total_pages` | `int` | Total number of pages |
| `has_next` | `bool` | Whether there's a next page |
| `has_previous` | `bool` | Whether there's a previous page |

## Iterating Through Pages

```python
page_number = 1
all_transactions = []

while True:
    result = client.transactions.list(page_number=page_number, page_size=100)
    all_transactions.extend(result.data)

    if not result.has_next:
        break
    page_number += 1

print(f"Fetched {len(all_transactions)} total transactions")
```

## List Methods

All list methods return `PaginatedResponse`:

| Method | Return Type |
|--------|-------------|
| `accounts.list()` | `PaginatedResponse[Account]` |
| `transactions.list()` | `PaginatedResponse[Transaction]` |
| `transaction_categories.list()` | `PaginatedResponse[TransactionCategory]` |
| `account_balances.list()` | `PaginatedResponse[AccountBalance]` |

## Pagination Parameters

All list methods accept these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_number` | `int` | `1` | Page to retrieve (1-indexed) |
| `page_size` | `int` | `100` | Items per page |
