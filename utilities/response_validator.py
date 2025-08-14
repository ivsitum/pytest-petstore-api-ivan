from __future__ import annotations
import json
from typing import Any, Iterable, List, Mapping
import requests
from utilities.logger_utilities import setup_logger

logger = setup_logger()


class ResponseValidator:
    """helper class with common HTTP/JSON assertions for API tests."""
    @staticmethod
    def _json(response: requests.Response) -> Any:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("Response is not valid JSON. Raw body: %s", response.text)
            assert False, "Response body is not valid JSON"

    @staticmethod
    def validate_status_code(response: requests.Response, expected_status: int) -> None:
        if response.status_code != expected_status:
            logger.error(
                "Unexpected status code: got %s, expected %s. Body: %s",
                response.status_code,
                expected_status,
                response.text,
            )
        assert response.status_code == expected_status, (
            f"Unexpected status {response.status_code}; expected {expected_status}. "
            f"Body: {response.text}"
        )

    @staticmethod
    def validate_json_response(response: requests.Response) -> None:
        ResponseValidator._json(response)

    @staticmethod
    def validate_json_value(response: requests.Response, key: str, expected_value: Any) -> None:
        """Assert top-level JSON object has key and its value equals expected_value."""
        data = ResponseValidator._json(response)
        assert isinstance(data, Mapping), "Expected JSON object at top level"

        assert key in data, f"Response JSON does not contain key '{key}'"
        actual = data[key]
        assert actual == expected_value, f"Expected {key} == {expected_value!r}, got {actual!r}"

    @staticmethod
    def validate_status_code_in(response, expected_statuses):
        assert response.status_code in expected_statuses, (
            f"Unexpected status {response.status_code}; "
            f"expected one of {expected_statuses}. "
            f"Body: {response.text}"
        )
