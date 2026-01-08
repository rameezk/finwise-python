"""Shared test fixtures."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
import respx

from finwise import FinWise


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return "test-api-key-12345"


@pytest.fixture
def base_url() -> str:
    """Test API base URL."""
    return "https://api.finwiseapp.io"


@pytest.fixture
def client(api_key: str, base_url: str) -> Generator[FinWise, None, None]:
    """Create a FinWise client for testing."""
    client = FinWise(api_key=api_key, base_url=base_url)
    yield client
    client.close()


@pytest.fixture
def mock_api(base_url: str) -> Generator[respx.Router, None, None]:
    """Create a mock API router."""
    with respx.mock(base_url=base_url) as router:
        yield router


@pytest.fixture
def sample_account() -> dict[str, Any]:
    """Sample account response data."""
    return {
        "id": "acc_123abc",
        "name": "Test Savings Account",
        "type": "savings",
        "currency": "USD",
        "description": "My test savings account",
        "balance": 5000.00,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-15T12:30:00Z",
        "archivedAt": None,
    }


@pytest.fixture
def sample_account_archived(sample_account: dict[str, Any]) -> dict[str, Any]:
    """Sample archived account response data."""
    return {
        **sample_account,
        "archivedAt": "2024-02-01T00:00:00Z",
    }


@pytest.fixture
def sample_accounts_list(sample_account: dict[str, Any]) -> dict[str, Any]:
    """Sample paginated accounts list response."""
    return {
        "data": [
            sample_account,
            {
                **sample_account,
                "id": "acc_456def",
                "name": "Test Checking Account",
                "type": "checking",
                "balance": 2500.00,
            },
        ],
        "pageNumber": 1,
        "pageSize": 100,
        "totalCount": 2,
        "totalPages": 1,
        "hasNext": False,
        "hasPrevious": False,
    }


@pytest.fixture
def sample_transaction() -> dict[str, Any]:
    """Sample transaction response data."""
    return {
        "id": "txn_789xyz",
        "accountId": "acc_123abc",
        "amount": "-50.00",
        "transactionDate": "2024-01-15",
        "description": "Grocery shopping",
        "categoryId": "cat_groceries",
        "categoryName": "Groceries",
        "type": "expense",
        "createdAt": "2024-01-15T10:00:00Z",
        "updatedAt": "2024-01-15T10:00:00Z",
        "archivedAt": None,
    }


@pytest.fixture
def sample_category() -> dict[str, Any]:
    """Sample transaction category response data."""
    return {
        "id": "cat_groceries",
        "name": "Groceries",
        "color": "#4CAF50",
        "icon": "shopping_cart",
        "parentId": None,
        "createdAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def error_not_found() -> dict[str, Any]:
    """Sample 404 error response."""
    return {
        "message": "Resource not found",
        "code": "NOT_FOUND",
        "errors": [],
    }


@pytest.fixture
def error_validation() -> dict[str, Any]:
    """Sample 400 validation error response."""
    return {
        "message": "Validation failed",
        "code": "VALIDATION_ERROR",
        "errors": [
            {
                "code": "REQUIRED",
                "message": "Name is required",
                "path": ["name"],
                "received": None,
            }
        ],
    }


@pytest.fixture
def error_unauthorized() -> dict[str, Any]:
    """Sample 401 unauthorized error response."""
    return {
        "message": "Invalid API key",
        "code": "UNAUTHORIZED",
        "errors": [],
    }
