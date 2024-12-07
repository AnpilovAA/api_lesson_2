from json import loads
from urllib.parse import urlparse

from config import TOKEN

from requests import get
from requests.exceptions import HTTPError


def shorten_link(token: str, url: str) -> None:
    response = get(url=url, params=token)
    response.raise_for_status()
    if "error" in loads(response.text):
        """"
        Это условие помогает поймать ошибку в случае введения
        пользователя ссылки в формате xx,ru
        """
        print(f"Код ошибки {response.status_code}, \nтекст: {response.text}")
        raise HTTPError
    short_link = loads(response.text)["response"]["short_url"]
    return short_link


def count_clicks(token: str, url: str):
    response = get(url=url, params=token)
    response.raise_for_status()
    if "error" in loads(response.text):
        """"
        Это условие помогает поймать ошибку в случае введения
        пользователя ссылки в формате xx,ru
        """
        print(f"Код ошибки {response.status_code}\nтекст: {response.text}")
        raise HTTPError
    return loads(response.text)["response"]['stats'][0]["views"]


if __name__ == "__main__":
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": TOKEN,
        # 'url': input("Вставьте ссылку: "),
        'url': "hh.ru",
        'string': "key",
        "private": 0,
        "v": 5.199,
    }
    try:
        short_link = shorten_link(token=params, url=url)
    except HTTPError:
        raise KeyboardInterrupt

    url_stat_method = "https://api.vk.ru/method/utils.getLinkStats"
    params_stat_method = {
        "key": urlparse(short_link).path.strip('/'),
        "access_token": TOKEN,
        "v": 5.199,
    }
    try:
        clicks_count = count_clicks(
            token=params_stat_method,
            url=url_stat_method
        )
    except HTTPError:
        raise KeyboardInterrupt
    print(clicks_count)
