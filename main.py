from constants import ConstantCommands
from constants import ConstantExceptions
from UtilClasses.itemsstorage import ItemsStorage
from UtilClasses.userrequest import UserRequest
from UtilClasses.itemsscaner import ItemsScaner, ScanningException, ScanerInitializationException


class Main:
    def __init__(self):
        if not self.__setup_scaner():
            input()
            exit()

        self.__storage = ItemsStorage()

        # Difficult commands have their own methods.
        self.__command_methods = {
            ConstantCommands.COMMAND_DIE: self.__die,
            ConstantCommands.COMMAND_ANALYZE_ITEM: self.__analyze_item,
            ConstantCommands.COMMAND_ANALYZE_LIST: self.__analyze_list,
            ConstantCommands.COMMAND_ANALYZE_PAGES: self.__analyze_pages,
            ConstantCommands.COMMAND_STORAGE_INFO: self.__storage_info,
            ConstantCommands.COMMAND_STORAGE_PAGE: self.__storage_page,
            ConstantCommands.COMMAND_STORAGE_SORT: self.__storage_sort,
            ConstantCommands.COMMAND_STORAGE_SAVE: self.__storage_save
        }

        print('BuffScaner initialized')

    def work(self):
        """
        Runs endless loop and does BuffScaner job.
        :return: None
        """
        while True:
            self.__handle_command()

    def __analyze_item(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        item_hash = user_request.command_arg

        try:
            cs_item = self.__scaner.scan_item(hash_name=item_hash)
        except ScanningException as exception:
            return str(exception)

        self.__storage.add_item(item=cs_item)
        return repr(cs_item)

    def __analyze_list(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        list_name = user_request.command_arg

        try:
            cs_items_list = self.__scaner.scan_list(list_name=list_name)
        except ScanningException as exception:
            return str(exception)

        self.__storage.add_items(cs_items_list)
        return repr(cs_items_list)

    def __analyze_pages(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        try:
            page_index = int(user_request.command_arg)
        except ValueError:
            return ConstantExceptions.INVALID_ARGUMENT_TYPE

        if page_index < 1:
            return 'Page index can not be < 1.'

        for i in range(1, page_index + 1):
            try:
                page_list = self.__scaner.scan_buff_page(i)
            except ScanningException as exception:
                return f'Exception raised during scanning page {i}: {exception}'

            self.__storage.add_items(page_list)
            print(f'Buff page {i} was parsed and moved into storage.')

        return f'Buff pages scan complete. {page_index} pages was scanned.'

    def __storage_info(self, user_request: UserRequest) -> str:
        return repr(self.__storage)

    def __storage_sort(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        return self.__storage.sort_items(sorting_attribute=user_request.command_arg)

    def __storage_save(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        return self.__storage.save(file_name=user_request.command_arg)

    def __remove_storage_page(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        try:
            page_index = int(user_request.command_arg)
        except ValueError:
            return ConstantExceptions.INVALID_ARGUMENT_TYPE

        return self.__storage.remove_page(page_index=page_index)

    def __storage_page(self, user_request: UserRequest) -> str:
        if len(user_request.command_args) == 0:
            return ConstantExceptions.MISSING_ARGUMENT

        try:
            page_index = int(user_request.command_arg)
        except ValueError:
            return ConstantExceptions.INVALID_ARGUMENT_TYPE

        return self.__storage.get_page_repr(page_index=page_index)

    def __get_request_response(self, user_request: UserRequest) -> str:
        """
        Executes given request.
        :return: Request callback.
        """
        request_command = user_request.command

        if request_command in self.__command_methods.keys():
            return f'\n{self.__command_methods[request_command](user_request=user_request)}'
        else:
            return f'\nCommand "{request_command}" is not supported.'

    def __handle_command(self):
        """
        Listens and executes user command.
        :return: None
        """
        user_request = UserRequest(input())
        response = self.__get_request_response(user_request=user_request)
        print(response)

    def __setup_scaner(self) -> bool:
        """
        Sets up scaner.
        :return: Is successful?
        """
        try:
            self.__scaner = ItemsScaner()
            return True
        except ScanerInitializationException as exception:
            print(exception)
            return False

    @staticmethod
    def __die(user_request: UserRequest):
        exit()


if __name__ == '__main__':
    scaner = Main()
    scaner.work()
