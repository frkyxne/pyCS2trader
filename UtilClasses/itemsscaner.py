import os
import json
import time
import random
import urllib.parse
import requests
from FOREIGN.csmarketapi import CsMarket
from UtilClasses.csitem import CsItem
from UtilClasses.csitemlist import CsItemsList
from UtilClasses.configloader import ConfigLoader


class ItemsScaner:
    def __init__(self, config_loader: ConfigLoader):
        self.__market = None
        self.__request_timeout_min = None
        self.__request_timeout_max = None
        self.__buff_session = None
        self.__rub_to_cny_ratio = None

        try:
            self.load_config(config_loader=config_loader)
            self.__set_buff_ids()
        except Exception as exception:
            raise ScanerInitializationException(f'Failed to initialize ItemsScaner: {exception}')

    def load_config(self, config_loader: ConfigLoader):
        self.__market = CsMarket(api_key=config_loader.cs_market_api_key)
        self.__buff_session = config_loader.buff_session
        self.__request_timeout_min = config_loader.request_timeout_min
        self.__request_timeout_max = config_loader.request_timeout_max
        self.__rub_to_cny_ratio = config_loader.rub_to_cny_ratio

    def scan_item(self, hash_name: str) -> CsItem:
        """
        Scans buff and market for item by hash name.
        :param hash_name: Hash name of sought-for item.
        :return: Parsed CsItem.
        """
        try:
            buff_data = self.__get_item_buff_data(hash_name=hash_name)
        except BuffRequestFailure as exception:
            raise ScanningException(exception)

        try:
            market_data = self.__get_item_market_data(hash_name=hash_name)
        except MarketRequestFailure as exception:
            return CsItem(hash_name=hash_name, error=str(exception))

        try:
            cs_item = self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data)
        except ParsingFailure as exception:
            cs_item = CsItem(hash_name=hash_name, error=str(exception))

        return cs_item

    def scan_list(self, list_name: str) -> CsItemsList:
        """
        Scans buff and market for items by saved list name. ScanningException can be raised.
        :param list_name: Name of saved list.
        :return: Parsed CsItemsList.
        """
        try:
            hash_names = ItemsScaner.__get_hashes_by_scan_list_name(list_name)
        except FileNotFoundError:
            raise ScanningException('List file was not found.')

        buff_items_dict = self.__get_list_buff_data(hash_names=hash_names)

        non_error_hashes = []
        error_items = []

        for hash_name in buff_items_dict.keys():
            # If data is string, it is an error (Check __get_list_buff_data).
            if type(buff_items_dict[hash_name]) is str:
                error_items.append(CsItem(hash_name=hash_name, error=buff_items_dict[hash_name]))
            else:
                non_error_hashes.append(hash_name)

        try:
            market_items_dict = self.__get_list_market_data(hash_names=non_error_hashes)
        except MarketRequestFailure as exception:
            raise ScanningException(exception)

        cs_items = []

        for hash_name in non_error_hashes:
            buff_data = buff_items_dict[hash_name]
            market_data = market_items_dict[hash_name]

            try:
                cs_items.append(self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data))
            except ParsingFailure as exception:
                error_items.append(CsItem(hash_name=hash_name, error=str(exception)))

        cs_items.extend(error_items)

        return CsItemsList(list_name=list_name, items=cs_items)

    def scan_buff_page(self, page_index: int) -> CsItemsList:
        """
        Scans buff page and returns parsed CsItemsList. ScanningException can be raised.
        :param page_index: Index of Buff page to parse.
        :return: Parsed CsItemsList.
        """
        # Scan buff.
        try:
            buff_datas = self.__get_buff_page_data(page_index=page_index)
        except BuffRequestFailure as exception:
            raise ScanningException(str(exception))

        # Get hash names in buff datas.
        hash_names = [hash_name['market_hash_name'] for hash_name in buff_datas]

        # Scan market.
        try:
            market_datas = self.__get_list_market_data(hash_names=hash_names)
        except MarketRequestFailure as exception:
            raise ScanningException(str(exception))
        cs_items = []
        for i in range(len(hash_names) - 1):
            hash_name = hash_names[i]
            buff_data = buff_datas[i]
            market_data = market_datas[hash_name] if hash_name in market_datas.keys() else None

            try:
                cs_items.append(self.__parse_item(hash_name=hash_name, buff_data=buff_data, market_data=market_data))
            except ParsingFailure as exception:
                cs_items.append(CsItem(hash_name=hash_name, error=str(exception)))

        self.__sleep()
        return CsItemsList(items=cs_items)

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

    def __get_item_buff_data(self, hash_name: str, do_timeout: bool = False) -> dict:
        """
        Returns raw buff data by hash_name. BuffRequestFailure can be raised.
        :param hash_name: Hash name of sought-for item.
        :param do_timeout: Do timeout after asking buff?
        :return: Raw buff data typeof dict.
        """
        try:
            buff_id = self.__get_buff_id_by_hash(hash_name=hash_name)
        except KeyError:
            raise BuffRequestFailure('Buff id was now found.')

        # Scan buff.
        params = {
            'game': 'csgo',
            'page_num': '1',
            'goods_id': buff_id
        }

        buff_item_url = f'https://buff.163.com/api/market/goods/sell_order?{urllib.parse.urlencode(params)}'

        # Trying to get buff response.
        buff_cookies = {'session': self.__buff_session}

        try:
            buff_response = requests.get(url=buff_item_url, cookies=buff_cookies)
        except Exception as exception:
            raise BuffRequestFailure(f'Failed to get buff response: {exception}')

        # Parse response.
        buff_json_load = json.loads(buff_response.text)
        buff_response.close()

        # Does buff response is error?
        if buff_json_load['code'] != 'OK':
            raise BuffRequestFailure(f'Buff response is an error: {buff_json_load["data"]}.')

        # Do timeout if necessary.
        if do_timeout:
            print(f'Buff asked for {hash_name}, sleeping...')
            self.__sleep()

        # Buff response is successful.
        return buff_json_load['data']['items'][0]

    def __get_list_buff_data(self, hash_names: [str]) -> dict:
        """
        Gradually requests buff for items by hash names in given dictionary. If request for item failed,
        data will be string of exception.
        :param hash_names: list of hash names to search for.
        :return: Dictionary[hash name] = data.
        """
        cs_items = dict()

        for hash_name in hash_names:
            try:
                buff_data = self.__get_item_buff_data(hash_name=hash_name, do_timeout=True)
                cs_items[hash_name] = buff_data
            except BuffRequestFailure as exception:
                cs_items[hash_name] = str(exception)

        return cs_items

    def __get_buff_page_data(self, page_index: int) -> dict:
        """
        Returns raw buff data by page index BuffRequestFailure can be raised.
        :param page_index: Index of parsing page.
        :return: Raw buff page data.
        """
        items = dict()

        goods_url = 'https://buff.163.com/api/market/goods'
        params = {'game': 'csgo', 'page_num': page_index}
        cookies = {'session': self.__buff_session}

        try:
            buff_response = requests.get(goods_url, params=params, cookies=cookies)
            buff_json_load = json.loads(buff_response.text)

            if buff_json_load['code'] == 'OK':
                item_datas = buff_json_load['data']['items']

                for item_data in item_datas:
                    items[item_data['market_hash_name']] = item_data

                return item_datas
            else:
                raise BuffRequestFailure(f'Buff request is failure {buff_json_load}')
        except Exception as ex:
            raise BuffRequestFailure(f'Failed to request buff for page {page_index}: {ex}')

    def __get_item_market_data(self, hash_name: str) -> dict:
        """
        Requests market for item data by item hash name. MarketRequestFailure can be raised.
        :param hash_name: Hash name of sought-for item.
        :return: Raw market data typeof dict.
        """
        try:
            return self.__market.search_item_by_hash_name(hash_name=hash_name)['data']
        except Exception as exception:
            raise MarketRequestFailure(exception)

    def __get_list_market_data(self, hash_names: [str]) -> dict:
        """
        Requests market for items by hash names in given dictionary. If request for item failed,
        MarketRequestFailure is raised.
        :param hash_names: list of hash names to search for.
        :return: Dictionary[hash name] = data.
        """
        try:
            item_datas = self.__market.search_list_items_by_hash_name_all(list_hash_name=hash_names)['data']
            cs_items = {}

            for item_data in item_datas:
                cs_items[item_data] = item_datas[item_data]

            return cs_items
        except Exception as exception:
            raise MarketRequestFailure(exception)

    def __parse_item(self, hash_name: str, buff_data: dict, market_data: dict) -> CsItem:
        """
        Parses buff & market datas into CsItem. ParsingFailure can be raised.
        :param hash_name: Hash name of sought-for item.
        :param buff_data: Buff data of sought-for item to parse.
        :param market_data: Market data of sought-for item to parse.
        :return: Parsed CsItem.
        """
        # try:
        #     buff_url = f'https://buff.163.com/goods/{self.__get_buff_id_by_hash(hash_name=hash_name)}'
        # except KeyError:
        #     raise ParsingFailure('Buff id was now found.')

        # Get min buff price.
        try:
            if 'price' in buff_data.keys():
                buff_price = float(buff_data['price'])
            else:
                buff_price = float(buff_data['sell_min_price'])
        except KeyError:
            raise ParsingFailure('Failed to parse buff data.')

        # Market data can be empty if there is no items on market.
        if market_data is not None and len(market_data) > 0:
            try:
                market_price = float(int(market_data[0]['price']) / 100)
            except KeyError:
                raise ParsingFailure('Failed to parse market data.')

            return CsItem(hash_name=hash_name, buff_price=buff_price, market_price=market_price,
                          rub_to_cny=self.__rub_to_cny_ratio)
        else:
            return CsItem(hash_name=hash_name, error='No such item on cs market.')

    def __sleep(self):
        """
        Makes timeout with random duration.
        :return: None
        """
        time.sleep(random.randrange(self.__request_timeout_min, self.__request_timeout_max))

    @staticmethod
    def __get_hashes_by_scan_list_name(scan_list_name: str):
        scaner_path = os.path.realpath('__file__')
        s = scaner_path.split('\\')
        lists_folder = scaner_path.replace(f'{s[-1]}', '')
        list_file = f'{lists_folder}Scan lists\\{scan_list_name}.txt'

        try:
            file_lines = open(list_file, 'r', encoding="utf8").readlines()
        except FileNotFoundError:
            raise FileNotFoundError

        return [line.replace('\n', '') for line in file_lines]


# Exceptions

class ScanerInitializationException(Exception):
    pass


class BuffRequestFailure(Exception):
    pass


class BuffParseFailure(Exception):
    pass


class MarketRequestFailure(Exception):
    pass


class ScanningException(Exception):
    pass


class ParsingFailure(Exception):
    pass
