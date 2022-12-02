import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from fake_useragent import UserAgent


class VK:
    def __init__(self, token, url):
        self.__token = token
        self.__base_url = url
        self.http = Session()
        self.http.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 429, 500, 502, 503, 504],
            backoff_factor=5
        )
        self.adapter = HTTPAdapter(max_retries=retry_strategy)

        self.http.mount("https://", self.adapter)

    def __get(self, method, **kwargs):
        qwery_params = "&".join((f'{k}={v}' for k, v in kwargs.items()))
        url = f'{self.__base_url}{method}?{qwery_params}&access_token={self.__token}&v=5.81'
        req = self.http.get(url=url, )
        if req.status_code == 200:
            return req.json()
        return None

    def get_group_list(self, **kwargs):
        """Получаем JSON с группами"""
        return self.__get(method='groups.search', **kwargs)

    def get_users(self, **kwargs):
        """Получаем id Пользователей"""
        return self.__get(method='groups.getMembers', **kwargs)

    def get_user_info(self, **kwargs):
        """Получаем данные пользователей за 1 раз не больше 1000 id"""
        return self.__get(method='users.get', **kwargs)

    def get_posts(self, **kwargs):
        """Получение всех постов с группы по id """
        return self.__get(method='wall.get', **kwargs)

    def get_comments(self, **kwargs):
        """Получение комментариев к посту"""
        return self.__get(method='wall.getComments', **kwargs)

    def get_group_id(self, **kwargs):
        """Возвращает id  группы по screen_name"""
        return self.__get(method='utils.resolveScreenName', **kwargs)

    def get_group_information(self, **kwargs):
        """Возвращает информацию о заданном сообществе по id или screen_name"""
        return self.__get(method='groups.getById', **kwargs)
