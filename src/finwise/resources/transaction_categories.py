"""Transaction categories resource."""

from __future__ import annotations

from typing import Optional

from finwise.models.transaction_category import (
    TransactionCategory,
    TransactionCategoryCreateRequest,
)
from finwise.resources._base import BaseResource


class TransactionCategoriesResource(BaseResource):
    """
    Transaction Categories API resource.

    Provides methods for managing transaction categories in FinWise.
    Categories help organize transactions for budgeting and reporting.

    Example:
        >>> client = FinWise(api_key="your-key")
        >>>
        >>> # Create a category
        >>> category = client.transaction_categories.create(
        ...     name="Groceries",
        ...     color="#4CAF50",
        ...     icon="shopping_cart",
        ... )
        >>>
        >>> # List categories
        >>> categories = client.transaction_categories.list()
        >>>
        >>> # Delete a category
        >>> client.transaction_categories.delete("cat_123")
    """

    _path = "/transaction-categories"

    def create(
        self,
        name: str,
        *,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> TransactionCategory:
        """
        Create a new transaction category.

        Args:
            name: Category name (1-100 characters).
            color: Optional hex color code (e.g., "#FF5733").
            icon: Optional icon name/identifier (max 50 characters).
            parent_id: Optional parent category ID for creating subcategories.

        Returns:
            The created TransactionCategory object.

        Raises:
            ValidationError: If the request data is invalid.
            NotFoundError: If the parent category doesn't exist.

        Example:
            >>> # Create a top-level category
            >>> food = client.transaction_categories.create(
            ...     name="Food & Dining",
            ...     color="#FF9800",
            ...     icon="restaurant",
            ... )
            >>>
            >>> # Create a subcategory
            >>> groceries = client.transaction_categories.create(
            ...     name="Groceries",
            ...     color="#4CAF50",
            ...     icon="shopping_cart",
            ...     parent_id=food.id,
            ... )
        """
        request = TransactionCategoryCreateRequest(
            name=name,
            color=color,
            icon=icon,
            parent_id=parent_id,
        )

        response = self._transport.post(
            self._path,
            json=request.model_dump(by_alias=True, exclude_none=True),
        )

        return TransactionCategory.model_validate(response)

    def list(
        self,
        *,
        parent_id: Optional[str] = None,
    ) -> list[TransactionCategory]:
        """
        List transaction categories.

        Note: The API does not support pagination for this endpoint.
        All categories are returned.

        Args:
            parent_id: Optional filter by parent category ID.
                      Use None to get top-level categories only.

        Returns:
            List of TransactionCategory objects.

        Example:
            >>> # List all categories
            >>> categories = client.transaction_categories.list()
            >>> for cat in categories:
            ...     print(f"{cat.name} ({cat.color or 'no color'})")
            >>>
            >>> # List subcategories of a parent
            >>> subcategories = client.transaction_categories.list(
            ...     parent_id="cat_food",
            ... )
        """
        params: dict[str, str] = {}

        if parent_id is not None:
            params["parentId"] = parent_id

        response = self._transport.get(self._path, params=params or None)

        # API returns raw list
        if isinstance(response, list):
            return [TransactionCategory.model_validate(item) for item in response]

        # Fallback for wrapped response
        return [
            TransactionCategory.model_validate(item)
            for item in response.get("data", [])
        ]

    def delete(self, category_id: str) -> None:
        """
        Delete a transaction category.

        Note: Deleting a category may affect transactions that use it.
        Consider updating those transactions first.

        Args:
            category_id: The unique category identifier.

        Raises:
            NotFoundError: If the category doesn't exist.

        Example:
            >>> client.transaction_categories.delete("cat_123")
        """
        self._transport.delete(f"{self._path}/{category_id}")
