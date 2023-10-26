import csv
from UtilClasses.CsItem import CsItem
from UtilClasses.CsItemList import CsItemsList
from constants import ItemStorage as StorageConstants
from config import ItemsStorage as StorageConfig


class ItemsStorage:
    def __init__(self):
        self.__items = []

    def __repr__(self):
        representation = 'Items storage representation.\n\n'

        items_len = len(self.__items)
        representation += f'Items in storage: [{items_len}] ([{self.pages_count}] pages).\n'

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

        for item in items:
            self.add_item(item)

    def remove_page(self, page_index: int) -> str:
        """
        Tries to remove page from storage.
        :param page_index: Index of page to delete.
        :return: Callback of operation.
        """
        if page_index < self.pages_count:
            return 'Page index is lower than storage pages count.'

        for page_item in self.__get_items_by_page(page_index=page_index):
            self.__items.remove(page_item)

        return 'Page items were removed from storage.'

    def clear(self):
        """
        Removes all items from storage.
        :return: None
        """
        self.__items.clear()

    def get_page_repr(self, page_index: int) -> str:
        """
        :param page_index: Index of page to represent.
        :return: Representation of storage page.
        """
        if len(self.__items) == 0:
            return StorageConstants.EXCEPTION_STORAGE_EMPTY

        return self.__get_page_repr(page_index=page_index)

    def sort_items(self, sorting_attribute: str) -> str:
        """
        Tries to sort storage by given attribute.
        :param sorting_attribute: Attribute to sort by.
        :return: Callback of operation.
        """
        if len(self.__items) == 0:
            return StorageConstants.EXCEPTION_STORAGE_EMPTY

        match sorting_attribute:
            case StorageConstants.SORTING_ATTRIBUTE_PROFIT_RUB:
                self.__items.sort(key=lambda x: x.profit_rub, reverse=True)
            case StorageConstants.SORTING_ATTRIBUTE_PERCENT:
                self.__items.sort(key=lambda x: x.profit_percent, reverse=True)
            case StorageConstants.SORTING_ATTRIBUTE_COST_PRICE:
                self.__items.sort(key=lambda x: x.buff_cost_price, reverse=True)
            case _:
                return f'Sorting attribute "{sorting_attribute}" is not supported.'

        return f'Storage was sorted by: {sorting_attribute}.'

    def save(self, file_name: str):
        """
        Saves all items in .csv file.
        :param file_name: Name of save file.
        :return: None
        """
        with (open(f'{StorageConfig.STORAGE_SAVES_FOLDER_NAME}/{file_name}.csv', 'w', encoding='UTF8', newline='')
              as file):
            writer = csv.writer(file)
            writer.writerow(StorageConfig.STORAGE_SAVE_HEADER)

            for item in self.__items:
                writer.writerow(item.properties_array)

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

    def __get_items_by_page(self, page_index) -> [CsItem]:
        """
        Tries to get items on given page.
        :param page_index: Page index to search items on.
        :return: Empty array or [CsItem] array.
        """
        if page_index > self.pages_count:
            return []

        items = []
        start_index = (page_index - 1) * StorageConfig.PAGE_ITEMS_COUNT
        end_index = start_index + StorageConfig.PAGE_ITEMS_COUNT

        if len(self.__items) < end_index:
            end_index = len(self.__items) - 1

        for i in range(start_index, end_index + 1):
            items.append(self.__items[i])

        return items

    def __get_page_repr(self, page_index) -> str:
        """
        Makes representation of given page.
        :param page_index: Index of page to represent.
        :return: str
        """
        if page_index > self.pages_count:
            return 'Page index is more than storage has.'

        representation = f'Storage page [{page_index}]:\n'

        for page_item in self.__get_items_by_page(page_index=page_index):
            representation += page_item.short_repr + '\n\n'

        return representation
