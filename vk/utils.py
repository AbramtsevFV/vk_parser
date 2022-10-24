import pickle

def parse_group(group: dict) -> dict:
    entry = {
        'group_id': group['id'],
        'name': group['name'],
        'screen_name': group['screen_name'],
        'is_closed': group['is_closed']
    }
    return entry


def parse_user(user: dict, group: dict) -> dict:
    city = user.get('city', {}).get('title', '')
    country = user.get('country', {}).get('title', '')
    career = user.get('career', '')
    if career:
        career = '\n'.join(
            [f'company: {i.get("company", "No company")}, position: {i.get("position", "No position")} ' for i in
             career])

    entry = {
        'user_id': user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'city': city,
        'country': country,
        'mobile_phone': user.get('mobile_phone', ''),
        'home_phone': user.get('home_phone', ''),
        'career': career,
        'university_name': user.get('university_name', ''),
        'group_id': group['group_id'],
        'group_name': group['group_name']
    }
    return entry


def save_data(path, data):
    with open(path, 'rb') as file:
        pickle.dump(data, file)

def load_data(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data
