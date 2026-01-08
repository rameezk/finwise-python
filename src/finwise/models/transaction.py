"""Transaction models."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreateRequest(BaseModel):
    """
    Request model for creating a transaction.

    Attributes:
        account_id: ID of the account for this transaction.
        amount: Transaction amount (positive for income, negative for expense).
        transaction_date: Date of the transaction.
        description: Optional transaction description.
        category_id: Optional category ID for categorization.
        type: Transaction type (income, expense, or transfer).

    Example:
        >>> request = TransactionCreateRequest(
        ...     account_id="acc_123",
        ...     amount=Decimal("-50.00"),
        ...     transaction_date=date(2024, 1, 15),
        ...     description="Grocery shopping",
        ...     type="expense",
        ... )
    """

    account_id: str = Field(..., alias="accountId")
    amount: Decimal = Field(
        ...,
        description="Transaction amount (positive for income, negative for expense)",
    )
    transaction_date: date = Field(..., alias="transactionDate")
    description: Optional[str] = Field(None, max_length=500)
    category_id: Optional[str] = Field(None, alias="categoryId")
    type: Literal["income", "expense", "transfer"] = "expense"

    model_config = ConfigDict(populate_by_name=True)


class Transaction(BaseModel):
    """
    Transaction response model.

    Attributes:
        id: Unique transaction identifier.
        account_id: ID of the account.
        amount: Transaction amount.
        transaction_date: Date of the transaction.
        description: Transaction description (if set).
        category_id: Category ID (if categorized).
        category_name: Category name (if categorized).
        type: Transaction type.
        created_at: When the transaction was created.
        updated_at: When the transaction was last updated.
        archived_at: When the transaction was archived (None if active).

    Example:
        >>> transactions = client.transactions.list()
        >>> for txn in transactions:
        ...     print(f"{txn.transaction_date}: {txn.description} ({txn.amount})")
    """

    id: str
    account_id: str = Field(..., alias="accountId")
    amount: Decimal
    transaction_date: date = Field(..., alias="transactionDate")
    description: Optional[str] = None
    category_id: Optional[str] = Field(None, alias="categoryId")
    category_name: Optional[str] = Field(None, alias="categoryName")
    type: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    archived_at: Optional[datetime] = Field(None, alias="archivedAt")

    model_config = ConfigDict(populate_by_name=True)

    @property
    def is_archived(self) -> bool:
        """Check if the transaction is archived."""
        return self.archived_at is not None

    @property
    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        return self.type == "income"

    @property
    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        return self.type == "expense"


class AggregatedTransactions(BaseModel):
    """
    Aggregated transactions response model.

    Provides a summary of transactions over a period.

    Attributes:
        total_income: Sum of all income transactions.
        total_expenses: Sum of all expense transactions (as positive number).
        net_amount: Net amount (income - expenses).
        transaction_count: Number of transactions in the period.
        start_date: Start date of the aggregation period.
        end_date: End date of the aggregation period.

    Example:
        >>> summary = client.transactions.aggregated(
        ...     start_date=date(2024, 1, 1),
        ...     end_date=date(2024, 1, 31),
        ... )
        >>> print(f"Income: {summary.total_income}")
        >>> print(f"Expenses: {summary.total_expenses}")
        >>> print(f"Net: {summary.net_amount}")
    """

    total_income: Decimal = Field(..., alias="totalIncome")
    total_expenses: Decimal = Field(..., alias="totalExpenses")
    net_amount: Decimal = Field(..., alias="netAmount")
    transaction_count: int = Field(..., alias="transactionCount")
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")

    model_config = ConfigDict(populate_by_name=True)
