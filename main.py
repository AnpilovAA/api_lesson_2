from json import loads
from urllib.parse import urlparse
from os import environ


from dotenv import load_dotenv, find_dotenv
from requests import get
from requests.exceptions import HTTPError


def shorten_link(token: str, url: str) -> None:
    if is_shorten_link(token['url']):
        return token['url']
    else:
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


def count_clicks(token: str, url: str):
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
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": environ["TOKEN"],
        'url': input("Вставьте ссылку: "),
        'string': "key",
        "private": 0,
        "v": 5.199,
    }
    try:
        short_link = shorten_link(token=params, url=url)
        print(short_link)
    except HTTPError:
        raise KeyboardInterrupt

    url_stat_method = "https://api.vk.ru/method/utils.getLinkStats"
    params_stat_method = {
        "key": urlparse(short_link).path.strip('/'),
        "access_token": environ["TOKEN"],
        "v": 5.199,
    }
    try:
        clicks_count = count_clicks(
            token=params_stat_method,
            url=url_stat_method
        )
    except HTTPError:
        raise KeyboardInterrupt
    if clicks_count is not None:
        print(clicks_count)
    if is_shorten_link(params["url"]):
        print("Cсылка короткая")
    else:
        print("Cсылка длинная")
