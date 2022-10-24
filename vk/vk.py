import time
from tqdm import tqdm
import logging

import pickle

import pandas as pd

from creds.tokens import vk_token
from libraries import vk, VK
import logging

from vk.utils import parse_group, parse_user

logger = logging.getLogger('logger')





def get_groups_list(search) -> list:
    """Получаем список групп, отвечающих поиску"""

    groups = vk.get_group_list(q=search, count=1000, offset=0)
    if groups:
        groups_list = groups.get('response', {}).get('items', None)
        print(f'{"*" * 5} Получение групп {"*" * 5}')
        return [parse_group(group) for group in groups_list]


def get_users_list(groups_list):
    """Получаем список пользователей из каждой найденной группы"""

    res = []
    print(f'{"*" * 5} Получение id пользователей {"*" * 5}')
    for group in tqdm(groups_list):
        offset = 0
        group_dict = {'group_name': group['name'],
                      'group_id': group['group_id'],
                      'user_list': []
                      }
        while True:
            req = vk.get_users(group_id=group['group_id'], count=1000, offset=offset)

            if req is None or req.get('error', {}).get('error_code', None) in [15, 203]:
                logger.warning(req)
                break
            if req:
                count = req['response']['count']
                group_dict['user_list'].extend(req['response']['items'])
                if count - offset < 1000:
                    res.append(group_dict)
                    break

            offset += 1000
            time.sleep(0.5)

    return res


def get_users(lst_gr: list):
    """Получаем и сохраняем пользователей с интересующими нас полями"""

    result_list = []
    start = 0
    print(f'{"*" * 5} Парсинг пользователей {"*" * 5}')
    for group in tqdm(lst_gr):
        lst_us = group['user_list']
        for step in tqdm(range(1000, len(lst_us), 1000)):

            st = ','.join(map(str, lst_us[start:step]))
            start = step
            users_list = vk.get_user_info(user_ids={st}, fields='country,city,education,career,contacts')

            if users_list:
                result_list.extend([parse_user(user, group) for user in users_list['response']])

            time.sleep(0.5)

    return result_list


def get_count_coments(lst_gr):
    """Получение коментариев к постам"""
    print(f'{"*" * 5} Загрузка постов {"*" * 5}')
    res = []

    for group in tqdm(lst_gr):
        owner_id = f"-{group['group_id']}"

        posts = vk.get_posts(owner_id=owner_id, count=100)
        if posts:
            if posts.get('response', {}).get('items', None):
                for post in posts['response']['items']:
                    if post["comments"]["count"] > 0:
                        comments = vk.get_comments(owner_id=owner_id, count=100, post_id=post['id'])
                        if comments is None or comments.get('error', None) is None:
                            for comment in comments['response']['items']:
                                res.append({'group_id': group['group_id'], 'user_id': comment['from_id']})
                    time.sleep(0.5)
            else:
                logger.warning(posts)
    return res


def merge_data(user_comments, users_list):
    """Функция собирает данные во едино"""

    # подготовка данных по комментариям в группе
    user_comments_df = pd.DataFrame(user_comments)
    user_comments_df = user_comments_df.groupby(['group_id', 'user_id'])[['user_id']].count().reset_index(level=0)
    user_comments_df.rename(columns={'user_id': 'count_coments'}, level=0, inplace=True)

    users_list_df = pd.DataFrame(users_list)
    users_list_df = users_list_df.merge(user_comments_df, right_on=['user_id', 'group_id'],
                                        left_on=['user_id', 'group_id'], how='left')
    # Добавляем ссылку
    users_list_df['profile_url'] = users_list_df['user_id'].apply(lambda x: f'https://vk.com/id{x}')

    return users_list_df
