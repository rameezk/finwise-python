"""Account balances resource."""

from __future__ import annotations

import builtins
from datetime import date, datetime
from decimal import Decimal

from finwise.models.account_balance import (
    AccountBalance,
    AccountBalanceCreateRequest,
    AggregatedBalance,
    Amount,
)
from finwise.resources._base import BaseResource
from finwise.types.pagination import (
    PaginatedResponse,
    PaginationInfo,
    build_list_params,
)


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
        page_number: int = 1,
        page_size: int = 100,
    ) -> PaginatedResponse[AccountBalance]:
        """
        List account balance records with pagination.

        Args:
            page_number: Page number to retrieve (default: 1).
            page_size: Number of items per page (default: 100).

        Returns:
            Paginated response containing AccountBalance objects.

        Example:
            >>> balances = client.account_balances.list()
            >>> for balance in balances:
            ...     if balance.amount:
            ...         print(f"{balance.date}: {balance.amount.format()}")
        """
        params = build_list_params(page_number, page_size)
        response = self._transport.get(self._path, params=params, include_headers=True)

        items = response.body if isinstance(response.body, list) else []
        balances = [AccountBalance.model_validate(item) for item in items]
        pagination = PaginationInfo.from_headers(response.headers)

        return PaginatedResponse[AccountBalance](
            data=balances,
            page_number=pagination.page_number,
            page_size=pagination.page_size,
            total_count=pagination.total_count,
            total_pages=pagination.total_pages,
            has_next=pagination.has_next,
            has_previous=pagination.has_previous,
        )

    def aggregated(
        self,
        *,
        currency: str,
    ) -> builtins.list[AggregatedBalance]:
        """
        Get aggregated balance history for a specific currency.

        Returns a time series of balance snapshots, useful for
        tracking net worth over time.

        Args:
            currency: Currency code to aggregate (e.g., "USD", "ZAR").
                     This parameter is required.

        Returns:
            List of AggregatedBalance snapshots sorted by date.

        Example:
            >>> snapshots = client.account_balances.aggregated(currency="ZAR")
            >>> for snapshot in snapshots:
            ...     print(f"{snapshot.date}: {snapshot.amount.format()}")
        """
        params: dict[str, str] = {"currencyCode": currency}

        response = self._transport.get(f"{self._path}/aggregated", params=params)

        if isinstance(response, list):
            return [AggregatedBalance.model_validate(item) for item in response]

        return []

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
