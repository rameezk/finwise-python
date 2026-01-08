"""Pagination types."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Pagination parameters for list requests.

    Attributes:
        page_number: Page number to retrieve (1-indexed, default: 1).
        page_size: Number of items per page (default: 100, max: 500).

    Example:
        >>> params = PaginationParams(page_number=2, page_size=50)
        >>> client.accounts.list(**params.to_query_dict())
    """

    page_number: int = Field(default=1, ge=1, alias="pageNumber")
    page_size: int = Field(default=100, ge=1, le=500, alias="pageSize")

    model_config = ConfigDict(populate_by_name=True)

    def to_query_dict(self) -> dict[str, Any]:
        """Convert to query parameter dictionary for API requests."""
        return {
            "pageNumber": self.page_number,
            "pageSize": self.page_size,
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.

    Attributes:
        data: List of items on the current page.
        page_number: Current page number.
        page_size: Items per page.
        total_count: Total number of items across all pages.
        total_pages: Total number of pages.
        has_next: Whether there are more pages after this one.
        has_previous: Whether there are pages before this one.

    Example:
        >>> accounts = client.accounts.list(page_size=10)
        >>> print(f"Page {accounts.page_number} of {accounts.total_pages}")
        >>> for account in accounts.data:
        ...     print(account.name)
        >>> # Or access by index
        >>> first = accounts[0]
        >>> if accounts.has_next:
        ...     next_page = client.accounts.list(page_number=accounts.page_number + 1)
    """

    data: list[T]
    page_number: int = Field(..., alias="pageNumber")
    page_size: int = Field(..., alias="pageSize")
    total_count: int = Field(..., alias="totalCount")
    total_pages: int = Field(..., alias="totalPages")
    has_next: bool = Field(..., alias="hasNext")
    has_previous: bool = Field(..., alias="hasPrevious")

    model_config = ConfigDict(populate_by_name=True)

    def items(self) -> Iterator[T]:
        """Iterate over the data items on this page."""
        return iter(self.data)

    def __len__(self) -> int:
        """Return the number of items on this page."""
        return len(self.data)

    def __getitem__(self, index: int) -> T:
        """Get an item by index."""
        return self.data[index]
