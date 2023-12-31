import csv
import os
from UtilClasses.csitem import CsItem
from UtilClasses.csitemlist import CsItemsList
from UtilClasses.configloader import ConfigLoader


class ItemsStorage:
    def __init__(self, config_loader: ConfigLoader):
        self.__items = []
        self.__rub_to_cny = config_loader.rub_to_cny_ratio

    def __repr__(self):
        representation = f'{"-" * 29}\nItems storage representation.\n\n'

        items_len = len(self.__items)
        representation += f'Items in storage: [{items_len}]'

        representation += '\n' + '-' * len(representation.split('\n')[-1])
        return representation

    def add_item(self, item: CsItem):
        """
        Adds item to storage.
        :param item: CsItem to add.
        :return: None
        """
        if item.processing_error is not None:
            return

        existing_good = self.__get_item_by_hash(item.hash_name)

        if existing_good is not None:
            self.__items.remove(existing_good)

        self.__items.append(item)

    def add_items(self, items: CsItemsList):
        """
        Adds items list to storage.
        :param items: CsItemsList to add.
        :return: None
        """
        if items is None or len(items) == 0:
            return

        for item in items.non_error_items():
            self.add_item(item)

    def clear(self):
        """
        Removes all items from storage.
        :return: None
        """
        self.__items.clear()

    def load(self, file_name: str):
        """
        Loads .csv data to storage.
        :param file_name: Name of save file.
        :return: Callback of operation.
        """
        try:
            save_lines = open(f'{self.__saves_folder()}/{file_name}.csv', 'r', encoding='UTF8').readlines()
        except FileNotFoundError as exception:
            return f'During storage load exception raised: {exception}'

        # Remove header
        save_lines.pop(0)

        try:
            for save_line in save_lines:
                s = save_line.split(',')
                self.add_item(CsItem(hash_name=s[0], buff_price=float(s[1]), market_price=float(s[3]),
                                     rub_to_cny=self.__rub_to_cny))
        except ValueError as exception:
            return f'During parsing of load file exception raised: {exception}'

        return f'Items from {file_name}.csv were added successfully.'

    def save(self, file_name: str) -> str:
        """
        Saves all items in .csv file.
        :param file_name: Name of save file.
        :return: Callback of operation.
        """
        header = ['hash_name', 'buff_cny_price', 'buff_rub_price', 'market_price', 'rub to cny',
                  'profit_percent']

        try:
            with (open(f'{self.__saves_folder()}/{file_name}.csv', 'w', encoding='UTF8', newline='')
                  as file):
                writer = csv.writer(file)
                writer.writerow(header)

                for item in self.__items:
                    writer.writerow(item.properties_array)

        except Exception as exception:
            return f'During storage save exception occurred: {exception}'

        return 'Storage saved.'

    def __get_item_by_hash(self, hash_name: str):
        """
        Gets item by hash in storage. If there is none, returns None.
        :param hash_name: Hash name of sought-for item.
        :return: CsItem | None.
        """
        for good in self.__items:
            if good.hash_name == hash_name:
                return good
        return None

    @staticmethod
    def __saves_folder() -> str:
        loader_path = os.path.abspath(__file__)
        s = loader_path.split('\\')
        return loader_path.replace(f'{s[-2]}\\{s[-1]}', '') + 'Storage saves'
