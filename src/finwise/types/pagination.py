"""Pagination types."""

from __future__ import annotations

import json
import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


@dataclass
class PaginationInfo:
    """Pagination info extracted from response headers."""

    page_number: int
    page_size: int
    total_count: int
    has_next: bool

    @classmethod
    def from_headers(cls, headers: dict[str, str]) -> PaginationInfo:
        """Create from response headers."""
        return cls(
            page_number=int(headers.get("x-page-number", "1")),
            page_size=int(headers.get("x-page-size", "100")),
            total_count=int(headers.get("x-count", "0")),
            has_next=headers.get("x-has-next-page", "false").lower() == "true",
        )

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        if self.page_size == 0:
            return 0
        return math.ceil(self.total_count / self.page_size)

    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.page_number > 1


def build_list_params(
    page_number: int = 1,
    page_size: int = 100,
    filters: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Build query params for list endpoints with JSON-encoded values."""
    params: dict[str, str] = {
        "pagination": json.dumps({"pageNumber": page_number, "pageSize": page_size})
    }
    if filters:
        params["filters"] = json.dumps(filters)
    return params


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
