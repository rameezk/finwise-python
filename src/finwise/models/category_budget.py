"""Category budget models."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AggregatedCategoryBudget(BaseModel):
    """
    Aggregated category budget total.

    Represents the budget amount for a specific category and transaction type.

    Attributes:
        amount: Budget amount for this category/type combination.
        category_id: Transaction category ID (if aggregated by category).
        transaction_type: Transaction type (e.g., "debit", "credit").

    Example:
        >>> budgets = client.category_budgets.aggregated(currency_code="ZAR")
        >>> for item in budgets:
        ...     print(f"Category {item.category_id}: {item.amount} ({item.transaction_type})")
    """

    amount: Decimal
    category_id: Optional[str] = Field(None, alias="transactionCategoryId")
    transaction_type: Optional[str] = Field(None, alias="transactionType")

    model_config = ConfigDict(populate_by_name=True)
