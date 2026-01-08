"""Transaction category models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionCategoryCreateRequest(BaseModel):
    """
    Request model for creating a transaction category.

    Attributes:
        name: Category name (1-100 characters).
        color: Optional hex color code (e.g., "#FF5733").
        icon: Optional icon name/identifier.
        parent_id: Optional parent category ID for subcategories.

    Example:
        >>> request = TransactionCategoryCreateRequest(
        ...     name="Groceries",
        ...     color="#4CAF50",
        ...     icon="shopping_cart",
        ... )
    """

    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    parent_id: Optional[str] = Field(None, alias="parentId")

    model_config = ConfigDict(populate_by_name=True)


class TransactionCategory(BaseModel):
    """
    Transaction category response model.

    Attributes:
        id: Unique category identifier.
        name: Category name.
        color: Hex color code (if set).
        icon: Icon name/identifier (if set).
        parent_id: Parent category ID (if this is a subcategory).
        created_at: When the category was created.

    Example:
        >>> categories = client.transaction_categories.list()
        >>> for cat in categories:
        ...     print(f"{cat.name} ({cat.color or 'no color'})")
    """

    id: str
    name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[str] = Field(None, alias="parentId")
    created_at: datetime = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

    @property
    def is_subcategory(self) -> bool:
        """Check if this is a subcategory (has a parent)."""
        return self.parent_id is not None
