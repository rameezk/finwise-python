"""Base resource class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from finwise._http import HTTPTransport


class BaseResource:
    """
    Base class for API resources.

    Provides common functionality for all resource classes including
    HTTP transport access.
    """

    def __init__(self, transport: HTTPTransport) -> None:
        """
        Initialize the resource.

        Args:
            transport: HTTP transport instance for making API requests.
        """
        self._transport = transport
