import pytest


class TestApi:

    @pytest.mark.API
    def test_create_segment(self, api_client):

        # log in
        api_client.post_login()
        # creating segment
        resp = api_client.post_create_segment()
        assert resp.status_code == 200, 'Bad autentification'
        # deleting segment
        api_client.post_delete_segment(id_segment=resp.json()['id'])

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        # log in
        api_client.post_login()
        # deleting segment
        api_client.post_delete_segment()
