"""Transactions resource."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from finwise.models.transaction import (
    Transaction,
    TransactionCreateRequest,
)
from finwise.resources._base import BaseResource


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
        category_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        type: Optional[Literal["income", "expense", "transfer"]] = None,
    ) -> list[Transaction]:
        """
        List transactions with optional filtering.

        Note: The API does not support pagination or filtering by account ID.
        All matching transactions are returned.

        Args:
            category_id: Optional filter by category ID.
            start_date: Optional filter for transactions on or after this date.
            end_date: Optional filter for transactions on or before this date.
            type: Optional filter by transaction type.

        Returns:
            List of Transaction objects.

        Example:
            >>> # List all transactions
            >>> transactions = client.transactions.list()
            >>> for txn in transactions:
            ...     print(f"{txn.description}: {txn.amount.format()}")
            >>>
            >>> # Filter by date range
            >>> transactions = client.transactions.list(
            ...     start_date=date(2024, 1, 1),
            ...     end_date=date(2024, 1, 31),
            ... )
            >>>
            >>> # Filter by type
            >>> expenses = client.transactions.list(type="expense")
        """
        params: dict[str, str] = {}

        if category_id:
            params["categoryId"] = category_id
        if start_date:
            params["startDate"] = start_date.isoformat()
        if end_date:
            params["endDate"] = end_date.isoformat()
        if type:
            params["type"] = type

        response = self._transport.get(self._path, params=params or None)

        # API returns raw list
        if isinstance(response, list):
            return [Transaction.model_validate(item) for item in response]

        # Fallback for wrapped response
        return [Transaction.model_validate(item) for item in response.get("data", [])]

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
