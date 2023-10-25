class ItemsScaner:
    CS_MARKET_API_KEY = '6236Q06gwWwB1Zm81FPUZd98BObfdui'
    BUFF_URL_SALE = 'https://buff.163.com/api/market/goods'
    BUFF_URL_IDS_FILE = 'https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt'

    AUTO_SCAN_TIMEOUT_MIN = 10
    AUTO_SCAN_TIMEOUT_MAX = 13
    AUTO_SCAN_DO = False

    BUFF_COOKIES = {
        'Device-Id': 'DxOuNxr6QYqhI1OP4Pej',
        'Locale-Supported': 'en',
        'game': 'csgo',
        'AQ_HD': '1',
        'YD_SC_SID': 'XXX',
        'NETS_utid': 'XXX',
        'NTES_YD_SESS': 'jHq_7VcML_g6tSje.3gx.78rCTnPqBrVhvOEqqdpIKUNT7Ap0cd2Fkdpfmn7eC5XuJ4OlHFTBKXnDMSSJ9ToRj5unCvDxboeUCm4lx3TrJQdIVgJODzaeG.bCvHJTQN1a9DW9AVLxv1jts5VSYpKd1K3VCjYNT0nxFC6qucjAhUl8AHXjKEaaWSjML0K3gSGsBp5Ne2QGeUhkJ5eFaURqsii4y_6dH508V46kPtqfxW3Q',
        'S_INFO': '1696835338|0|0&60##|7-9918096329',
        'P_INFO': '7-9918096329|1696835338|1|netease_buff|00&99|null&null&null#RU&null#10#0|&0||7-9918096329',
        'remember_me': 'U1077865208|4oxBIHY0fZWd63GlZHQiSqR88P1lRfW0',
        'session': '1-kuBGr2Wqq0qtwQkPO84LLbJ0Tj_QSomjEvCSusjKj_5q2029024672',
        'csrf_token': 'IjJiY2U3MTFkZGJmZDRiMTUyZGNlNjA5ODVhYWJkODkxZTRjMjdiZDMi.GAZwOA.DnE4_HhuHbaAlyVL0P7gQMgj8gg',
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

    SCAN_LISTS_FOLDER_NAME = 'F:/Code/GitHubRepositories/buffscaner/Scan lists'