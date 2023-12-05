import requests
import urllib.parse
from UtilClasses.csitem import CsItem


class BuffParser:
    def __init__(self, session: str):
        self.__set_buff_ids()
        self.__goods_url = 'https://buff.163.com/api/market/goods'
        self.__request_cookies = {'session': session}

        # Test buff connection.
        params = {'game': 'csgo', 'page_num': 2}
        response = requests.get(self.__goods_url, params=params, cookies=self.__request_cookies)
        response_code = response.json()['code']

        if response_code != 'OK':
            raise BuffParserException(f'Failed to connect to buff servers: {response_code}.')

    def get_page_data(self, page_index: int) -> [CsItem]:
        """
        Parses buff page by page index. BuffParserException can be raised.
        :param page_index: Index of parsing page.
        :return: CsItems array with hash_name and buff_cny_price.
        """
        params = {'game': 'csgo', 'page_num': page_index}
        response = requests.get(self.__goods_url, params=params, cookies=self.__request_cookies)
        response_dict = response.json()
        response.close()
        response_code = response_dict['code']

        if response_code != 'OK':
            raise BuffParserException(f'Failed to request buff for page {page_index}: {response_code}')

        item_datas = response_dict['data']['items']
        items = []

        for item_data in item_datas:
            items.append(CsItem(hash_name=item_data['market_hash_name'], buff_price=float(item_data['sell_min_price'])))

        return items

    def get_item_data(self, hash_name: str) -> CsItem:
        """
        Returns raw buff data by hash_name. BuffParserException can be raised.
        :param hash_name: Hash name of sought-for item.
        :return: CsItem with hash_name and buff_cny_price.
        """
        # Get buff id.
        try:
            buff_id = self.__get_buff_id_by_hash(hash_name=hash_name)
        except KeyError:
            raise BuffParserException('Buff id was now found.')

        # Scan buff.
        params = {
            'game': 'csgo',
            'page_num': '1',
            'goods_id': buff_id
        }

        item_url = f'https://buff.163.com/api/market/goods/sell_order?{urllib.parse.urlencode(params)}'
        response = requests.get(url=item_url, params=params, cookies=self.__request_cookies)
        response_dict = response.json()
        response.close()
        response_code = response_dict['code']

        # Does buff response is error?
        if response_code != 'OK':
            raise BuffParserException(f'Failed to ask buff for {hash_name}: {response_code}.')

        # Buff response is successful.
        item = response_dict['data']['items'][0]

        return CsItem(hash_name=hash_name, buff_price=float(item['price']))

    def __set_buff_ids(self):
        """
        Sets __buff_ids to know buff ids.
        :return: None
        """
        self.__buff_ids = {}
        buff_ids_url = 'https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt'
        buff_ids_lines = requests.get(url=buff_ids_url).text.split('\n')

        for buff_id_line in buff_ids_lines:
            split = buff_id_line.split(';')
            self.__buff_ids[split[1]] = int(split[0])

    def __get_buff_id_by_hash(self, hash_name: str) -> int:
        """
        Returns buff int id by item hash name. KeyError exception can be raised.
        :param hash_name: Hash name of sought-for item.
        :return: Buff int id.
        """
        return self.__buff_ids[hash_name]


class BuffParserException(Exception):
    pass
