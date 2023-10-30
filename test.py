import urllib.parse
import requests
import json
from config import ItemsScaner as ScanerConfig


def ask_buff_page():
    BUFF_COOKIES = {'session': '1-XWTZrUcNaBdoHvCDlLZWWBgOPVKtepGbyxRwF5OUpwPI2029024672'}
    BUFF_PARAMS = {
        'game': 'csgo',
        'page_num': '2',
    }
    buff_response = requests.get(ScanerConfig.BUFF_URL_SALE, params=BUFF_PARAMS, cookies=BUFF_COOKIES)
    buff_response.close()
    print(buff_response.text)
    json_load = json.loads(buff_response.text)
    print(json_load)
    print(type(json_load))


def ask_buff_item():
    BUFF_COOKIES = {'session': '1-XWTZrUcNaBdoHvCDlLZWWBgOPVKtepGbyxRwF5OUpwPI2029024672'}

    params = {
        'game': 'csgo',
        'page_num': '1',
        'goods_id': 33813
    }

    buff_item_url = f'{ScanerConfig.BUFF_URL_SALE}/sell_order?{urllib.parse.urlencode(params)}'

    buff_response = requests.get(url=buff_item_url, cookies=BUFF_COOKIES)

    # Parse response.
    buff_json_load = json.loads(buff_response.text)
    buff_response.close()
    print(buff_response.text)


ask_buff_item()