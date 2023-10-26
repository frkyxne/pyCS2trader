from constants import TelegramBot as BotConstants
from FOREIGN.TelegramFreak.telegramfreak import TelegramFreak
from FOREIGN.TelegramFreak.utilclasses import UserRequest, BotReply
from UtilClasses.itemsstorage import ItemsStorage
from UtilClasses import itemsscaner


class Main:
    def __init__(self):
        if not self.__setup_telegram_bot():
            input()
            exit()

        if not self.__setup_scaner():
            input()
            exit()

        self.__storage = ItemsStorage()

        # Difficult commands have their own methods.
        self.__command_methods = {
            BotConstants.COMMAND_ANALYZE_ITEM: self.__analyze_item,
            BotConstants.COMMAND_ANALYZE_LIST: self.__analyze_list,
            BotConstants.COMMAND_ANALYZE_PAGES: self.__analyze_pages,
            BotConstants.COMMAND_STORAGE_PAGE: self.__storage_page,
            BotConstants.COMMAND_STORAGE_SORT: self.__storage_sort,
            BotConstants.COMMAND_STORAGE_SAVE: self.__storage_save
        }

    def work(self):
        """
        Runs endless loop and does BuffScaner job.
        :return: None
        """
        # Skip first update to not die from last /die command.
        self.__telegram_bot.get_unserviced_requests()

        while True:
            self.__handle_telegram_commands()

    def __analyze_item(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        self.__send_reply_notification(notification_text='Item scan started.', user_request=user_request)
        cs_item = self.__scaner.scan_item(' '.join(user_request.commands_args))
        self.__storage.add_item(item=cs_item)
        return BotReply(reply_text=repr(cs_item), replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __analyze_list(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        self.__send_reply_notification(notification_text='List scan started.', user_request=user_request)
        cs_items_list = self.__scaner.scan_list(user_request.commands_args[0])

        if cs_items_list.non_error_items() is not None:
            self.__storage.add_items(cs_items_list)

        return BotReply(reply_text=repr(cs_items_list), replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __analyze_pages(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        try:
            page_index = int(user_request.commands_args[0])
        except ValueError:
            return self.__invalid_argument_reply(user_request=user_request)

        if page_index < 1:
            return self.__invalid_argument_reply(user_request=user_request)

        self.__send_reply_notification(notification_text='Buff pages scan started.', user_request=user_request)

        for i in range(1, page_index + 1):
            page_list = self.__scaner.scan_buff_page(i)

            if page_list.non_error_items() is not None:
                self.__storage.add_items(page_list)

        return BotReply(reply_text=f'Buff pages scan complete. {page_index} pages was scanned.',
                        replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __storage_sort(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        storage_callback = self.__storage.sort_items(sorting_attribute=user_request.commands_args[0])
        return BotReply(reply_text=storage_callback, replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __storage_save(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        self.__storage.save(file_name=user_request.commands_args[0])
        return BotReply(reply_text='Storage saved.', replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __remove_storage_page(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        try:
            page_index = int(user_request.commands_args[0])
        except ValueError:
            return self.__invalid_argument_reply(user_request=user_request)

        storage_callback = self.__storage.remove_page(page_index=page_index)
        return BotReply(reply_text=storage_callback, replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __storage_page(self, user_request: UserRequest) -> BotReply:
        if user_request.commands_args is None or len(user_request.commands_args) == 0:
            return self.__invalid_argument_reply(user_request=user_request)

        try:
            page_index = int(user_request.commands_args[0])
        except ValueError:
            return self.__invalid_argument_reply(user_request=user_request)

        storage_callback = self.__storage.get_page_repr(page_index=page_index)
        return BotReply(reply_text=storage_callback, replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __get_request_reply(self, user_request: UserRequest) -> BotReply:
        """
        Gets BuffScaner reply to given request.
        :return: BotReply.
        """
        request_command = user_request.command

        if request_command in BotConstants.FAST_REPLY_DICTIONARY.keys():
            # Command is fast reply, send reply.

            return BotReply(reply_text=BotConstants.FAST_REPLY_DICTIONARY[request_command],
                            replying_message=user_request.message,
                            reply_variants=self.__telegram_bot.supported_commands)

        # Command is complex.
        if request_command in self.__command_methods.keys():
            return self.__command_methods[request_command](user_request=user_request)

        if request_command == BotConstants.COMMAND_DIE:
            self.__send_reply_notification(notification_text='Bot is offline.', user_request=user_request)
            exit()

        if request_command == BotConstants.COMMAND_STORAGE_INFO:
            reply = repr(self.__storage)
        else:
            reply = 'Main does not support this command.'

        return BotReply(reply_text=reply, replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __handle_telegram_commands(self):
        """
        Listens and executes telegram commands.
        :return: None
        """
        for user_request in self.__telegram_bot.get_unserviced_requests():
            self.__telegram_bot.reply_to_message(self.__get_request_reply(user_request=user_request))

    def __invalid_argument_reply(self, user_request: UserRequest):
        """
        Forms invalid argument reply.
        :param user_request: Request with invalid argument.
        :return: BotReply.
        """
        return BotReply(reply_text='Invalid argument.', replying_message=user_request.message,
                        reply_variants=self.__telegram_bot.supported_commands)

    def __send_reply_notification(self, notification_text: str, user_request: UserRequest):
        """
        Sends reply to request with given text.
        :param notification_text: Text of notification.
        :return: None
        """
        self.__telegram_bot.reply_to_message(BotReply(reply_text=notification_text,
                                                      replying_message=user_request.message,
                                                      reply_variants=[]))

    def __setup_telegram_bot(self) -> bool:
        """
        Sets up TelegramFreak.
        :return: Is successful?
        """
        try:
            self.__telegram_bot = TelegramFreak()
        except Exception as exception:
            print(f'Failed to host a telegram bot: {exception}')
            return False

        self.__telegram_bot.supported_commands = BotConstants.SUPPORTED_COMMANDS
        return True

    def __setup_scaner(self) -> bool:
        """
        Sets up scaner.
        :return: Is successful?
        """
        try:
            self.__scaner = itemsscaner.ItemsScaner()
            return True
        except itemsscaner.ScanerInitializationFailure as exception:
            print(exception)
            return False


if __name__ == '__main__':
    scaner = Main()
    scaner.work()
