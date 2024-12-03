from json import loads


from api_lesson_2.config import TOKEN


from requests import get
from requests.exceptions import HTTPError


def short_link(token: str, url: str) -> None:
    try:
        response = get(url=url, params=token)
        response.raise_for_status()
        short_link = loads(response.text)["response"]["short_url"]
        return short_link
    except HTTPError:
        print(response.status_code, "Код ошибки")


if __name__ == "__main__":
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": TOKEN,
        'url': input("Вставьте ссылку: "),
        'string': "key",
        "private": 0,
        "v": 5.199,
    }
    print("Сокращённая ссылка: ", short_link(token=params, url=url))
