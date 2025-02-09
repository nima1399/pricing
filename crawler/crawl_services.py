import logging
from abc import abstractmethod

from crawler.models import CrawlConfig
from crawler.request_processor import RequestProcessor

logger = logging.getLogger(__name__)


class BaseCrawlService:

    def __init__(self, conf: CrawlConfig):
        self._conf = conf

    @abstractmethod
    def fetch(self):
        raise NotImplementedError


class NobitexCrawlService(BaseCrawlService):

    def fetch(self):
        response = self._get_response()
        price = self._get_price(response)
        logger.info(f"{self._conf.valuable_object.title}: {price}")
        return float(price)

    def _get_response(self):
        request = RequestProcessor(self._conf.get_url())
        return request.get_request()

    def _get_price(self, response):
        return response.json()["lastTradePrice"]
