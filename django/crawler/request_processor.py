import logging

import requests

logger = logging.getLogger(__name__)


class RequestProcessor:
    def __init__(
        self,
        url,
        header=None,
        body=None,
    ):
        self._url = url
        self._header = header or {}
        self._body = body or {}

    def get_request(self):
        try:
            return requests.get(self._url)
        except Exception as e:
            raise requests.exceptions.RequestException(
                f"can not send request for reason : {str(e)}"
            )
