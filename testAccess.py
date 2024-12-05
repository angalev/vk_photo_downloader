import requests
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config['Token']['access_token']
user_id = 826975570
api_version = config['API_version']['v']
secret_key = config['Secret_app_key']['secret_app_key']
app_id = config['App_ID']['app_id']
secret_code = config['Secret_code']['secret_code']

def generate_token_request(app_id, secret_code, secret_key):
    print(f'https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends, photos, wall&response_type=code&v={api_version}')
    print(f'https://oauth.vk.com/access_token?client_id={app_id}&client_secret={secret_key}&redirect_uri=https://oauth.vk.com/blank.html&code={secret_code}')

class VK:

    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


vk = VK(access_token, user_id)

print(vk.users_info())
generate_token_request(app_id, secret_code,secret_key)

