import pytest


class TestApi:

    @pytest.mark.API
    def test_create_segment(self, api_client):

        # log in
        status_code = api_client.post_login()
        # creating segment
        resp, name = api_client.post_create_segment()
        assert resp.status_code == 200 and api_client.is_segment_exist(name=name), 'Failed creating segment'
        # deleting segment after adding
        status_code, is_deleted = api_client.post_delete_segment(id_segment=resp.json()['id'])
        assert status_code == 204 and is_deleted, 'Failed deleting segment'

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        # log in
        status_code = api_client.post_login()
        # creating segment to exclude problems with empty list of segments
        resp, name = api_client.post_create_segment()
        assert resp.status_code == 200 and api_client.is_segment_exist(name=name), 'Failed creating segment'
        # deleting segment
        status_code, is_deleted = api_client.post_delete_segment(id_segment=resp.json()['id'])
        assert status_code == 204 and is_deleted, 'Failed deleting segment'
