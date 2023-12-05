from datetime import datetime

import constants
from constants import ConstantCommands
from constants import ConstantExceptions
from UtilClasses.itemsstorage import ItemsStorage
from UtilClasses.consolemanager import ConsoleManager, UserRequest
from UtilClasses.itemsscaner import ItemsScaner, ItemsScanerException
from UtilClasses.configloader import ConfigLoader, ConfigException


class Main:
    def __init__(self):
        if not self.__setup():
            input('Enter any message to exit')
            exit()

        # Commands have their own methods.
        self.__command_methods = {
            ConstantCommands.COMMAND_DIE: self.__die,
            ConstantCommands.COMMAND_ANALYZE_ITEM: self.__analyze_item,
            ConstantCommands.COMMAND_ANALYZE_PAGES: self.__analyze_pages,
            ConstantCommands.COMMAND_STORAGE_INFO: self.__storage_info,
            ConstantCommands.COMMAND_SAVE_CSV: self.__storage_save_csv,
            ConstantCommands.COMMAND_SAVE_EXCEL: self.__storage_save_excel,
            ConstantCommands.COMMAND_STORAGE_LOAD: self.__storage_load,
            ConstantCommands.COMMAND_HELP: self.__help,
        }

        ConsoleManager.print('BuffScaner initialized')

    def work(self):
        """
        Runs endless loop and does BuffScaner job.
        :return: None
        """
        while True:
            self.__handle_command()

    def __analyze_item(self, user_request: UserRequest):
        """
        /analyze_item
        """
        if len(user_request.command_args) == 0:
            ConsoleManager.print(ConstantExceptions.MISSING_ARGUMENT)
            return

        item_hash = user_request.command_arg

        try:
            cs_item = self.__scaner.scan_item(hash_name=item_hash)
        except ItemsScanerException as exception:
            ConsoleManager.print(str(exception))
            return

        self.__storage.add_item(item=cs_item)
        ConsoleManager.print(cs_item)

    def __analyze_pages(self, user_request: UserRequest) -> str:
        """
        /analyze_pages
        """
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
            except ItemsScanerException as exception:
                ConsoleManager.print(f'Exception raised during scanning page {i}: {exception}')
                continue

            self.__storage.add_items(page_list)
            ConsoleManager.print(f'Buff page {i} was parsed and moved into storage.')

            if i % self.__config_loader.scanned_pages_to_autosave == 0:
                self.__storage.save_csv('autosave')
                ConsoleManager.print('Storage was auto saved.')

        return f'Buff pages scan complete. {page_index} pages was scanned.'

    def __storage_info(self, user_request: UserRequest):
        """
        /storage
        """
        ConsoleManager.print(self.__storage)

    def __storage_save_csv(self, user_request: UserRequest):
        """
        /save_csv
        """
        if len(user_request.command_args) == 0:
            ConsoleManager.print(ConstantExceptions.MISSING_ARGUMENT)

        ConsoleManager.print(self.__storage.save_csv(file_name=user_request.command_arg))

    def __storage_save_excel(self, user_request: UserRequest):
        """
        /save_excel
        """
        if len(user_request.command_args) == 0:
            ConsoleManager.print(ConstantExceptions.MISSING_ARGUMENT)

        ConsoleManager.print(self.__storage.save_excel(file_name=user_request.command_arg))

    def __storage_load(self, user_request: UserRequest):
        """
        /storage_load
        """
        if len(user_request.command_args) == 0:
            ConsoleManager.print(ConstantExceptions.MISSING_ARGUMENT)

        ConsoleManager.print(self.__storage.load(file_name=user_request.command_arg))

    def __execute_user_request(self, user_request: UserRequest):
        """
        Executes given request.
        :return: Request callback.
        """
        request_command = user_request.command

        if request_command in self.__command_methods.keys():
            self.__command_methods[request_command](user_request=user_request)
        else:
            ConsoleManager.print(f'Command "{request_command}" is not supported.')

    def __handle_command(self):
        """
        Listens and executes user command.
        :return: None
        """
        user_request = ConsoleManager.get_input()
        self.__execute_user_request(user_request=user_request)

    def __setup(self) -> bool:
        """
        Loads config and sets up pyCS2trader.
        :return: Is successful?
        """
        try:
            self.__config_loader = ConfigLoader()
        except ConfigException as exception:
            print(exception)
            return False

        try:
            self.__scaner = ItemsScaner(self.__config_loader)
        except ItemsScanerException as exception:
            print(exception)
            return False

        self.__storage = ItemsStorage(self.__config_loader)
        return True

    @staticmethod
    def __die(user_request: UserRequest):
        """
        /die
        """
        exit()

    @staticmethod
    def __help(user_request: UserRequest):
        """
        /help
        """
        ConsoleManager.print(constants.ConstantStrings.HELP_REPLY)


if __name__ == '__main__':
    scaner = Main()
    scaner.work()
