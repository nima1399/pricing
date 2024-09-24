from abc import abstractmethod

import requests

from .models import CrawlConfig
import logging

logger = logging.getLogger(__name__)

class BaseCrawlService:

    def __init__(self, conf: CrawlConfig):
        self._conf = conf

    @abstractmethod
    def fetch(self):
        raise NotImplementedError


class NobitexCrawlService(BaseCrawlService):

    def fetch(self):
        try:
            crawl_config = self._conf
            logger.info("reached hereeeeee")
            logger.info(f"helper_data: {crawl_config.helper_data}")
            url = list(crawl_config.helper_data.keys())[0]
            logger.info("reached here")
            btc_usdt = requests.get(url).json()["lastTradePrice"]
            logger.info("reach here 2")
            logger.info(f"btc_usdt: {btc_usdt}")
            return float(btc_usdt)
        except Exception as e:
            logger.error(f"Error in NobitexCrawlService.fetch: {e}")
            raise e

# SOLID PRINCIPLES SHOULD BE CONSIDERED