from json import loads

from config import TOKEN

from requests import get
from requests.exceptions import HTTPError


def shorten_link(token: str, url: str) -> None:
    response = get(url=url, params=token)
    response.raise_for_status()
    if "error_code" in loads(response.text)['error']:
        """"
        Это условие помогает поймать ошибку в случае введения
        пользователя ссылки в формате xx,ru
        """
        print(f"Код ошибки {response.status_code}, \nтекст: {response.text}")
        raise HTTPError
    short_link = loads(response.text)["response"]["short_url"]
    return short_link


def count_clicks(token: str, url: str):
    pass


if __name__ == "__main__":
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": TOKEN,
        'url': input("Вставьте ссылку: "),
        'string': "key",
        "private": 0,
        "v": 5.199,
    }
    try:
        short_link = shorten_link(token=params, url=url)
        print("Сокращенная ссылка: ", short_link)
    except HTTPError:
        print("Не правильная ссылка")
