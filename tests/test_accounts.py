"""Tests for the Accounts resource."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from finwise import (
    Account,
    AuthenticationError,
    FinWise,
    NotFoundError,
    PaginatedResponse,
    ValidationError,
)


class TestAccountsCreate:
    """Tests for accounts.create()."""

    def test_create_account_success(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_account: dict[str, Any],
    ) -> None:
        """Test successful account creation."""
        mock_api.post("/accounts").mock(
            return_value=Response(201, json=sample_account)
        )

        account = client.accounts.create(
            name="Test Savings Account",
            type="savings",
            currency="USD",
            description="My test savings account",
        )

        assert isinstance(account, Account)
        assert account.id == "acc_123abc"
        assert account.name == "Test Savings Account"
        assert account.type == "savings"
        assert account.currency == "USD"
        assert account.balance == 5000.00
        assert not account.is_archived

    def test_create_account_minimal(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_account: dict[str, Any],
    ) -> None:
        """Test account creation with minimal parameters."""
        mock_api.post("/accounts").mock(
            return_value=Response(201, json=sample_account)
        )

        account = client.accounts.create(
            name="Test Account",
            type="checking",
        )

        assert isinstance(account, Account)
        assert account.id == "acc_123abc"

    def test_create_account_client_validation_error(
        self,
        client: FinWise,
    ) -> None:
        """Test that Pydantic validates request data on the client side."""
        import pydantic

        with pytest.raises(pydantic.ValidationError) as exc_info:
            client.accounts.create(name="", type="savings")

        assert "String should have at least 1 character" in str(exc_info.value)

    def test_create_account_server_validation_error(
        self,
        client: FinWise,
        mock_api: respx.Router,
        error_validation: dict[str, Any],
    ) -> None:
        """Test account creation with server-side validation error."""
        mock_api.post("/accounts").mock(
            return_value=Response(400, json=error_validation)
        )

        with pytest.raises(ValidationError) as exc_info:
            # Valid client-side data, but server returns 400
            client.accounts.create(name="Valid Name", type="savings")

        assert exc_info.value.status_code == 400
        assert "Validation failed" in exc_info.value.message


class TestAccountsRetrieve:
    """Tests for accounts.retrieve()."""

    def test_retrieve_account_success(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_account: dict[str, Any],
    ) -> None:
        """Test successful account retrieval."""
        mock_api.get("/accounts/acc_123abc").mock(
            return_value=Response(200, json=sample_account)
        )

        account = client.accounts.retrieve("acc_123abc")

        assert isinstance(account, Account)
        assert account.id == "acc_123abc"
        assert account.name == "Test Savings Account"

    def test_retrieve_account_not_found(
        self,
        client: FinWise,
        mock_api: respx.Router,
        error_not_found: dict[str, Any],
    ) -> None:
        """Test account retrieval with not found error."""
        mock_api.get("/accounts/invalid_id").mock(
            return_value=Response(404, json=error_not_found)
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.accounts.retrieve("invalid_id")

        assert exc_info.value.status_code == 404

    def test_retrieve_account_unauthorized(
        self,
        client: FinWise,
        mock_api: respx.Router,
        error_unauthorized: dict[str, Any],
    ) -> None:
        """Test account retrieval with authentication error."""
        mock_api.get("/accounts/acc_123abc").mock(
            return_value=Response(401, json=error_unauthorized)
        )

        with pytest.raises(AuthenticationError) as exc_info:
            client.accounts.retrieve("acc_123abc")

        assert exc_info.value.status_code == 401


class TestAccountsUpdate:
    """Tests for accounts.update()."""

    def test_update_account_success(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_account: dict[str, Any],
    ) -> None:
        """Test successful account update."""
        updated_account = {**sample_account, "name": "Updated Account Name"}
        mock_api.patch("/accounts/acc_123abc").mock(
            return_value=Response(200, json=updated_account)
        )

        account = client.accounts.update(
            "acc_123abc",
            name="Updated Account Name",
        )

        assert isinstance(account, Account)
        assert account.name == "Updated Account Name"

    def test_update_account_not_found(
        self,
        client: FinWise,
        mock_api: respx.Router,
        error_not_found: dict[str, Any],
    ) -> None:
        """Test account update with not found error."""
        mock_api.patch("/accounts/invalid_id").mock(
            return_value=Response(404, json=error_not_found)
        )

        with pytest.raises(NotFoundError):
            client.accounts.update("invalid_id", name="New Name")


class TestAccountsList:
    """Tests for accounts.list()."""

    def test_list_accounts_success(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_accounts_list: dict[str, Any],
    ) -> None:
        """Test successful account listing."""
        mock_api.get("/accounts").mock(
            return_value=Response(200, json=sample_accounts_list)
        )

        accounts = client.accounts.list()

        assert isinstance(accounts, PaginatedResponse)
        assert len(accounts) == 2
        assert accounts.total_count == 2
        assert accounts.page_number == 1
        assert not accounts.has_next

        # Test iteration over data
        account_names = [acc.name for acc in accounts.data]
        assert "Test Savings Account" in account_names
        assert "Test Checking Account" in account_names

        # Test index access
        assert accounts[0].name == "Test Savings Account"

    def test_list_accounts_with_pagination(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_accounts_list: dict[str, Any],
    ) -> None:
        """Test account listing with pagination parameters."""
        paginated_response = {
            **sample_accounts_list,
            "pageNumber": 2,
            "pageSize": 50,
            "hasNext": True,
            "hasPrevious": True,
        }
        mock_api.get("/accounts").mock(
            return_value=Response(200, json=paginated_response)
        )

        accounts = client.accounts.list(page_number=2, page_size=50)

        assert accounts.page_number == 2
        assert accounts.page_size == 50
        assert accounts.has_next
        assert accounts.has_previous

    def test_list_accounts_empty(
        self,
        client: FinWise,
        mock_api: respx.Router,
    ) -> None:
        """Test listing with no accounts."""
        empty_response = {
            "data": [],
            "pageNumber": 1,
            "pageSize": 100,
            "totalCount": 0,
            "totalPages": 0,
            "hasNext": False,
            "hasPrevious": False,
        }
        mock_api.get("/accounts").mock(
            return_value=Response(200, json=empty_response)
        )

        accounts = client.accounts.list()

        assert len(accounts) == 0
        assert accounts.total_count == 0


class TestAccountsArchive:
    """Tests for accounts.archive()."""

    def test_archive_account_success(
        self,
        client: FinWise,
        mock_api: respx.Router,
        sample_account_archived: dict[str, Any],
    ) -> None:
        """Test successful account archival."""
        mock_api.post("/accounts/acc_123abc/archive").mock(
            return_value=Response(200, json=sample_account_archived)
        )

        account = client.accounts.archive("acc_123abc")

        assert isinstance(account, Account)
        assert account.is_archived
        assert account.archived_at is not None

    def test_archive_account_not_found(
        self,
        client: FinWise,
        mock_api: respx.Router,
        error_not_found: dict[str, Any],
    ) -> None:
        """Test archiving non-existent account."""
        mock_api.post("/accounts/invalid_id/archive").mock(
            return_value=Response(404, json=error_not_found)
        )

        with pytest.raises(NotFoundError):
            client.accounts.archive("invalid_id")


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_requires_api_key(self) -> None:
        """Test that client requires an API key."""
        with pytest.raises(ValueError) as exc_info:
            FinWise()

        assert "API key must be provided" in str(exc_info.value)

    def test_client_with_api_key(self, api_key: str) -> None:
        """Test client initialization with API key."""
        client = FinWise(api_key=api_key)
        assert client.accounts is not None
        assert client.transactions is not None
        assert client.account_balances is not None
        assert client.transaction_categories is not None
        client.close()

    def test_client_context_manager(self, api_key: str) -> None:
        """Test client as context manager."""
        with FinWise(api_key=api_key) as client:
            assert client.accounts is not None

    def test_client_repr(self, client: FinWise) -> None:
        """Test client string representation."""
        repr_str = repr(client)
        assert "FinWise" in repr_str
        assert "api.finwiseapp.io" in repr_str
