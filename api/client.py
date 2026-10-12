import logging
import requests

log = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url="https://petstore.swagger.io/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        log.info("%s %s %s", method, url, kwargs.get("json", ""))
        response = self.session.request(method, url, timeout=15, **kwargs)
        log.info("-> %s %s", response.status_code, response.text[:200])
        return response

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, **kw):
        return self.request("POST", path, **kw)

    def put(self, path, **kw):
        return self.request("PUT", path, **kw)

    def delete(self, path, **kw):
        return self.request("DELETE", path, **kw)
