import requests as r
import configparser
import json
from tqdm import tqdm


# Get authentification info from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config['Token']['access_token']
api_version = config['API_version']['v']
ytoken = config['YToken']['ytoken']

# Input subject info
print('Введите ID пользователя в цифровом формате:')
user_id = int(input())
print('Введите максимальное количество скачиваемых фотографий профиля:')
number = int(input())

class VK_user:
    def __init__(self, access_token, api_version=5.199):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': access_token,
            'v': api_version
        }

    def get_profile_pics(self, user_id):
        params = self.params
        params.update({'user_id': user_id, 'album_id': 'profile',
                       'extended': 1, 'photo_sizes': 1, 'count': number})
        response = r.get(f'{self.base_url}photos.get', params=params)
        return response.json()

    def upload_photo(self, name, url, user_id):
        headers = {'Authorization': f'OAuth {ytoken}'}
        params = {'path': f'VK_downloads_{user_id}/{name}'}
        response = r.get(yadi_url+'/upload', headers=headers,
                         params=params).json()
        r.put(response['href'], files={'file': r.get(url).content})

    def highest_resolution(self, photo):
        size_priority = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        size_type = sorted([c['type'] for c in photo['sizes']],
                                key=lambda x: size_priority.index(x))
        return size_type[0]

    def download_photo(self, user_id):
        log_list = []
        response = self.get_profile_pics(user_id)
        try:
            with tqdm(total=len(response['response']['items'])) as pbar:
                for photo in response['response']['items']:
                    pbar.update(1)
                    size_type = self.highest_resolution(photo)
                    for elem in photo['sizes']:
                        if elem['type'] == size_type:
                            self.upload_photo(f"{photo['id']}.jpg", elem['url'], user_id)
                            log_list.append({"file_name": f"{photo['id']}.jpg",
                                     "size": elem['type']})
                with open('log.json', 'w+') as f:
                    f.write(json.dumps(log_list))
                    print(f'Загружено фотографий:{len(log_list)}')
        except:
            print('Программа завершена с ошибкой. Возможно отсутствует доступ к запрошенному профилю.')


if __name__ == '__main__':
    vk_account = VK_user(access_token)

    yadi_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Authorization': f'OAuth {ytoken}'}
    params = {'path': f'VK_downloads_{user_id}'}
    response = r.put(yadi_url, headers=headers, params=params)
    if response.status_code == 409:
        print('Папка для указанного ID уже существует, введите другой ID, или удалите папку.')
    if response.status_code != 201:
        print('Ошибка')
    else:
        vk_account.download_photo(user_id)

