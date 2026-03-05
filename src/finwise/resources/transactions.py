"""Transactions resource."""

from __future__ import annotations

import builtins
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from finwise.models.transaction import (
    AggregatedTransaction,
    Transaction,
    TransactionCreateRequest,
)
from finwise.resources._base import BaseResource
from finwise.types.pagination import (
    PaginatedResponse,
    PaginationInfo,
    build_list_params,
)


class TransactionsResource(BaseResource):
    """
    Transactions API resource.

    Provides methods for managing financial transactions in FinWise.

    Example:
        >>> client = FinWise(api_key="your-key")
        >>>
        >>> # Create a transaction
        >>> txn = client.transactions.create(
        ...     account_id="acc_123",
        ...     amount=Decimal("-50.00"),
        ...     transaction_date=date(2024, 1, 15),
        ...     description="Grocery shopping",
        ...     type="expense",
        ... )
        >>>
        >>> # List transactions
        >>> transactions = client.transactions.list()
        >>> for txn in transactions:
        ...     print(f"{txn.description}: {txn.amount}")
    """

    _path = "/transactions"

    def create(
        self,
        account_id: str,
        amount: Decimal,
        transaction_date: date,
        *,
        description: Optional[str] = None,
        category_id: Optional[str] = None,
        type: Literal["income", "expense", "transfer"] = "expense",
    ) -> Transaction:
        """
        Create a new transaction.

        Args:
            account_id: ID of the account for this transaction.
            amount: Transaction amount. Use negative values for expenses,
                   positive for income.
            transaction_date: Date of the transaction.
            description: Optional transaction description (max 500 characters).
            category_id: Optional category ID for categorization.
            type: Transaction type (default: "expense").

        Returns:
            The created Transaction object.

        Raises:
            ValidationError: If the request data is invalid.
            NotFoundError: If the account or category doesn't exist.

        Example:
            >>> from decimal import Decimal
            >>> from datetime import date
            >>>
            >>> # Create an expense
            >>> expense = client.transactions.create(
            ...     account_id="acc_123",
            ...     amount=Decimal("-50.00"),
            ...     transaction_date=date(2024, 1, 15),
            ...     description="Grocery shopping",
            ...     category_id="cat_groceries",
            ...     type="expense",
            ... )
            >>>
            >>> # Create income
            >>> income = client.transactions.create(
            ...     account_id="acc_123",
            ...     amount=Decimal("3000.00"),
            ...     transaction_date=date(2024, 1, 1),
            ...     description="Monthly salary",
            ...     type="income",
            ... )
        """
        request = TransactionCreateRequest(
            account_id=account_id,
            amount=amount,
            transaction_date=transaction_date,
            description=description,
            category_id=category_id,
            type=type,
        )

        response = self._transport.post(
            self._path,
            json=request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )

        return Transaction.model_validate(response)

    def list(
        self,
        *,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        transaction_types: Optional[list[str]] = None,
        category_ids: Optional[list[str]] = None,
        exclude_archived: bool = True,
        exclude_transfers: bool = False,
        exclude_excluded_transactions: bool = True,
        exclude_parent_transactions: bool = True,
        page_number: int = 1,
        page_size: int = 100,
    ) -> PaginatedResponse[Transaction]:
        """
        List transactions with filtering and pagination.

        Args:
            from_date: Filter transactions from this date/time.
            to_date: Filter transactions up to this date/time.
            transaction_types: Filter by transaction types (e.g., ["debit", "credit"]).
            category_ids: Filter by category IDs.
            exclude_archived: Exclude archived transactions (default: True).
            exclude_transfers: Exclude transfer transactions (default: False).
            exclude_excluded_transactions: Exclude manually excluded transactions (default: True).
            exclude_parent_transactions: Exclude parent/split transactions (default: True).
            page_number: Page number to retrieve (default: 1).
            page_size: Number of items per page (default: 100).

        Returns:
            Paginated response containing Transaction objects.

        Example:
            >>> # List all transactions
            >>> transactions = client.transactions.list()
            >>> for txn in transactions:
            ...     print(f"{txn.description}: {txn.amount.format()}")
            >>>
            >>> # Filter by date range
            >>> from datetime import datetime
            >>> transactions = client.transactions.list(
            ...     from_date=datetime(2024, 1, 1),
            ...     to_date=datetime(2024, 1, 31, 23, 59, 59),
            ... )
            >>>
            >>> # Filter by type
            >>> debits = client.transactions.list(transaction_types=["debit"])
            >>>
            >>> # Pagination
            >>> page1 = client.transactions.list(page_size=50)
            >>> if page1.has_next:
            ...     page2 = client.transactions.list(page_number=2, page_size=50)
        """
        filters: dict[str, object] = {
            "excludeArchived": exclude_archived,
            "excludeTransfers": exclude_transfers,
            "excludeExcludedTransactions": exclude_excluded_transactions,
            "excludeParentTransactions": exclude_parent_transactions,
        }
        if from_date:
            filters["fromDate"] = from_date.isoformat() + "Z"
        if to_date:
            filters["toDate"] = to_date.isoformat() + "Z"
        if transaction_types:
            filters["transactionTypes"] = transaction_types
        if category_ids:
            filters["transactionCategoryIds"] = category_ids

        params = build_list_params(page_number, page_size, filters)
        response = self._transport.get(self._path, params=params, include_headers=True)

        items = response.body if isinstance(response.body, list) else []
        transactions = [Transaction.model_validate(item) for item in items]
        pagination = PaginationInfo.from_headers(response.headers)

        return PaginatedResponse[Transaction](
            data=transactions,
            page_number=pagination.page_number,
            page_size=pagination.page_size,
            total_count=pagination.total_count,
            total_pages=pagination.total_pages,
            has_next=pagination.has_next,
            has_previous=pagination.has_previous,
        )

    def archive(self, transaction_id: str) -> Transaction:
        """
        Archive a transaction.

        Archived transactions are soft-deleted and won't appear in
        active transaction lists.

        Args:
            transaction_id: The unique transaction identifier.

        Returns:
            The archived Transaction object.

        Raises:
            NotFoundError: If the transaction doesn't exist.

        Example:
            >>> archived = client.transactions.archive("txn_123")
            >>> assert archived.is_archived
        """
        response = self._transport.post(f"{self._path}/{transaction_id}/archive")
        return Transaction.model_validate(response)

    def aggregated(
        self,
        *,
        currency_code: str,
        time_zone: str = "UTC",
        aggregate_by: Optional[builtins.list[str]] = None,
        budget_start_date: int = 1,
        to_date: Optional[datetime] = None,
        exclude_archived: bool = True,
        exclude_transfers: bool = True,
        exclude_excluded_transactions: bool = True,
        exclude_parent_transactions: bool = True,
    ) -> builtins.list[AggregatedTransaction]:
        """
        Get aggregated transaction totals by category and/or type.

        Args:
            currency_code: Currency code for aggregation (e.g., "ZAR", "USD").
            time_zone: Time zone for date calculations (default: "UTC").
            aggregate_by: Fields to aggregate by (default: ["transactionCategoryId", "transactionType"]).
            budget_start_date: Day of month when budget period starts (default: 1).
            to_date: End date for aggregation period.
            exclude_archived: Exclude archived transactions (default: True).
            exclude_transfers: Exclude transfer transactions (default: True).
            exclude_excluded_transactions: Exclude manually excluded transactions (default: True).
            exclude_parent_transactions: Exclude parent/split transactions (default: True).

        Returns:
            List of aggregated transaction totals.

        Example:
            >>> # Get spending by category for the current period
            >>> aggregated = client.transactions.aggregated(
            ...     currency_code="ZAR",
            ...     time_zone="Africa/Johannesburg",
            ... )
            >>> for item in aggregated:
            ...     print(f"Category {item.category_id}: {item.amount} ({item.transaction_type})")
        """
        if aggregate_by is None:
            aggregate_by = ["transactionCategoryId", "transactionType"]

        filters: dict[str, object] = {
            "excludeArchived": exclude_archived,
            "excludeTransfers": exclude_transfers,
            "excludeExcludedTransactions": exclude_excluded_transactions,
            "excludeParentTransactions": exclude_parent_transactions,
            "fromDateForCategoryIds": {},
        }
        if to_date:
            filters["toDate"] = to_date.isoformat() + "Z"

        body = {
            "filters": filters,
            "currencyCode": currency_code,
            "timeZone": time_zone,
            "aggregateBy": aggregate_by,
            "budgetStartDate": budget_start_date,
        }

        response = self._transport.post(f"{self._path}/aggregated3", json=body)

        items = response if isinstance(response, list) else []
        return [AggregatedTransaction.model_validate(item) for item in items]
