class ItemStorage:
    EXCEPTION_STORAGE_EMPTY = 'Storage is empty :('

    SORTING_ATTRIBUTE_PROFIT_RUB = 'rub'
    SORTING_ATTRIBUTE_PERCENT = 'percent'
    SORTING_ATTRIBUTE_COST_PRICE = 'cost_price'


class TelegramBot:
    COMMAND_START = '/start'
    COMMAND_HELP = '/help'
    COMMAND_ANALYZE_ITEM = '/analyze_item'
    COMMAND_ANALYZE_LIST = '/analyze_list'
    COMMAND_ANALYZE_PAGES = '/analyze_pages'
    COMMAND_DIE = '/die'
    COMMAND_STORAGE_INFO = '/storage'
    COMMAND_STORAGE_CLEAR = '/storage_clear'
    COMMAND_STORAGE_REMOVE_PAGE = '/storage_remove_page'
    COMMAND_STORAGE_PAGE = '/storage_page'
    COMMAND_STORAGE_SORT = '/storage_sort'
    COMMAND_STORAGE_SAVE = '/storage_save'

    REPLY_TO_NOT_ADMIN = 'This bot is private. You are not in admins list :('
    REPLY_START = 'Hello, friendo. Type /help to get info.'

    REPLY_HELP = ('/help - all supported commands info.\n'
                  '/analyze_item {item_hash} - analyze item by hash.\n'
                  '/analyze_list {list_name} - analyze list of items by list name.\n'
                  '/analyze_pages {pages_count} - analyze buff pages.\n'
                  '/die - kill bot.\n'
                  '/storage - show storage data.\n'
                  '/storage_clear - clear storage data.\n'
                  '/storage_remove_page {page index} - remove page items from storage.\n'
                  '/storage_page {page index} - show storage page. Index starts from 1.\n'
                  '/storage_sort {rub/percent/cost_price} - sort items storage.\n'
                  '/storage_save {file name}- save storage as .scv file.')

    FAST_REPLY_DICTIONARY = {COMMAND_START: REPLY_START,
                             COMMAND_HELP: REPLY_HELP}

    SUPPORTED_COMMANDS = (COMMAND_START, COMMAND_HELP, COMMAND_DIE,
                          COMMAND_ANALYZE_ITEM, COMMAND_ANALYZE_LIST, COMMAND_ANALYZE_PAGES,
                          COMMAND_STORAGE_INFO, COMMAND_STORAGE_CLEAR, COMMAND_STORAGE_PAGE, COMMAND_STORAGE_SORT,
                          COMMAND_STORAGE_REMOVE_PAGE, COMMAND_STORAGE_SAVE)
