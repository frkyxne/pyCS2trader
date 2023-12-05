class ConstantExceptions:
    MISSING_ARGUMENT = 'Missing argument.'
    WRONG_ARGUMENT_SYNTAX = 'Wrong argument syntax.'
    INVALID_ARGUMENT_TYPE = 'Invalid argument type.'


class ConstantCommands:
    COMMAND_ANALYZE_ITEM = '/analyze_item'
    COMMAND_ANALYZE_PAGES = '/analyze_pages'
    COMMAND_DIE = '/die'
    COMMAND_HELP = '/help'
    COMMAND_STORAGE_INFO = '/storage'
    COMMAND_STORAGE_CLEAR = '/storage_clear'
    COMMAND_SAVE_CSV = '/save_csv'
    COMMAND_SAVE_EXCEL = '/save_excel'
    COMMAND_STORAGE_LOAD = '/storage_load'


class ConstantStrings:
    HELP_REPLY = ('Supported commands:\n'
                  '/analyze_item {hash name} - analyze item by hash name.\n'
                  '/analyze_pages {pages count} - analyze given number of pages.\n'
                  '/die - kill pyCS2trader.\n'
                  '/help - show supported commands info.\n'
                  '/storage - show storage representation.\n'
                  '/storage_clear - remove all items from storage.\n'
                  '/save_csv {file name} - save storage as .csv file.\n'
                  '/save_excel {file name} - save storage as .csv file that Excel can correctly read.\n'
                  '/storage_load {file name} - load storage from .csv file.')
