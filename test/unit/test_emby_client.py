import pytest

from emby_client import EmbyClient, PublicEmbyClient, MediaItemType, EmbyMediaItem
from emby_croft import EmbyCroft

HOST = "http://emby:8096"
USERNAME = "ricky"
PASSWORD = ""


class TestEmbyClient(object):

    @pytest.mark.client
    @pytest.mark.live
    def test_songs_by_artist(self):
        artist = 'slaves'
        client = EmbyClient(HOST, USERNAME, PASSWORD)
        response = client.search(artist, [MediaItemType.ARTIST.value])
        search_items = EmbyCroft.parse_search_hints_from_response(response)
        artists = EmbyMediaItem.from_list(search_items)
        assert len(artists) == 1
        artist_id = artists[0].id
        songs = client.get_songs_by_artist(artist_id)
        assert songs is not None
        for song in songs.json()['Items']:
            assert artist in [a.lower() for a in song['Artists']]

    @pytest.mark.client
    @pytest.mark.live
    def test_songs_by_album(self):
        album = 'deadweight'
        client = EmbyClient(HOST, USERNAME, PASSWORD)
        response = client.search(album, [MediaItemType.ALBUM.value])
        search_items = EmbyCroft.parse_search_hints_from_response(response)
        albums = EmbyMediaItem.from_list(search_items)
        assert len(albums) == 1
        album_id = albums[0].id
        songs = client.get_songs_by_album(album_id)
        assert songs is not None
        for song in songs.json()['Items']:
            assert album == song['Album'].lower()

    @pytest.mark.client
    @pytest.mark.live
    def test_server_info_public(self):
        client = PublicEmbyClient(HOST)
        response = client.get_server_info_public()
        assert response.status_code == 200
        server_info = response.json()
        TestEmbyClient._assert_server_info(server_info)

    @pytest.mark.client
    @pytest.mark.live
    def test_server_info(self):
        client = EmbyClient(HOST, USERNAME, PASSWORD)
        response = client.get_server_info()
        assert response.status_code == 200
        server_info = response.json()
        TestEmbyClient._assert_server_info(server_info)

    def _assert_server_info(server_info):
        assert server_info['LocalAddress'] is not None
        assert server_info['WanAddress'] is not None
        assert server_info['ServerName'] is not None
        assert server_info['Version'] is not None
        assert server_info['Id'] is not None