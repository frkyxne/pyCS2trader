from UtilClasses.csitem import CsItem


class CsItemsList:
    def __init__(self, items: [CsItem], list_name: str = None):
        self.__list_name = list_name
        self.__items = items

    def __iter__(self):
        return iter(self.__items)

    def __len__(self):
        return len(self.__items)

    def non_error_items(self):
        return [item for item in self.__items if item.processing_error is None]

    def error_items(self):
        return [item for item in self.__items if item.processing_error is not None]

    def __repr__(self):
        representation = f'{"-"*29}\nCs items list representation.\n\n'

        if self.__list_name is not None:
            representation += f'List name: {self.__list_name}\n'

        representation += f'Non error items: [{len(self.non_error_items())}]\n'

        for non_error_item in self.non_error_items():
            representation += f'-{non_error_item.hash_name}\n'

        representation += f'Error items: [{len(self.error_items())}]\n'

        for error_item in self.error_items():
            representation += f'-{error_item.hash_name}\n'

        representation += '-' * len(representation.split('\n')[-2])
        return representation
