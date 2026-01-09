# API Reference

Quick reference for all available methods.

For the official FinWise API documentation, see [finwiseapp.io/docs/api](https://finwiseapp.io/docs/api).

## Client

| Method | Description |
|--------|-------------|
| `FinWise(api_key, ...)` | Create a new client |
| `client.close()` | Close the client |

## Accounts

`client.accounts`

| Method | Description |
|--------|-------------|
| `create(name, type, currency, ...)` | Create a new account |
| `retrieve(account_id)` | Get an account by ID |
| `update(account_id, ...)` | Update an account |
| `list(page_number, page_size)` | List all accounts |
| `archive(account_id)` | Archive an account |

## Transactions

`client.transactions`

| Method | Description |
|--------|-------------|
| `create(account_id, amount, transaction_date, ...)` | Create a transaction |
| `list(account_id, start_date, end_date, type, ...)` | List transactions |
| `aggregated(start_date, end_date, ...)` | Get aggregated summary |
| `archive(transaction_id)` | Archive a transaction |

## Account Balances

`client.account_balances`

| Method | Description |
|--------|-------------|
| `create(account_id, balance, balance_date)` | Create a balance record |
| `list(account_id, ...)` | List balance records |
| `aggregated(as_of_date, ...)` | Get aggregated balance |
| `archive(balance_id)` | Archive a balance record |

## Transaction Categories

`client.transaction_categories`

| Method | Description |
|--------|-------------|
| `create(name, color, icon, parent_id)` | Create a category |
| `list(parent_id, ...)` | List categories |
| `delete(category_id)` | Delete a category |
