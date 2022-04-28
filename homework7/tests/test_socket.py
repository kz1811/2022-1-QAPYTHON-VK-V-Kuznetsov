import pytest
import settings
from http_client_socket.http_socket import Socket
from utils.value_gen import Generator


class TestSocket:
    client = Socket(settings.APP_HOST, int(settings.APP_PORT))


@pytest.mark.socket
class TestSocketPostRequests(TestSocket):

    def test_post_request(self, clear_data):
        name = Generator().name()
        answer_post = self.client.send_post_request(name)
        assert answer_post['status_code'] == 201 and answer_post['data']['user_id'] > 0


@pytest.mark.socket
class TestSocketGetRequests(TestSocket):

    def test_get_request_negative(self, clear_data):
        name = Generator().name()
        answer_get = self.client.send_get_request(name)
        assert answer_get['status_code'] == 404

    def test_get_request_positive(self, clear_data):
        name = Generator().name()

        answer_post = self.client.send_post_request(name)
        assert answer_post['status_code'] == 201 and answer_post['data']['user_id'] > 0
        answer_get = self.client.send_get_request(name)
        assert answer_get['status_code'] == 200 and answer_post['data']['user_id'] == answer_get['data']['user_id']


@pytest.mark.socket
class TestSocketPutRequests(TestSocket):

    def test_put_request_positive(self, clear_data):
        name = Generator().name()
        surname = Generator().surname()

        answer_post = self.client.send_post_request(name)
        assert answer_post['status_code'] == 201 and answer_post['data']['user_id'] > 0

        answer_put = self.client.send_put_request(name, surname)
        assert answer_put['status_code'] == 200

        answer_get = self.client.send_get_request(name)
        assert answer_get['status_code'] == 200 and \
               answer_get['data']['surname'] == surname and \
               answer_post['data']['user_id'] == answer_get['data']['user_id']

    def test_put_request_negative(self, clear_data):
        name = Generator().name()
        surname = Generator().surname()

        answer_put = self.client.send_put_request(name, surname)
        assert answer_put['status_code'] == 404


@pytest.mark.socket
class TestSocketDeleteRequests(TestSocket):

    def test_delete_request_positive(self, clear_data):
        name = Generator().name()

        answer_post = self.client.send_post_request(name)
        assert answer_post['status_code'] == 201 and answer_post['data']['user_id'] > 0

        answer_delete = self.client.send_delete_request(name)
        assert answer_delete['status_code'] == 200

        answer_get = self.client.send_get_request(name)
        assert answer_get['status_code'] == 404

    def test_delete_request_negative(self, clear_data):
        name = Generator().name()

        answer_delete = self.client.send_delete_request(name)
        assert answer_delete['status_code'] == 404
