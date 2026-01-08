"""Account balances resource."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from finwise.models.account_balance import (
    AccountBalance,
    AccountBalanceCreateRequest,
    AggregatedBalance,
    Amount,
)
from finwise.resources._base import BaseResource


class AccountBalancesResource(BaseResource):
    """
    Account Balances API resource.

    Provides methods for managing account balance records and retrieving
    aggregated balance information.

    Example:
        >>> client = FinWise(api_key="your-key")
        >>>
        >>> # Create a balance record
        >>> balance = client.account_balances.create(
        ...     account_id="acc_123",
        ...     balance=Decimal("5000.00"),
        ...     balance_date=date(2024, 1, 15),
        ... )
        >>>
        >>> # List balance records
        >>> balances = client.account_balances.list()
        >>>
        >>> # Get aggregated balance
        >>> summary = client.account_balances.aggregated()
        >>> print(f"Total: {summary.total_balance}")
    """

    _path = "/account-balances"

    def create(
        self,
        account_id: str,
        balance: Decimal,
        balance_date: date,
        currency: str = "USD",
    ) -> AccountBalance:
        """
        Create a new account balance record.

        Balance records capture point-in-time snapshots of account balances,
        useful for tracking balance history over time.

        Args:
            account_id: ID of the account this balance belongs to.
            balance: Balance amount at the snapshot time.
            balance_date: Date of the balance snapshot.
            currency: ISO 4217 currency code (default: "USD").

        Returns:
            The created AccountBalance object.

        Raises:
            ValidationError: If the request data is invalid.
            NotFoundError: If the account doesn't exist.

        Example:
            >>> from decimal import Decimal
            >>> from datetime import date
            >>>
            >>> balance = client.account_balances.create(
            ...     account_id="acc_123",
            ...     balance=Decimal("5000.00"),
            ...     balance_date=date(2024, 1, 15),
            ... )
        """
        request = AccountBalanceCreateRequest(
            account_id=account_id,
            amount=Amount(amount=balance, currency_code=currency),
            date=datetime.combine(balance_date, datetime.min.time()),
        )

        response = self._transport.post(
            self._path,
            json=request.model_dump(by_alias=True, mode="json"),
        )

        return AccountBalance.model_validate(response)

    def list(
        self,
        *,
        account_id: Optional[str] = None,
    ) -> list[AccountBalance]:
        """
        List account balance records.

        Args:
            account_id: Optional filter by account ID.

        Returns:
            List of AccountBalance objects.

        Example:
            >>> # List all balance records
            >>> balances = client.account_balances.list()
            >>>
            >>> # Filter by account
            >>> balances = client.account_balances.list(account_id="acc_123")
        """
        params: dict[str, str] = {}
        if account_id:
            params["accountId"] = account_id

        response = self._transport.get(self._path, params=params or None)

        # API returns raw list
        if isinstance(response, list):
            return [AccountBalance.model_validate(item) for item in response]

        # Fallback for paginated response
        return [
            AccountBalance.model_validate(item) for item in response.get("data", [])
        ]

    def aggregated(
        self,
        *,
        as_of_date: Optional[date] = None,
        currency: Optional[str] = None,
    ) -> AggregatedBalance:
        """
        Get aggregated balance across all accounts.

        Provides a summary of total balances, useful for dashboards
        and financial overviews.

        Args:
            as_of_date: Optional date for the aggregation (default: today).
            currency: Optional currency filter (default: all currencies).

        Returns:
            AggregatedBalance with total balance information.

        Example:
            >>> summary = client.account_balances.aggregated()
            >>> print(f"Total balance: {summary.currency} {summary.total_balance}")
            >>> print(f"Across {summary.account_count} accounts")
        """
        params: dict[str, str] = {}
        if as_of_date:
            params["asOfDate"] = as_of_date.isoformat()
        if currency:
            params["currency"] = currency

        response = self._transport.get(
            f"{self._path}/aggregated", params=params or None
        )

        return AggregatedBalance.model_validate(response)

    def archive(self, balance_id: str) -> AccountBalance:
        """
        Archive an account balance record.

        Args:
            balance_id: The unique balance record identifier.

        Returns:
            The archived AccountBalance object.

        Raises:
            NotFoundError: If the balance record doesn't exist.

        Example:
            >>> archived = client.account_balances.archive("bal_123")
        """
        response = self._transport.post(f"{self._path}/{balance_id}/archive")
        return AccountBalance.model_validate(response)
