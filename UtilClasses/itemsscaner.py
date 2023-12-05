import os
import time
import random
from UtilClasses.buffparser import BuffParser, BuffParserException
from UtilClasses.csmarketparser import CsMarketParser, CsMarketException
from UtilClasses.csitem import CsItem
from UtilClasses.configloader import ConfigLoader


class ItemsScaner:
    def __init__(self, config_loader: ConfigLoader):
        try:
            self.__buff_parser = BuffParser(session=config_loader.buff_session)
        except BuffParserException as exception:
            raise ItemsScanerException(exception)

        try:
            self.__market_parser = CsMarketParser(api_key=config_loader.cs_market_api_key)
        except CsMarketException as exception:
            raise ItemsScanerException(exception)

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
            buff_item = self.__buff_parser.get_item_data(hash_name=hash_name)
        except BuffParserException as exception:
            raise ItemsScanerException(exception)

        try:
            market_item = self.__market_parser.get_item_data(hash_name=hash_name)
        except CsMarketException as exception:
            raise ItemsScanerException(exception)

        return CsItem(hash_name=hash_name, buff_price=buff_item.buff_price, market_price=market_item.market_price,
                      rub_to_cny=self.__rub_to_cny_ratio)

    def scan_buff_page(self, page_index: int) -> [CsItem]:
        try:
            buff_items = self.__buff_parser.get_page_data(page_index=page_index)
        except BuffParserException as exception:
            raise ItemsScanerException(exception)

        hash_names = [buff_item.hash_name for buff_item in buff_items]

        try:
            market_items = self.__market_parser.get_items_data(hash_names=hash_names)
        except CsMarketException as exception:
            raise ItemsScanerException(exception)

        cs_items = []

        for i in range(len(buff_items)):
            hash_name = buff_items[i].hash_name
            buff_price = buff_items[i].buff_price
            market_price = market_items[i].market_price
            cs_items.append(CsItem(hash_name=hash_name, buff_price=buff_price, market_price=market_price,
                                   rub_to_cny=self.__rub_to_cny_ratio))

        self.__sleep()
        return cs_items

    def __sleep(self):
        """
        Makes timeout with random duration.
        :return: None
        """
        time.sleep(random.randrange(self.__request_timeout_min, self.__request_timeout_max))


class ItemsScanerException(Exception):
    pass
