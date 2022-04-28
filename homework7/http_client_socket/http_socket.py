import socket
import json
import settings
from _socket import timeout


class Socket:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_get_request(self, user_name):
        data = self.request_('GET', f'/get_user/{user_name}')
        return data

    def send_post_request(self, name):
        json_data = json.dumps({'name': name})
        data = self.request_('POST', '/add_user', json_data)
        return data

    def send_delete_request(self, name):
        json_data = json.dumps({'name': name})
        data = self.request_('DELETE', '/delete_user', json_data)
        return data

    def send_put_request(self, name, surname):
        json_data = json.dumps({'name': name, 'surname': surname})
        data = self.request_('PUT', '/change_user', json_data)
        return data

    def request_(self, type_req, params, data=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.5)
        self.client.connect((self.host, self.port))

        request = f'{type_req} {params} HTTP/1.1\r\nHost:{self.host}:{self.port}\r\n'

        if data is not None:
            length_data = str(len(data))
            request += f'Content-Type: application/json\r\nContent-Length: {length_data}\r\n\r\n{data}'
        else:
            request += '\r\n'

        self.client.send(request.encode())

        data = self.get_data_from_socket()
        self.client.close()

        return data

    def get_data_from_socket(self):
        total_data = []
        # try:
        while True:
            # читаем данные из сокета до тех пор пока они там есть
            data = self.client.recv(4096)
            if data:
                print(f'received data: {data}')
                total_data.append(data.decode())
            else:
                break
        # except timeout:
        #     pass

        total_data = ''.join(total_data).splitlines()
        status_code = int(total_data[0].split(' ')[1])
        body = json.loads(total_data[-1])
        return {'status_code': status_code, 'data': body}
