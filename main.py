from json import loads
from urllib.parse import urlparse
from os import environ


from dotenv import load_dotenv, find_dotenv
from requests import get
from requests.exceptions import HTTPError


def shorten_link(token: dict) -> str:
    if is_shorten_link(token['url']):
        return token['url']
    else:
        url = "https://api.vk.ru/method/utils.getShortLink"
        response = get(url=url, params=token)
        response.raise_for_status()
        if "error" in loads(response.text):
            """"
            these conditions help to detect the error
            """
            print(f"Код ошибки {response.status_code}, \nтекст: {response.text}")
            raise HTTPError
        short_link = loads(response.text)["response"]["short_url"]
        return short_link


def count_clicks(token: dict) -> str:
    url = "https://api.vk.ru/method/utils.getLinkStats"
    response = get(url=url, params=token)
    response.raise_for_status()
    if "error" in loads(response.text):
        """"
        these conditions help to detect the error
        """
        print(f"Код ошибки {response.status_code}\nтекст: {response.text}")
        raise HTTPError
    try:
        return loads(response.text)["response"]['stats'][0]["views"]
    except IndexError:
        print("По ссылке еще не было переходов!")


def is_shorten_link(url: str) -> bool:
    if urlparse(url).netloc == "vk.cc":
        return True
    return False


if __name__ == "__main__":
    load_dotenv(dotenv_path=find_dotenv())
    vk_token = environ["VK_TOKEN"]
    params = {
        "access_token": vk_token,
        'url': input("Вставьте ссылку: "),
        'string': "key",
        "private": 0,
        "v": 5.199,
    }
    try:
        short_link = shorten_link(token=params)
        print(short_link)
    except HTTPError:
        raise KeyboardInterrupt

    params_stat_method = {
        "key": urlparse(short_link).path.strip('/'),
        "access_token": vk_token,
        "v": 5.199,
    }
    try:
        clicks_count = count_clicks(token=params_stat_method)
    except HTTPError:
        raise KeyboardInterrupt
    if clicks_count is not None:
        print("Количетсво кликов: ", clicks_count)
    if is_shorten_link(params["url"]):
        print("Ссылка короткая")
    else:
        print("Ссылка длинная")
