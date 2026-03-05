"""Transaction models."""

from __future__ import annotations

import datetime as dt
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from finwise.models.account_balance import Amount


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
        user_id: ID of the user who owns this transaction.
        account_id: ID of the account (nullable).
        amount: Transaction amount with currency.
        date: Date/time of the transaction.
        description: Transaction description (if set).
        category_id: Category ID (if categorized).
        type: Transaction type.
        created_at: When the transaction was created.
        updated_at: When the transaction was last updated.
        archived_at: When the transaction was archived (None if active).
        data_import_id: ID of the data import that created this record.

    Example:
        >>> transactions = client.transactions.list()
        >>> for txn in transactions:
        ...     print(f"{txn.date}: {txn.description} ({txn.amount.format()})")
    """

    id: str
    user_id: str = Field(..., alias="userId")
    account_id: Optional[str] = Field(None, alias="accountId")
    amount: Amount
    date: datetime
    description: Optional[str] = None
    category_id: Optional[str] = Field(None, alias="categoryId")
    type: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    archived_at: Optional[datetime] = Field(None, alias="archivedAt")
    data_import_id: Optional[str] = Field(None, alias="dataImportId")

    model_config = ConfigDict(populate_by_name=True)

    @property
    def value(self) -> Decimal:
        """Get the transaction amount value."""
        return self.amount.amount

    @property
    def currency(self) -> str:
        """Get the currency code."""
        return self.amount.currency_code

    @property
    def transaction_date(self) -> dt.date:
        """Get the transaction date (for backwards compatibility)."""
        return self.date.date()

    @property
    def is_archived(self) -> bool:
        """Check if the transaction is archived."""
        return self.archived_at is not None

    @property
    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        return self.type == "income" if self.type else False

    @property
    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        return self.type == "expense" if self.type else False


class AggregatedTransaction(BaseModel):
    """
    Aggregated transaction total for a category/type combination.

    Represents the sum of transactions for a specific category and transaction type.

    Attributes:
        amount: Total amount for this category/type combination.
        category_id: Transaction category ID (if aggregated by category).
        transaction_type: Transaction type (e.g., "debit", "credit").

    Example:
        >>> aggregated = client.transactions.aggregated(currency_code="ZAR")
        >>> for item in aggregated:
        ...     print(f"Category {item.category_id}: {item.amount} ({item.transaction_type})")
    """

    amount: Decimal
    category_id: Optional[str] = Field(None, alias="transactionCategoryId")
    transaction_type: Optional[str] = Field(None, alias="transactionType")

    model_config = ConfigDict(populate_by_name=True)
