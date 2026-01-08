"""Account balance models."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# Balance type literals based on API docs
BalanceType = Literal["manual", "synced"]


class Amount(BaseModel):
    """
    Amount model with value and currency.

    Attributes:
        amount: The numeric value.
        currency_code: The ISO currency code (e.g., "USD", "ZAR").
    """

    amount: Decimal
    currency_code: str = Field(..., alias="currencyCode")

    model_config = ConfigDict(populate_by_name=True)

    def format(self) -> str:
        """Format the amount with currency."""
        return f"{self.currency_code} {self.amount:,.2f}"


class AccountBalanceCreateRequest(BaseModel):
    """
    Request model for creating an account balance record.

    Attributes:
        account_id: ID of the account this balance belongs to.
        amount: Amount with value and currency.
        date: Date of the balance snapshot.

    Example:
        >>> request = AccountBalanceCreateRequest(
        ...     account_id="acc_123",
        ...     amount=Amount(amount=Decimal("5000.00"), currency_code="USD"),
        ...     date=datetime(2024, 1, 15),
        ... )
    """

    account_id: str = Field(..., alias="accountId")
    amount: Amount = Field(..., description="Balance amount")
    date: datetime = Field(..., description="Date of the balance")

    model_config = ConfigDict(populate_by_name=True)


class AccountBalance(BaseModel):
    """
    Account balance response model.

    Represents a point-in-time balance snapshot for an account.

    Attributes:
        id: Unique balance record identifier.
        user_id: ID of the user who owns this balance record.
        account_id: ID of the account this balance belongs to.
        date: Date/time of the balance snapshot.
        type: Balance type (manual or synced).
        amount: Amount with value and currency (nullable).
        created_at: When the record was created.
        updated_at: When the record was last updated.
        archived_at: When the record was archived (None if active).
        data_import_id: ID of the data import that created this record.

    Example:
        >>> balance = client.account_balances.list()[0]
        >>> print(f"{balance.amount.format()} on {balance.date}")
    """

    id: str = Field(..., description="Unique balance record identifier")
    user_id: str = Field(..., alias="userId", description="User ID")
    account_id: Optional[str] = Field(None, alias="accountId", description="Account ID")
    date: datetime = Field(..., description="Balance date/time")
    type: BalanceType = Field(..., description="Balance type (manual or synced)")
    amount: Optional[Amount] = Field(None, description="Balance amount")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    archived_at: Optional[datetime] = Field(None, alias="archivedAt")
    data_import_id: Optional[str] = Field(None, alias="dataImportId")

    model_config = ConfigDict(populate_by_name=True)

    @property
    def balance(self) -> Optional[Decimal]:
        """Get the balance value."""
        return self.amount.amount if self.amount else None

    @property
    def currency(self) -> Optional[str]:
        """Get the currency code."""
        return self.amount.currency_code if self.amount else None

    @property
    def is_archived(self) -> bool:
        """Check if the balance record is archived."""
        return self.archived_at is not None


class AggregatedBalance(BaseModel):
    """
    Aggregated balance response model.

    Provides a summary of balances across accounts.

    Attributes:
        total_balance: Sum of all account balances.
        currency: Currency of the aggregated balance.
        as_of_date: Date of the aggregation.
        account_count: Number of accounts included.

    Example:
        >>> summary = client.account_balances.aggregated()
        >>> print(f"Total: {summary.currency} {summary.total_balance}")
        >>> print(f"Across {summary.account_count} accounts")
    """

    total_balance: Decimal = Field(..., alias="totalBalance")
    currency: str
    as_of_date: date = Field(..., alias="asOfDate")
    account_count: int = Field(..., alias="accountCount")

    model_config = ConfigDict(populate_by_name=True)
