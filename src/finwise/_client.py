"""Main FinWise client for the SDK."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional

from finwise._config import ClientConfig
from finwise._http import HTTPTransport
from finwise.resources.account_balances import AccountBalancesResource
from finwise.resources.accounts import AccountsResource
from finwise.resources.transaction_categories import TransactionCategoriesResource
from finwise.resources.transactions import TransactionsResource

if TYPE_CHECKING:
    from httpx import Client as HttpxClient


class FinWise:
    """
    FinWise API client.

    The main entry point for interacting with the FinWise API. Provides access
    to all API resources through a simple, intuitive interface.

    Args:
        api_key: Your FinWise API key. If not provided, reads from the
                 FINWISE_API_KEY environment variable.
        base_url: Override the default API base URL.
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum number of retries for failed requests (default: 3).
        http_client: Optional custom httpx.Client instance for advanced use cases.

    Raises:
        ValueError: If no API key is provided and FINWISE_API_KEY is not set.

    Example:
        >>> from finwise import FinWise
        >>>
        >>> # Initialize with API key
        >>> client = FinWise(api_key="your-api-key")
        >>>
        >>> # Or use environment variable
        >>> # export FINWISE_API_KEY="your-api-key"
        >>> client = FinWise()
        >>>
        >>> # Use as context manager for automatic cleanup
        >>> with FinWise(api_key="your-api-key") as client:
        ...     accounts = client.accounts.list()

    Attributes:
        accounts: Access the Accounts API resource.
        account_balances: Access the Account Balances API resource.
        transactions: Access the Transactions API resource.
        transaction_categories: Access the Transaction Categories API resource.
    """

    accounts: AccountsResource
    """Accounts API resource for managing financial accounts."""

    account_balances: AccountBalancesResource
    """Account Balances API resource for balance records and aggregations."""

    transactions: TransactionsResource
    """Transactions API resource for managing financial transactions."""

    transaction_categories: TransactionCategoriesResource
    """Transaction Categories API resource for organizing transactions."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = "https://api.finwiseapp.io",
        timeout: float = 30.0,
        max_retries: int = 3,
        http_client: Optional[HttpxClient] = None,
    ) -> None:
        """Initialize the FinWise client."""
        resolved_api_key = api_key or os.environ.get("FINWISE_API_KEY")
        if not resolved_api_key:
            raise ValueError(
                "API key must be provided either as an argument or via the "
                "FINWISE_API_KEY environment variable. "
                "Get your API key at: https://finwiseapp.io/settings/api-keys"
            )

        self._config = ClientConfig(
            api_key=resolved_api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self._transport = HTTPTransport(
            config=self._config,
            http_client=http_client,
        )

        # Initialize API resources
        self.accounts = AccountsResource(self._transport)
        self.account_balances = AccountBalancesResource(self._transport)
        self.transactions = TransactionsResource(self._transport)
        self.transaction_categories = TransactionCategoriesResource(self._transport)

    def __enter__(self) -> FinWise:
        """Enter context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Exit context manager and close the client."""
        self.close()

    def __repr__(self) -> str:
        """Return string representation."""
        return f"FinWise(base_url={self._config.base_url!r})"

    def close(self) -> None:
        """
        Close the underlying HTTP client.

        This releases any resources held by the client. After calling close(),
        the client should not be used for further API requests.

        Example:
            >>> client = FinWise(api_key="your-key")
            >>> try:
            ...     accounts = client.accounts.list()
            ... finally:
            ...     client.close()
        """
        self._transport.close()
