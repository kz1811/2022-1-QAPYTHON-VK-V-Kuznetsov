import logging
import requests
import random
import string
from urllib.parse import urljoin
from requests.cookies import cookiejar_from_dict

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 300


class InvalidLoginException(Exception):
    pass


class RespondErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def rand_gen(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(random.randrange(30)))

    def __init__(self, base_url, user, password, ):
        self.base_url = base_url
        self.user = user
        self.password = password

        self.session = requests.Session()

        self.csrf_token = None

    def get_token(self):
        res = requests.get('https://account.my.com/login')

        self.csrf_token = [c for c in res.headers['Set-cookie'].split(';') if 'csrf' in c][0].split('=')[-1]

    def post_login(self, set_session=True):

        self.get_token()

        headers = {
            'Cookie': f'csrf_token={self.csrf_token}',
            'Referer': 'https://account.my.com/',
        }
        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://account.my.com/profile/userinfo',
            'failure': 'https://account.my.com/login/',
            'nosavelogin': '0',
        }

        res = requests.post('https://auth-ac.my.com/auth', data=data, headers=headers)

        cookies_string = ''
        for i in range(res.history.__len__()):
            if 'set-cookie' in res.history[i].headers.keys():
                cookies_string = cookies_string + res.history[i].headers['set-cookie']

        cookies_string = cookies_string.split(';')

        print(cookies_string)
        cookies_dict = {
            'mc': [c for c in cookies_string if 'mc=' in c][0].split('=')[-1],
            'mrcu': [c for c in cookies_string if 'mrcu=' in c][0].split('=')[-1],
            'ssdc': [c for c in cookies_string if 'ssdc=' in c][0].split('=')[-1],
            'sdcs': [c for c in cookies_string if 'sdcs=' in c][0].split('=')[-1],
            'csrf_token': [c for c in cookies_string if 'csrf_token=' in c][0].split('=')[-1],
        }

        self.session.cookies = cookiejar_from_dict(cookies_dict)

        url = urljoin(self.base_url, 'csrf/')
        res = self.session.get(url)

        cookies_dict['csrftoken'] = [c for c in res.headers['Set-Cookie'].split(';') if 'csrftoken' in c][0].split('=')[-1]
        self.csrf_token = cookies_dict['csrftoken']
        cookies_dict['z'] = [c for c in res.headers['Set-Cookie'].split(';') if 'z=' in c][0].split('=')[-1]
        cookies_dict['sdc'] = [c for c in res.history[3].headers['Set-cookie'].split(';') if 'sdc=' in c][0].split('=')[-1]
        print(cookies_dict)

        self.session.cookies = cookiejar_from_dict(cookies_dict)

        # return

    def post_create_segment(self, name=None):

        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')

        if name is None:
            name = self.rand_gen()

        data = {
            "name": f"{name}",
            "pass_condition": 1,
            "relations": [
            {
                "params": {
                    "type": "positive",
                    "left": 365,
                    "right": 0
                },
                "object_id": 73656,
                "object_type": "remarketing_player"
            }]}

        headers = {
            'X-CSRFToken': f'{self.csrf_token}',
        }

        return self.session.post(url, json=data, headers=headers)

    def post_delete_segment(self, id_segment=None, name=None):

        url = urljoin(self.base_url, f'api/v2/remarketing/segments.json')

        if id_segment is None and name is None:
            res = self.session.get(url)
            number = random.randint(0, len(res.json()['items']))
            id_segment = res.json()['items'][number]['id']

        elif id_segment is None:
            id_segment = self.get_id_by_name(name)

        headers = {
            'X-CSRFToken': f'{self.csrf_token}',
        }

        url = urljoin(self.base_url, f'api/v2/remarketing/segments/{id_segment}.json')
        res = self.session.delete(url, headers=headers)
        assert res.status_code == 204, 'Deletion not completed'
        return res

    def get_id_by_name(self, name):

        url = urljoin(self.base_url, "api/v2/remarketing/segments.json")

        params = {
            '_name': name,
        }
        res = self.session.get(url, params=params)
        id_segment = res.json()['items'][0]['id']
        return id_segment