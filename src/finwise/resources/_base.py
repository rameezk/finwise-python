"""Base resource class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from finwise.types.pagination import PaginationParams

if TYPE_CHECKING:
    from finwise._http import HTTPTransport


class BaseResource:
    """
    Base class for API resources.

    Provides common functionality for all resource classes including
    HTTP transport access and pagination parameter building.
    """

    def __init__(self, transport: HTTPTransport) -> None:
        """
        Initialize the resource.

        Args:
            transport: HTTP transport instance for making API requests.
        """
        self._transport = transport

    def _build_pagination_params(
        self,
        page_number: int = 1,
        page_size: int = 100,
    ) -> dict[str, Any]:
        """
        Build pagination query parameters.

        Args:
            page_number: Page number (1-indexed).
            page_size: Items per page.

        Returns:
            Dictionary of pagination parameters for the API.
        """
        params = PaginationParams(page_number=page_number, page_size=page_size)
        return params.to_query_dict()
