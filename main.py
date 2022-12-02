from vk.vk import get_users_list, get_users, get_count_coments, merge_data, get_groups_list, get_group_name, logger

"""Пример входящих данных"""
search = 'работа в Оренбурге'
url = 'https://vk.com/channel_no_brake'


def main(search_query=None, url=None):
    groups = None
    if search_query:
        groups = get_groups_list(search)
    if url:
        groups = get_group_name(url)
    return groups


if __name__ == '__main__':
    groups_list = main(url=url)
    if groups_list:
        lst = get_users_list(groups_list)
        users_list = get_users(lst)
        if users_list:
            user_comments = get_count_coments(lst)
            users_list_df = merge_data(user_comments, users_list)
            users_list_df.to_csv('vk_result.csv')
    else:
        logger.warning('Неверное имя группы')
