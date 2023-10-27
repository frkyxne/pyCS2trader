class ItemsScaner:
    CS_MARKET_API_KEY = '6236Q06gwWwB1Zm81FPUZd98BObfdui'
    BUFF_URL_SALE = 'https://buff.163.com/api/market/goods'
    BUFF_URL_IDS_FILE = 'https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt'

    AUTO_SCAN_TIMEOUT_MIN = 10
    AUTO_SCAN_TIMEOUT_MAX = 13

    BUFF_COOKIES = {
        'Device-Id': 'DxOuNxr6QYqhI1OP4Pej',
        'Locale-Supported': 'en',
        'game': 'csgo',
        'AQ_HD': '1',
        'YD_SC_SID': 'XXX',
        'NETS_utid': 'XXX',
        'NTES_YD_SESS': 'XXX',
        'S_INFO': '1696835338|0|0&60##|7-9918096329',
        'P_INFO': '7-9918096329|1696835338|1|netease_buff|00&99|null&null&null#RU&null#10#0|&0||7-9918096329',
        'remember_me': 'U1077865208|PCAhb1iKEByv8cMSTeoe8VbWARrseWrn',
        'session': '1-XWTZrUcNaBdoHvCDlLZWWBgOPVKtepGbyxRwF5OUpwPI2029024672',
        'csrf_token': 'ImVmNjEwZjc5ZWM2YTY1YjE2ZTc2OGFlOTlmMTk5NDdjZWQ5NDQ5OGEi.GBuqCQ.cQrSyNGqMmV8C_K0y1msZfWOfm4',
    }

    BUFF_HEADERS = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://buff.163.com/market/csgo',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36 '
                      'OPR/93.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    BUFF_PARAMS = {
        'game': 'csgo',
        'page_num': '1',
    }

    SCAN_LISTS_FOLDER_NAME = 'F:/Code/GitHubRepositories/BuffScaner/Scan lists'


class ItemsAnalyzer:
    BUFF_DEPOSIT_MODIFIER = 1
    MARKET_WITHDRAW_MODIFIER = 0.9025
    DEPOSIT_RUB_TO_CNY = 14


class ItemsStorage:
    PAGE_ITEMS_COUNT = 5

    STORAGE_SAVES_FOLDER_NAME = 'F:/Code/GitHubRepositories/BuffScaner/Storage saves'
    STORAGE_SAVE_HEADER = ['hash_name', 'buff_cny_price', 'buff_rub_price', 'market_price', 'rub to cny', 'profit_rub',
                           'profit_percent']


class Main:
    PAGES_TO_AUTOSAVE = 100
