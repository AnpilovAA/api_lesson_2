from urllib.parse import urlparse
from os import environ


from dotenv import load_dotenv, find_dotenv
from requests import get
from requests.exceptions import HTTPError


def shorten_link(token: dict) -> str:
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": token["vk_token"],
        'url': token['url'],
        'string': "key",
        "private": 0,
        "v": 5.199,
        }
    response = get(url=url, params=params)
    response.raise_for_status()
    if "error" in response.json():
        """"
        these conditions help to detect the error
        """
        print(f"Код ошибки {response.status_code}, \nтекст: {response.text}")
        raise HTTPError
    short_link = response.json()["response"]["short_url"]
    return short_link


def count_clicks(token: dict) -> str:
    url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "key": token["short_link"],
        "access_token": token['vk_token'],
        "v": 5.199
        }
    response = get(url=url, params=params)
    response.raise_for_status()
    if "error" in response.json():
        """"
        these conditions help to detect the error
        """
        print(f"Код ошибки {response.status_code}\nтекст: {response.text}")
        raise HTTPError
    try:
        return response.json()["response"]['stats'][0]["views"]
    except IndexError:
        print("По ссылке еще не было переходов!")


def is_shorten_link(url: str) -> bool:
    if urlparse(url).netloc == "vk.cc":
        return True
    return False


if __name__ == "__main__":
    load_dotenv(dotenv_path=find_dotenv())
    vk_token = environ["VK_TOKEN"]

    params_short_link = {
        "vk_token": vk_token,
        'url': input("Вставьте ссылку: ")
        }

    link = params_short_link["url"]

    params_stat_method = {
        "key": urlparse(link).path.strip('/'),
        "access_token": vk_token
        }
    if is_shorten_link(link):
        print("Ссылка короткая")
        try:
            clicks_count = count_clicks(token=params_stat_method)
        except HTTPError:
            raise KeyboardInterrupt
        if clicks_count is not None:
            print("Количетсво кликов: ", clicks_count)
    else:
        try:
            print("Ссылка длинная")
            short_link = shorten_link(token=params_short_link)
            print(short_link)
        except HTTPError:
            raise KeyboardInterrupt
