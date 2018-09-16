import pytest
from emby_croft import EmbyCroft
from emby_client import MediaItemType, EmbyMediaItem

HOST = "http://emby:8096"
USERNAME = "Ricky"
PASSWORD = ""


def test_auth():
    EmbyCroft(HOST, USERNAME, PASSWORD)


def test_search_for_artist():
    artist = "Dance Gavin Dance"

    emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
    artists = emby_croft.search_artist(artist)
    assert len(artists) == 1
    assert artists[0].name == artist
    assert artists[0].id is not None
    assert artists[0].type == MediaItemType.ARTIST


@pytest.mark.blab
def test_play_artist():
    item_id = "7aa716c56d586c405cfdab383086e530"

    emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
    file = emby_croft.play(item_id)

    assert file is not None


def test_search_for_song():
    song = "And I Told Them I Invented Times New Roman"

    emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
    songs = emby_croft.search_song(song)
    assert len(songs) == 3
    for song_item in songs:
        assert song in song_item.name
        assert song_item.id is not None
        assert song_item.type == MediaItemType.SONG
