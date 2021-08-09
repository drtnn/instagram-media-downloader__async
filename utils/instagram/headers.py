from data.config import CURRENT_DIR
import json
import random

COOKIE = json.loads(open(CURRENT_DIR + 'utils/instagram/cookies.json', 'r').read())

headers_agent_list = [
    "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"
    " Firefox/41.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"
    " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"
    " Safari/601.3.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"
    " Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
    " Edge/12.246",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
]


def post_headers(referer: str = None):
    cookie = random.choice(COOKIE)
    headers_classic = {
        'authority': 'www.instagram.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'x-ig-www-claim': 'hmac.AR2OIZnV3Xot5AT_boqr-HjjPl9BObBv1RN7LCdlgdQflWvw',
        'sec-ch-ua-mobile': '?0',
        'user-agent': random.choice(headers_agent_list),
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrftoken': 'baJJfHx4oUsVgv7qv1FBLdm7japAtZvB',
        'x-ig-app-id': '936619743392459',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie['cookie']
    }
    if referer:
        headers_classic['referer'] = referer
    # return headers_classic, cookie['username']
    return headers_classic


def story_headers():
    cookie = random.choice(COOKIE)
    return {
        'authority': 'i.instagram.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'accept': '*/*',
        'x-ig-www-claim': 'hmac.AR2OIZnV3Xot5AT_boqr-HjjPl9BObBv1RN7LCdlgdQflWk1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': random.choice(headers_agent_list),
        'x-ig-app-id': '936619743392459',
        'origin': 'https://www.instagram.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.instagram.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie['cookie'],
    }
    # , cookie['username']
