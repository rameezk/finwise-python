"""Account models."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from finwise.models.account_balance import Amount

# Account type - API may return values beyond the documented ones
AccountType = str  # Documented: depository, credit, loan, investment, other

# Account sub-type - API returns various sub-types including custom ones
AccountSubType = str


class AccountCreateRequest(BaseModel):
    """
    Request model for creating an account.

    Attributes:
        name: Account name (1-255 characters).
        type: Account type (depository, credit, loan, investment, other).
        sub_type: Account sub-type for more specific categorization.
        currency: ISO 4217 currency code (default: USD).
        description: Optional account description.
        initial_balance: Optional starting balance.

    Example:
        >>> request = AccountCreateRequest(
        ...     name="Emergency Fund",
        ...     type="depository",
        ...     sub_type="savings",
        ...     currency="USD",
        ... )
    """

    name: str = Field(..., min_length=1, max_length=255, description="Account name")
    type: AccountType = Field(..., description="Account type")
    sub_type: Optional[AccountSubType] = Field(None, alias="subType")
    currency: str = Field(
        default="USD",
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code",
    )
    description: Optional[str] = Field(None, max_length=1000)
    initial_balance: Optional[float] = Field(None, alias="initialBalance")

    model_config = ConfigDict(populate_by_name=True)


class AccountUpdateRequest(BaseModel):
    """
    Request model for updating an account.

    Attributes:
        name: New account name.
        description: New account description.

    Example:
        >>> request = AccountUpdateRequest(name="Renamed Account")
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

    model_config = ConfigDict(populate_by_name=True)


class Account(BaseModel):
    """
    Account response model.

    Attributes:
        id: Unique account identifier.
        user_id: ID of the user who owns this account.
        name: Account name.
        type: Account type (depository, credit, loan, investment, other).
        sub_type: Account sub-type for more specific categorization.
        current_balance: Current balance with currency info.
        available_balance: Available balance (may differ from current for credit).
        created_at: When the account was created.
        updated_at: When the account was last updated.
        archived_at: When the account was archived (None if active).
        logo_base64: Base64 encoded logo image.
        emoji: Emoji associated with the account.
        account_number: Account number (masked or partial).
        original_loan_amount: Original loan amount for loan accounts.
        interest_rate: Interest rate percentage.
        interest_rate_type: Type of interest rate (fixed, variable).
        last_payment_date: Date of the last payment.
        last_payment_amount: Amount of the last payment.
        amount_due: Current amount due.
        minimum_amount_due: Minimum payment due.
        is_linked: Whether the account is linked to a financial institution.
        institution_id: ID of the linked financial institution.
        institution_user_id: User ID at the linked institution.
        data: Additional metadata.

    Example:
        >>> account = client.accounts.retrieve("acc_123")
        >>> print(f"{account.name}: {account.current_balance.format()}")
        >>> if account.is_archived:
        ...     print("This account is archived")
    """

    id: str = Field(..., description="Unique account identifier")
    user_id: str = Field(..., alias="userId", description="User ID")
    name: str = Field(..., description="Account name")
    type: AccountType = Field(..., description="Account type")
    sub_type: AccountSubType = Field(..., alias="subType", description="Account sub-type")
    current_balance: Optional[Amount] = Field(None, alias="currentBalance")
    available_balance: Optional[Amount] = Field(None, alias="availableBalance")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    archived_at: Optional[datetime] = Field(None, alias="archivedAt")

    # Optional fields
    logo_base64: Optional[str] = Field(None, alias="logoBase64")
    emoji: Optional[str] = Field(None)
    account_number: Optional[str] = Field(None, alias="accountNumber")

    # Loan-specific fields
    original_loan_amount: Optional[Amount] = Field(None, alias="originalLoanAmount")
    interest_rate: Optional[float] = Field(None, alias="interestRate")
    interest_rate_type: Optional[str] = Field(None, alias="interestRateType")

    # Payment fields
    last_payment_date: Optional[date] = Field(None, alias="lastPaymentDate")
    last_payment_amount: Optional[Amount] = Field(None, alias="lastPaymentAmount")
    amount_due: Optional[Amount] = Field(None, alias="amountDue")
    minimum_amount_due: Optional[Amount] = Field(None, alias="minimumAmountDue")

    # Institution linking fields
    is_linked: Optional[bool] = Field(None, alias="isLinked")
    institution_id: Optional[str] = Field(None, alias="institutionId")
    institution_user_id: Optional[str] = Field(None, alias="institutionUserId")

    # Additional data
    data: Optional[dict[str, Any]] = Field(None)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def is_archived(self) -> bool:
        """Check if the account is archived."""
        return self.archived_at is not None

    @property
    def balance(self) -> Optional[Decimal]:
        """Get the current balance amount."""
        return self.current_balance.amount if self.current_balance else None

    @property
    def currency(self) -> Optional[str]:
        """Get the currency code."""
        return self.current_balance.currency_code if self.current_balance else None
