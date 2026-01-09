# Accounts

Manage financial accounts (checking, savings, credit cards, etc.).

## Create an Account

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

account = client.accounts.create(
    name="Savings Account",
    type="savings",
    currency="USD",
    description="Emergency fund",
    initial_balance=10000.00,
)
print(f"Created: {account.id}")
```

### Account Types

| Type | Description |
|------|-------------|
| `checking` | Checking/current account |
| `savings` | Savings account |
| `credit` | Credit card |
| `investment` | Investment/brokerage account |
| `loan` | Loan account |
| `other` | Other account type |

## Retrieve an Account

```python
account = client.accounts.retrieve("acc_123")
print(f"{account.name}: {account.balance}")
```

## Update an Account

```python
account = client.accounts.update(
    "acc_123",
    name="Renamed Account",
    description="Updated description",
)
```

## List Accounts

```python
# Basic listing
accounts = client.accounts.list()
for account in accounts.data:
    print(f"  - {account.name}")

# With pagination
accounts = client.accounts.list(page_number=1, page_size=50)
print(f"Total accounts: {accounts.total_count}")

if accounts.has_next:
    next_page = client.accounts.list(page_number=2, page_size=50)
```

## Archive an Account

```python
archived = client.accounts.archive("acc_123")
print(f"Archived at: {archived.archived_at}")
```

!!! note
    Archiving is a soft delete. The account data is preserved but hidden from normal listings.
