import requests
from exceptions import ServerError, ClientError
from crawler.crawl_services import logger


class RequestProcessor:

    def __init__(self, url, header = None, body = None,):
        self._url = url
        self._header = header or {}
        self._body = body or {}

    def get_request(self):
        try:
            response = requests.get(self._url)
            return response
        except Exception as e:
            raise requests.exceptions.RequestException(f"can not send request for reason : {str(e)}")

    def _check_status(self, status: int, response):
        if status == 200:
            return
        elif 500 > status >= 400:
            logger.error(f"Request failed due to ValidationError: {response.text}")
            raise ClientError
        elif 600 > status >= 500:
            logger.error(f"Request failed due to Server Error: {response.text}")
            raise ServerError

