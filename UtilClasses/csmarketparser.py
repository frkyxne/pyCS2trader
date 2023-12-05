import requests
from UtilClasses.csitem import CsItem


class CsMarketParser:
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__api_url = 'https://market.csgo.com/api/v2/'

    def get_item_data(self, hash_name: str) -> CsItem:
        request_url = self.__api_url + 'search-item-by-hash-name'
        request_params = {'key': self.__api_key, 'hash_name': hash_name}
        response = CsMarketParser.__request_market(url=request_url, params=request_params)
        item = response['data'][0]
        return CsItem(hash_name=hash_name, market_price=int(item['price']))

    def get_items_data(self, hash_names: [str]) -> [CsItem]:
        request_url = self.__api_url + 'search-list-items-by-hash-name-all'
        request_params = {'key': self.__api_key}

        for index, hash_name in enumerate(hash_names):
            request_params.update({f'list_hash_name[{index}]': hash_name})

        response = CsMarketParser.__request_market(url=request_url, params=request_params)
        response_data = response['data']
        cs_items = []

        for item_hash in response_data.keys():
            item_data = response_data[item_hash][0]
            cs_items.append(CsItem(hash_name=item_hash, market_price=int(item_data['price'])))

        return cs_items

    @staticmethod
    def __request_market(url: str, params: dict):
        response = requests.get(url, params)

        if response.status_code == 401:
            raise CsMarketException('Bad market api key.')
        elif response.status_code == 502:
            raise CsMarketException('No connection with market.csgo.com servers.')
        elif response.status_code == 503:
            raise CsMarketException('Engineering works on market.csgo.com servers.')
        elif response.status_code != 200:
            raise CsMarketException('Market.csgo.com unknown exception.')

        return response.json()


class CsMarketException(Exception):
    pass