"""
FinWise Python SDK (Unofficial).

An unofficial, community-maintained Python client for the FinWise API.
This project is not affiliated with or endorsed by FinWise.

Quick Start:
    >>> from finwise import FinWise
    >>>
    >>> # Initialize the client
    >>> client = FinWise(api_key="your-api-key")
    >>>
    >>> # List accounts
    >>> accounts = client.accounts.list()
    >>> for account in accounts.data:
    ...     print(account.name)
    >>>
    >>> # Create a transaction
    >>> from decimal import Decimal
    >>> from datetime import date
    >>>
    >>> transaction = client.transactions.create(
    ...     account_id="acc_123",
    ...     amount=Decimal("-50.00"),
    ...     transaction_date=date.today(),
    ...     description="Coffee",
    ...     type="expense",
    ... )

Environment Variable:
    You can set your API key via the FINWISE_API_KEY environment variable:

    >>> import os
    >>> os.environ["FINWISE_API_KEY"] = "your-api-key"
    >>> client = FinWise()  # Uses env var automatically

Error Handling:
    >>> from finwise import FinWise, NotFoundError, AuthenticationError
    >>>
    >>> client = FinWise(api_key="your-api-key")
    >>> try:
    ...     account = client.accounts.retrieve("invalid_id")
    ... except NotFoundError as e:
    ...     print(f"Account not found: {e.message}")
    ... except AuthenticationError as e:
    ...     print(f"Invalid API key: {e.message}")

For more information, visit: https://finwiseapp.io/docs/api
"""

from finwise._client import FinWise
from finwise._version import __version__

# Exceptions
from finwise.exceptions import (
    AuthenticationError,
    ConflictError,
    FinWiseAPIError,
    FinWiseConnectionError,
    FinWiseError,
    FinWiseTimeoutError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)

# Models
from finwise.models import (
    Account,
    AccountBalance,
    AccountBalanceCreateRequest,
    AccountCreateRequest,
    AccountUpdateRequest,
    AggregatedBalance,
    AggregatedTransactions,
    Transaction,
    TransactionCategory,
    TransactionCategoryCreateRequest,
    TransactionCreateRequest,
)

# Types
from finwise.types import PaginatedResponse, PaginationParams

__all__ = [
    # Version
    "__version__",
    # Client
    "FinWise",
    # Exceptions
    "FinWiseError",
    "FinWiseAPIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "RateLimitError",
    "ServerError",
    "FinWiseConnectionError",
    "FinWiseTimeoutError",
    # Models - Account
    "Account",
    "AccountCreateRequest",
    "AccountUpdateRequest",
    # Models - Account Balance
    "AccountBalance",
    "AccountBalanceCreateRequest",
    "AggregatedBalance",
    # Models - Transaction
    "Transaction",
    "TransactionCreateRequest",
    "AggregatedTransactions",
    # Models - Transaction Category
    "TransactionCategory",
    "TransactionCategoryCreateRequest",
    # Types
    "PaginatedResponse",
    "PaginationParams",
]
