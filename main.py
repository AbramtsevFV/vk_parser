
from vk.vk import get_users_list, get_users, get_count_coments, merge_data, get_groups_list

search = 'работа в Оренбурге'

if __name__ == '__main__':
    groups_list = get_groups_list(search)
    lst = get_users_list(groups_list)
    users_list = get_users(lst)

    user_comments = get_count_coments(lst)

    users_list_df = merge_data(user_comments, users_list)
    users_list_df.to_csv('vk_result.csv')


