import pytest

from emby_client import EmbyClient, MediaItemType, EmbyMediaItem
from emby_croft import EmbyCroft

HOST = "http://emby:8096"
USERNAME = "ricky"
PASSWORD = ""


class TestEmbyClient(object):

    @pytest.mark.client
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
