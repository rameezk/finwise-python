"""Configuration management."""

from __future__ import annotations

from dataclasses import dataclass

from finwise._version import __version__


@dataclass(frozen=True)
class ClientConfig:
    """
    Client configuration settings.

    Attributes:
        api_key: FinWise API key for authentication.
        base_url: API base URL (default: https://api.finwiseapp.io).
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum retry attempts for failed requests (default: 3).
        version: SDK version (auto-populated).
    """

    api_key: str
    base_url: str = "https://api.finwiseapp.io"
    timeout: float = 30.0
    max_retries: int = 3
    version: str = __version__

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not self.api_key:
            raise ValueError("api_key cannot be empty")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
