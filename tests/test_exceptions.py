"""Tests for exception handling and error message extraction."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from finwise import FinWise, ValidationError
from finwise.exceptions import _extract_error_message


class TestExtractErrorMessage:
    """Tests for _extract_error_message helper function."""

    def test_top_level_message(self) -> None:
        """Test extraction of top-level message."""
        response = {"message": "Validation failed", "code": "VALIDATION_ERROR"}
        assert _extract_error_message(response) == "Validation failed"

    def test_nested_error_message(self) -> None:
        """Test extraction from nested error.message (actual API format)."""
        response = {
            "error": {
                "errors": [{"code": "unrecognized_keys"}],
                "name": "BadRequestError",
                "message": "Invalid request query params",
            }
        }
        assert _extract_error_message(response) == "Invalid request query params"

    def test_fastapi_detail_format(self) -> None:
        """Test extraction of FastAPI-style detail field."""
        response = {"detail": "Not authenticated"}
        assert _extract_error_message(response) == "Not authenticated"

    def test_top_level_takes_precedence(self) -> None:
        """Test that top-level message takes precedence over nested."""
        response = {
            "message": "Top level message",
            "error": {"message": "Nested message"},
        }
        assert _extract_error_message(response) == "Top level message"

    def test_fallback_includes_response_body(self) -> None:
        """Test fallback includes response body for debugging."""
        response = {"unknownField": "some value", "code": 12345}
        result = _extract_error_message(response)
        assert "API error:" in result
        assert "unknownField" in result

    def test_empty_response_body(self) -> None:
        """Test handling of empty response body."""
        response: dict[str, Any] = {}
        assert _extract_error_message(response) == "Unknown error (empty response body)"

    def test_non_string_message_ignored(self) -> None:
        """Test that non-string messages are ignored."""
        response = {"message": 12345, "error": {"message": "Nested message"}}
        assert _extract_error_message(response) == "Nested message"

    def test_non_dict_error_ignored(self) -> None:
        """Test that non-dict error fields are ignored."""
        response = {"error": "This is a string, not a dict"}
        result = _extract_error_message(response)
        assert "API error:" in result


class TestApiErrorFormat:
    """Tests for actual API error format handling."""

    def test_pagination_error_format(
        self,
        client: FinWise,
        mock_api: respx.Router,
    ) -> None:
        """Test that the actual API error format is handled correctly."""
        # This is the actual format returned by the FinWise API
        api_error_response = {
            "error": {
                "errors": [
                    {
                        "code": "unrecognized_keys",
                        "keys": ["pageNumber", "pageSize"],
                        "path": [],
                        "message": "Unrecognized key(s) in object: 'pageNumber', 'pageSize'",
                    }
                ],
                "name": "BadRequestError",
                "message": "Invalid request query params",
            }
        }

        mock_api.get("/transactions").mock(
            return_value=Response(400, json=api_error_response)
        )

        with pytest.raises(ValidationError) as exc_info:
            client.transactions.list()

        # Should extract the correct message, not "Unknown error"
        assert exc_info.value.message == "Invalid request query params"
        assert exc_info.value.status_code == 400

    def test_currency_code_error_format(
        self,
        client: FinWise,
        mock_api: respx.Router,
    ) -> None:
        """Test that currency code validation error is handled correctly."""
        api_error_response = {
            "error": {
                "errors": [
                    {
                        "code": "invalid_type",
                        "expected": "string",
                        "received": "undefined",
                        "path": ["currencyCode"],
                        "message": "Required",
                    }
                ],
                "name": "BadRequestError",
                "message": "Invalid request query params",
            }
        }

        mock_api.get("/account-balances/aggregated").mock(
            return_value=Response(400, json=api_error_response)
        )

        with pytest.raises(ValidationError) as exc_info:
            client.account_balances.aggregated()

        assert exc_info.value.message == "Invalid request query params"
        assert exc_info.value.status_code == 400
