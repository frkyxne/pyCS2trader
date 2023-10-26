from UtilClasses.CsItem import CsItem


class CsItemsList:
    def __init__(self, list_name: str = None, items: [CsItem] = None, error: str = None):
        self.__list_name = list_name
        self.__items = items
        self.__error = error

    def __iter__(self):
        return iter(self.__items)

    def __len__(self):
        if self.__items is None:
            return 0

        return len(self.__items)

    def non_error_items(self):
        if self.__items is None:
            return None

        return [item for item in self.__items if item.processing_error is None]

    def error_items(self):
        if self.__items is None:
            return None

        return [item for item in self.__items if item.processing_error is not None]

    def __repr__(self):
        representation = 'Cs items list representation.\n\n'

        if self.__list_name is not None:
            representation += f'List name: {self.__list_name}\n'

        if self.__error is not None:
            representation += f'Error: {self.__error}\n'

        if self.__items is None:
            return representation

        representation += f'Non error items: [{len(self.non_error_items())}]\n'

        for non_error_item in self.non_error_items():
            representation += f'-{non_error_item.hash_name}\n'

        representation += f'Error items: [{len(self.error_items())}]\n'

        for error_item in self.error_items():
            representation += f'-{error_item.hash_name}\n'

        return representation
