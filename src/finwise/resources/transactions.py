"""Transactions resource."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from finwise.models.transaction import (
    AggregatedTransactions,
    Transaction,
    TransactionCreateRequest,
)
from finwise.resources._base import BaseResource
from finwise.types.pagination import PaginatedResponse


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
        >>>
        >>> # Get aggregated summary
        >>> summary = client.transactions.aggregated(
        ...     start_date=date(2024, 1, 1),
        ...     end_date=date(2024, 1, 31),
        ... )
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
        account_id: Optional[str] = None,
        category_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        type: Optional[Literal["income", "expense", "transfer"]] = None,
        page_number: int = 1,
        page_size: int = 100,
    ) -> PaginatedResponse[Transaction]:
        """
        List transactions with pagination and filtering.

        Args:
            account_id: Optional filter by account ID.
            category_id: Optional filter by category ID.
            start_date: Optional filter for transactions on or after this date.
            end_date: Optional filter for transactions on or before this date.
            type: Optional filter by transaction type.
            page_number: Page number to retrieve (default: 1).
            page_size: Number of items per page (default: 100, max: 500).

        Returns:
            Paginated response containing Transaction objects.

        Example:
            >>> # List all transactions
            >>> transactions = client.transactions.list()
            >>>
            >>> # Filter by date range
            >>> transactions = client.transactions.list(
            ...     start_date=date(2024, 1, 1),
            ...     end_date=date(2024, 1, 31),
            ... )
            >>>
            >>> # Filter by account and type
            >>> expenses = client.transactions.list(
            ...     account_id="acc_123",
            ...     type="expense",
            ... )
        """
        params = self._build_pagination_params(page_number, page_size)

        if account_id:
            params["accountId"] = account_id
        if category_id:
            params["categoryId"] = category_id
        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
        if type:
            params["type"] = type

        response = self._transport.get(self._path, params=params)

        transactions = [
            Transaction.model_validate(item) for item in response.get("data", [])
        ]

        return PaginatedResponse[Transaction](
            data=transactions,
            page_number=response.get("pageNumber", page_number),
            page_size=response.get("pageSize", page_size),
            total_count=response.get("totalCount", len(transactions)),
            total_pages=response.get("totalPages", 1),
            has_next=response.get("hasNext", False),
            has_previous=response.get("hasPrevious", False),
        )

    def aggregated(
        self,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[str] = None,
        category_id: Optional[str] = None,
    ) -> AggregatedTransactions:
        """
        Get aggregated transaction summary.

        Provides a summary of income, expenses, and net amount over
        a specified period.

        Args:
            start_date: Start date for aggregation (default: first of month).
            end_date: End date for aggregation (default: today).
            account_id: Optional filter by account ID.
            category_id: Optional filter by category ID.

        Returns:
            AggregatedTransactions with income/expense summary.

        Example:
            >>> from datetime import date
            >>>
            >>> # Get monthly summary
            >>> summary = client.transactions.aggregated(
            ...     start_date=date(2024, 1, 1),
            ...     end_date=date(2024, 1, 31),
            ... )
            >>> print(f"Income: {summary.total_income}")
            >>> print(f"Expenses: {summary.total_expenses}")
            >>> print(f"Net: {summary.net_amount}")
            >>> print(f"Transactions: {summary.transaction_count}")
        """
        params: dict[str, str] = {}

        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
        if account_id:
            params["accountId"] = account_id
        if category_id:
            params["categoryId"] = category_id

        response = self._transport.get(
            f"{self._path}/aggregated", params=params or None
        )

        return AggregatedTransactions.model_validate(response)

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
