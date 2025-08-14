import os
import requests
from dotenv import load_dotenv
from utilities.logger_utilities import setup_logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
API_KEY = os.getenv("API_KEY", "special-key")


class APIClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "api_key": api_key or API_KEY,
            }
        )

        self.logger = setup_logger()

    def _url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.base_url}{endpoint}"

    def _request(self, method: str, endpoint: str, **kwargs: dict[str, object]) -> requests.Response:
        url = self._url(endpoint)
        kwargs.setdefault("timeout", self.timeout)

        per_call_headers: dict[str, object] = (kwargs.pop("headers", {}) or {})  # type: ignore[assignment]
        headers = {**self.session.headers, **per_call_headers}

        if kwargs.pop("no_auth", False):
            headers.pop("api_key", None)

        response = self.session.request(method=method, url=url, headers=headers, **kwargs)

        safe_headers = dict(headers)
        if "api_key" in safe_headers:
            safe_headers["api_key"] = "******"

        self.logger.info("%s %s -> %s", method.upper(), url, response.status_code)
        self.logger.debug("headers: %s", safe_headers)
        if "json" in kwargs and kwargs["json"] is not None:
            self.logger.debug("payload(json): %s", kwargs["json"])
        if "data" in kwargs and kwargs["data"] is not None:
            self.logger.debug("payload(form): %s", kwargs["data"])
        self.logger.debug("response: %s", response.text[:500])

        return response


    def get(
        self,
        endpoint: str,
        params: dict[str, object] | None = None,
        **kwargs: dict[str, object],
    ) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        json: dict[str, object] | None = None,
        data: dict[str, object] | None = None,
        **kwargs: dict[str, object],
    ) -> requests.Response:
        return self._request("POST", endpoint, json=json, data=data, **kwargs)

    def put(
        self,
        endpoint: str,
        json: dict[str, object] | None = None,
        data: dict[str, object] | None = None,
        **kwargs: dict[str, object],
    ) -> requests.Response:
        return self._request("PUT", endpoint, json=json, data=data, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs: dict[str, object],
    ) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)