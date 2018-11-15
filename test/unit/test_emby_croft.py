import pytest, json
from unittest import TestCase, mock
from emby_croft import EmbyCroft
from emby_client import MediaItemType, EmbyMediaItem

HOST = "http://emby:8096"
USERNAME = "ricky"
PASSWORD = ""

"""
This test file is expected to have tests using mock's and using a real emby server
The expectation is that there will be 2 tests 1 that are exactly the same
1 that will utilize mocks for the calls to the emby server and another that
will actually call the Emby server and handle real responses. There is probably
a better way to do this but I'm lazy :)

"""


class TestEmbyCroft(object):

    # load mocked responses
    mocked_responses = None
    with open("test/unit/test_responses.json") as f:
        mocked_responses = json.load(f)

    @pytest.mark.mocked
    def test_auth_mock(self):
        with mock.patch('requests.post') as MockRequestsPost:
            auth_server_response = TestEmbyCroft.mocked_responses["emby"]["3.5.2.0"]["auth_server_response"]
            response = MockResponse(200, auth_server_response)
            MockRequestsPost.return_value = response
            emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

            assert emby_croft.client.auth.token is auth_server_response["AccessToken"]
            assert emby_croft.client.auth.user_id is auth_server_response["User"]["Id"]

    @pytest.mark.mocked
    def test_instant_mix_mock(self):
        with mock.patch('requests.post') as MockRequestsPost:
            auth_server_response = TestEmbyCroft.mocked_responses["emby"]["3.5.2.0"]["auth_server_response"]
            search_response = TestEmbyCroft.mocked_responses["emby"]["3.5.2.0"]["search_response"]
            get_songs_response = TestEmbyCroft.mocked_responses["emby"]["3.5.2.0"]["get_songs_response"]

            album = "This is how the wind shifts"
            response = MockResponse(200, auth_server_response)
            MockRequestsPost.return_value = response
            emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

            with mock.patch('requests.get') as MockRequestsGet:
                responses = [MockResponse(200, search_response), MockResponse(200, get_songs_response)]
                MockRequestsGet.side_effect = responses

                songs = emby_croft.instant_mix_for_media(album)
                assert songs is not None
                assert len(songs) is 1

    @pytest.mark.live
    def test_auth(self):
        emby_client = EmbyCroft(HOST, USERNAME, PASSWORD)
        assert emby_client.client.auth is not None

    @pytest.mark.live
    @pytest.mark.ricky
    def test_instant_mix_live(self):
        album = "This is how the wind shifts"
        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

        songs = emby_croft.instant_mix_for_media(album)
        assert songs is not None

    @pytest.mark.live
    def test_search_for_song(self):
        song = "And I Told Them I Invented Times New Roman"

        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
        songs = emby_croft.search_song(song)
        assert len(songs) == 3
        for song_item in songs:
            assert song in song_item.name
            assert song_item.id is not None
            assert song_item.type == MediaItemType.SONG


class MockResponse:
    def __init__(self, status_code, json_data):
        self.json_data = json_data
        self.text = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data