"""Accounts resource."""

from __future__ import annotations

from typing import Optional

from finwise.models.account import (
    Account,
    AccountCreateRequest,
    AccountSubType,
    AccountType,
    AccountUpdateRequest,
)
from finwise.resources._base import BaseResource


class AccountsResource(BaseResource):
    """
    Accounts API resource.

    Provides methods for managing financial accounts in FinWise.

    Example:
        >>> client = FinWise(api_key="your-key")
        >>>
        >>> # Create an account
        >>> account = client.accounts.create(
        ...     name="Savings Account",
        ...     type="depository",
        ...     sub_type="savings",
        ...     currency="USD",
        ... )
        >>>
        >>> # List all accounts
        >>> accounts = client.accounts.list()
        >>> for account in accounts:
        ...     print(account.name)
        >>>
        >>> # Get a specific account
        >>> account = client.accounts.retrieve("acc_123")
        >>>
        >>> # Update an account
        >>> account = client.accounts.update("acc_123", name="New Name")
        >>>
        >>> # Archive an account
        >>> client.accounts.archive("acc_123")
    """

    _path = "/accounts"

    def create(
        self,
        name: str,
        type: AccountType,
        *,
        sub_type: Optional[AccountSubType] = None,
        currency: str = "USD",
        description: Optional[str] = None,
        initial_balance: Optional[float] = None,
    ) -> Account:
        """
        Create a new account.

        Args:
            name: Account name (1-255 characters).
            type: Account type (depository, credit, loan, investment, other).
            sub_type: Account sub-type for more specific categorization.
            currency: ISO 4217 currency code (default: "USD").
            description: Optional account description (max 1000 characters).
            initial_balance: Optional initial balance amount.

        Returns:
            The created Account object.

        Raises:
            ValidationError: If the request data is invalid.
            AuthenticationError: If the API key is invalid.

        Example:
            >>> account = client.accounts.create(
            ...     name="Emergency Fund",
            ...     type="depository",
            ...     sub_type="savings",
            ...     currency="USD",
            ...     description="6 month emergency fund",
            ...     initial_balance=10000.00,
            ... )
            >>> print(f"Created account: {account.id}")
        """
        request = AccountCreateRequest(
            name=name,
            type=type,
            sub_type=sub_type,
            currency=currency,
            description=description,
            initial_balance=initial_balance,
        )

        response = self._transport.post(
            self._path,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )

        return Account.model_validate(response)

    def retrieve(self, account_id: str) -> Account:
        """
        Retrieve a specific account by ID.

        Args:
            account_id: The unique account identifier.

        Returns:
            The Account object.

        Raises:
            NotFoundError: If the account doesn't exist.
            AuthenticationError: If the API key is invalid.

        Example:
            >>> account = client.accounts.retrieve("acc_123")
            >>> print(f"{account.name}: {account.balance} {account.currency}")
        """
        response = self._transport.get(f"{self._path}/{account_id}")
        return Account.model_validate(response)

    def update(
        self,
        account_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Account:
        """
        Update an existing account.

        Args:
            account_id: The unique account identifier.
            name: New account name (1-255 characters).
            description: New account description (max 1000 characters).

        Returns:
            The updated Account object.

        Raises:
            NotFoundError: If the account doesn't exist.
            ValidationError: If the update data is invalid.

        Example:
            >>> account = client.accounts.update(
            ...     "acc_123",
            ...     name="Renamed Account",
            ...     description="Updated description",
            ... )
        """
        request = AccountUpdateRequest(name=name, description=description)

        response = self._transport.patch(
            f"{self._path}/{account_id}",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )

        return Account.model_validate(response)

    def list(self) -> list[Account]:
        """
        List all accounts.

        Returns:
            List of Account objects.

        Raises:
            AuthenticationError: If the API key is invalid.

        Example:
            >>> accounts = client.accounts.list()
            >>> for account in accounts:
            ...     print(f"{account.name}: {account.balance}")
        """
        response = self._transport.get(self._path)

        # API returns raw list
        if isinstance(response, list):
            return [Account.model_validate(item) for item in response]

        # Fallback for paginated response
        return [Account.model_validate(item) for item in response.get("data", [])]

    def archive(self, account_id: str) -> Account:
        """
        Archive an account.

        Archived accounts are soft-deleted and can potentially be restored.
        The account will no longer appear in active account lists.

        Args:
            account_id: The unique account identifier.

        Returns:
            The archived Account object (with archived_at set).

        Raises:
            NotFoundError: If the account doesn't exist.

        Example:
            >>> archived = client.accounts.archive("acc_123")
            >>> print(f"Archived at: {archived.archived_at}")
            >>> assert archived.is_archived
        """
        response = self._transport.post(f"{self._path}/{account_id}/archive")
        return Account.model_validate(response)
