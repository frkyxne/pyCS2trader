import csv
from UtilClasses.csitem import CsItem
from UtilClasses.csitemlist import CsItemsList
from constants import ItemStorage as StorageConstants
from config import ItemsStorage as StorageConfig


class ItemsStorage:
    def __init__(self):
        self.__items = []

    def __repr__(self):
        representation = f'{"-"*29}\nItems storage representation.\n\n'

        items_len = len(self.__items)
        representation += f'Items in storage: [{items_len}] ([{self.pages_count}] pages).'

        representation += '\n' + '-' * len(representation.split('\n')[-1])
        return representation

    @property
    def pages_count(self) -> int:
        return (len(self.__items) // StorageConfig.PAGE_ITEMS_COUNT +
                (1 if len(self.__items) % StorageConfig.PAGE_ITEMS_COUNT != 0 else 0))

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

    def save(self, file_name: str) -> str:
        """
        Saves all items in .csv file.
        :param file_name: Name of save file.
        :return: Callback of operation.
        """
        try:
            with (open(f'{StorageConfig.STORAGE_SAVES_FOLDER_NAME}/{file_name}.csv', 'w', encoding='UTF8', newline='')
                  as file):
                writer = csv.writer(file)
                writer.writerow(StorageConfig.STORAGE_SAVE_HEADER)

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
