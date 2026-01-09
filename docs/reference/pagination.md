# Pagination

All list methods return a `PaginatedResponse` object for easy iteration through results.

## Basic Usage

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

# Get first page
accounts = client.accounts.list(page_number=1, page_size=50)

print(f"Page {accounts.page_number} of {accounts.total_pages}")
print(f"Showing {len(accounts)} of {accounts.total_count} accounts")
```

## PaginatedResponse Properties

| Property | Type | Description |
|----------|------|-------------|
| `data` | `list` | Items on the current page |
| `page_number` | `int` | Current page number (1-indexed) |
| `page_size` | `int` | Items per page |
| `total_count` | `int` | Total items across all pages |
| `total_pages` | `int` | Total number of pages |
| `has_next` | `bool` | Whether there's a next page |
| `has_previous` | `bool` | Whether there's a previous page |

## Iterating Through Items

```python
# Iterate through items on this page
for account in accounts.data:
    print(account.name)

# Or iterate directly on the response
for account in accounts:
    print(account.name)

# Access by index
first_account = accounts[0]  # or accounts.data[0]
```

## Fetching Multiple Pages

```python
# Check for more pages
if accounts.has_next:
    next_page = client.accounts.list(
        page_number=accounts.page_number + 1,
        page_size=50,
    )
```

## Iterating Through All Pages

```python
page_number = 1
all_accounts = []

while True:
    accounts = client.accounts.list(
        page_number=page_number,
        page_size=100
    )
    all_accounts.extend(accounts.data)

    if not accounts.has_next:
        break
    page_number += 1

print(f"Fetched {len(all_accounts)} accounts")
```
