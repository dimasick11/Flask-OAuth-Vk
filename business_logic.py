import requests


def get_concate_username(token, user_id):
    data = {'user_id': user_id,
            'v': '5.92', 
            'access_token': token,
           }
    
    user_info = requests.post('https://api.vk.com/method/users.get', data = data)
    
    if 'response' in user_info.json():
        user_info = user_info.json().get('response')[0]
        first_name, last_name = user_info['first_name'], user_info['last_name']
        return first_name + ' ' + last_name
    return None

def get_friends_curr_user(token, user_id):
    tmp = {}
    data = {'user_id': user_id,
            'v': '5.92', 
            'access_token': token,
            'count': 5
           }
    
    user_list = requests.post('https://api.vk.com/method/friends.get', data = data)
    if 'response' in user_list.json():
        user_list = user_list.json().get('response').get('items')
        for user_id in user_list:
            tmp[user_id] = {
                'user_url': f'https://vk.com/id{user_id}',
                'user_name': get_concate_username(token, user_id)
            }
    return tmp
