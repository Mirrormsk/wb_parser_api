from time import sleep
import logging
import requests
from requests import RequestException

logger = logging.getLogger(__name__)


class WbParser:
    def __init__(self):
        self.request_delay = 1
        self.max_request_retries = 5

    def _make_request(
        self, url: str, params: dict = None, headers: dict = None
    ) -> requests.Response:
        """Make self.max_request_retries attempts for request"""
        for attempt in range(self.max_request_retries):
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response
            except RequestException as e:
                if attempt < self.max_request_retries - 1:
                    sleep(self.request_delay)
                    logger.info(f"Attempt {attempt + 1} to make request to {url}")
                else:
                    logger.error(f"Cant make request to {url}. Error: {e}")

    def _get_query(self, query: str) -> requests.Response:
        """
        Make request to WB.
        :param query: query for search (product name)
        :return: requests.Response
        """
        headers = {
            "Pragma": "no-cache",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Accept-Language": "ru",
            # 'Accept-Encoding': 'gzip, deflate, br',
            "Sec-Fetch-Mode": "cors",
            "Cache-Control": "no-cache",
            "Origin": "https://www.wildberries.ru",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Referer": "https://www.wildberries.ru/",
            "Connection": "keep-alive",
            "Host": "search.wb.ru",
            "Sec-Fetch-Dest": "empty",
        }

        params = {
            "TestGroup": "no_test",
            "TestID": "no_test",
            "appType": "1",
            "curr": "rub",
            "dest": "-446078",
            "query": query,
            "resultset": "catalog",
            "sort": "popular",
            "suppressSpellcheck": "false",
            "uclusters": "0",
        }

        response = self._make_request(
            "https://search.wb.ru/exactmatch/ru/male/v4/search",
            params=params,
            headers=headers,
        )

        return response

    def parse_query(self, query: str, count: int = 10):
        """Get query response from WB and return products list"""
        response = self._get_query(query)
        if response.ok:
            data = response.json()
            results = data["data"]["products"]
            return results[:count]
        else:
            raise requests.exceptions.RequestException("Can not connect to WB API")

    @staticmethod
    def normalize_results(results: list[dict]) -> list[str]:
        """Normalize response from WB API for sending in Telegram message"""
        normalized_results = []
        for item in results:
            item_name = item.get("name")
            item_id = item.get("id")
            item_url = f"https://www.wildberries.ru/catalog/{item_id}/detail.aspx"
            normalized_results.append(
                f"{item_name}:\n{item_url}"
            )
        return normalized_results


wb_parser = WbParser()
