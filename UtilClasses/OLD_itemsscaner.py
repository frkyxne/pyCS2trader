import json
import urllib.parse
import requests
import random
import time
from FOREIGN.csmarketapi import CsMarket
from classes import CsItem, CsItemsList
from config import ItemsScaner as ScanerConfig
from constants import ItemScaner as ScanerConstants


class ItemsScaner:
    def __set_buff_ids(self):
        self.__buff_ids = {}
        buff_ids_lines = requests.get(url=ScanerConfig.BUFF_URL_IDS_FILE).text.split('\n')

        for buff_id_line in buff_ids_lines:
            split = buff_id_line.split(';')
            self.__buff_ids[split[1]] = int(split[0])

    def __init__(self):
        self.__market = CsMarket(api_key=ScanerConfig.CS_MARKET_API_KEY)
        self.__set_buff_ids()
        self.__buff_page = 1

    def __get_buff_id_by_hash(self, hash_name: str):  # Returns str or None
        if hash_name in self.__buff_ids.keys():
            return self.__buff_ids[hash_name]
        else:
            return None

    def __get_item_buff_data(self, hash_name: str, do_timeout: bool = False) -> (dict, str):
        # Returns (data or None, processing error or None).
        buff_id = self.__get_buff_id_by_hash(hash_name=hash_name)

        if buff_id is None:
            return None, 'Buff id was not found.'

        # Scan buff.
        params = {
            'game': 'csgo',
            'page_num': '1',
            'goods_id': buff_id
        }

        buff_item_url = f'{ScanerConfig.BUFF_URL_SALE}/sell_order?{urllib.parse.urlencode(params)}'

        # Trying to get buff response.
        try:
            buff_response = requests.get(url=buff_item_url, cookies=ScanerConfig.BUFF_COOKIES,
                                         headers=ScanerConfig.BUFF_HEADERS)
        except Exception:
            return None, ScanerConstants.EXCEPTION_BUFF_REQUEST_FAILED

        if do_timeout:
            print(f'Buff asked for {hash_name}, sleeping...')
            ItemsScaner.__sleep()

        buff_json_load = json.loads(buff_response.text)
        buff_response.close()

        # Does buff response is error?
        if buff_json_load['code'] != 'OK':
            return None, f'Buff response is an error: {buff_json_load["data"]}.'

        # Buff response is successful.
        return buff_json_load['data']['items'][0], None

    def __get_item_market_data(self, hash_name: str) -> (dict, str):  # Returns (data or None, processing error or
        # None).
        try:
            return self.__market.search_item_by_hash_name(hash_name=hash_name)['data'], None
        except Exception as ex:
            return None, str(ex)

    def __get_list_buff_data(self, hash_names: [str]) -> dict:  # dict(hash_name: data)
        cs_items = dict()

        for hash_name in hash_names:
            try:
                buff_data = self.__get_item_buff_data(hash_name=hash_name, do_timeout=True)
                cs_items[hash_name] = buff_data
            except Exception as ex:
                cs_items[hash_name] = (None, str(ex))

        return cs_items

    def __get_list_market_data(self, hash_names: [str]) -> dict:  # dict(hash_name: data).
        try:
            print('Asking cs market...')
            item_datas = self.__market.search_list_items_by_hash_name_all(list_hash_name=hash_names)['data']

            print('Cs market responded, parsing...')
            cs_items = {}

            for item_data in item_datas:
                cs_items[item_data] = item_datas[item_data]

            return cs_items
        except Exception as ex:
            raise ex

    def __parse_item(self, hash_name: str, buff_data: dict, market_data: dict) -> CsItem:
        if buff_data is None:
            return CsItem(hash_name=hash_name, error='Buff data is None.')

        if market_data is None:
            return CsItem(hash_name=hash_name, error='Market data is None.')

        buff_url = f'https://buff.163.com/goods/{self.__get_buff_id_by_hash(hash_name=hash_name)}'

        # Get min buff price.
        if 'price' in buff_data.keys():
            buff_price = float(buff_data['price'])
        else:
            buff_price = float(buff_data['sell_min_price'])

        # Market data can be empty if there is no items on market.
        if len(market_data) > 0:
            market_price = float(int(market_data[0]['price']) / 100)
            return CsItem(hash_name=hash_name, buff_url=buff_url, buff_price=buff_price, market_price=market_price)
        else:
            return CsItem(hash_name=hash_name, error='No such item on cs market.')

    def scan_item(self, hash_name: str) -> CsItem:  # Return parsed or error CsItem
        buff_data, buff_error = self.__get_item_buff_data(hash_name=hash_name)

        if buff_error is not None:
            return CsItem(hash_name=hash_name, error=buff_error)

        market_data, market_error = self.__get_item_market_data(hash_name=hash_name)

        if market_error is not None:
            return CsItem(hash_name=hash_name, error=market_error)

        return self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data)

    def scan_list(self, list_name: str) -> CsItemsList:
        hash_names = ItemsScaner.get_hashes_by_scan_list_name(list_name)

        if hash_names is None:
            return CsItemsList(list_name=list_name, error='List name was not found.')

        buff_items_dict = self.__get_list_buff_data(hash_names=hash_names)

        try:
            market_items_dict = self.__get_list_market_data(hash_names=hash_names)
        except Exception as ex:
            return CsItemsList(list_name=list_name, error=str(ex))

        cs_items = []

        for hash_name in hash_names:
            buff_data, buff_error = buff_items_dict[hash_name]

            if buff_error is not None:
                cs_items.append(CsItem(hash_name=hash_name, error=buff_error))
            else:
                market_data = market_items_dict[hash_name]
                cs_items.append(self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data))

        return CsItemsList(list_name=list_name, items=cs_items)

    def scan_next_page(self) -> CsItemsList:
        list_name = f'Buff page {self.__buff_page}'

        # Scan buff.
        try:
            buff_datas = ItemsScaner.__get_buff_page_data(page=self.__buff_page)
        except Exception as ex:
            return CsItemsList(list_name=list_name, error=str(ex))

        hash_names = [hash_name['market_hash_name'] for hash_name in buff_datas]

        # Scan market.
        try:
            market_datas = self.__get_list_market_data(hash_names=hash_names)
        except Exception as ex:
            return CsItemsList(list_name=list_name, error=str(ex))

        cs_items = []

        for i in range(len(hash_names)-1):
            hash_name = hash_names[i]
            buff_data = buff_datas[i]
            market_data = market_datas[hash_name] if hash_name in market_datas.keys() else None

            cs_items.append(self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data))

        print(f'Buff page {self.__buff_page} was scanned, sleeping...')
        self.__buff_page += 1
        ItemsScaner.__sleep()
        return CsItemsList(list_name=list_name, items=cs_items)

    @staticmethod
    def get_hashes_by_scan_list_name(scan_list_name: str):
        list_file = f'{ScanerConfig.SCAN_LISTS_FOLDER_NAME}/{scan_list_name}.txt'

        try:
            file_lines = open(list_file, 'r', encoding="utf8").readlines()
        except Exception:
            return None

        return [line.replace('\n', '') for line in file_lines]

    @staticmethod
    def __get_buff_page_data(page: int) -> dict:  # Returns (dict(hash: buff_data))
        items = dict()
        params = ScanerConfig.BUFF_PARAMS
        params['page_num'] = page

        try:
            buff_response = requests.get(ScanerConfig.BUFF_URL_SALE, params=params, cookies=ScanerConfig.BUFF_COOKIES,
                                         headers=ScanerConfig.BUFF_HEADERS)
            buff_json_load = json.loads(buff_response.text)

            if buff_json_load['code'] == 'OK':
                item_datas = buff_json_load['data']['items']

                for item_data in item_datas:
                    items[item_data['market_hash_name']] = item_data

                return item_datas

            else:
                raise Exception(f'Buff request is failure {buff_json_load}')
        except Exception as ex:
            raise ex

    @staticmethod
    def __sleep():
        time.sleep(random.randrange(ScanerConfig.AUTO_SCAN_TIMEOUT_MIN, ScanerConfig.AUTO_SCAN_TIMEOUT_MAX))
