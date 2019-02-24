import logging
from enum import Enum
from random import shuffle

try:
    # this import works when installing/running the skill
    # note the relative '.'
    from .emby_client import EmbyClient, MediaItemType, EmbyMediaItem
except (ImportError, SystemError):
    # when running unit tests the '.' from above fails so we exclude it
    from emby_client import EmbyClient, MediaItemType, EmbyMediaItem

class IntentType(Enum):
    MEDIA = "media"
    ARTIST = "artist"
    ALBUM = "album"
    SONG = "song"

    @staticmethod
    def from_string(enum_string):
        assert enum_string is not None
        for item_type in IntentType:
            if item_type.value == enum_string.lower():
                return item_type



class EmbyCroft(object):

    def __init__(self, host, username, password):
        self.log = logging.getLogger(__name__)
        self.client = EmbyClient(host, username, password)

    @staticmethod
    def determine_intent(intent: dict):
        """
        Determine the intent!

        :param self:
        :param intent:
        :return:
        """
        if 'media' in intent:
            return intent['media'], IntentType.from_string('media')
        elif 'artist' in intent:
            return intent['artist'], IntentType.from_string('artist')
        else:
            return None

    def handle_intent(self, intent: str, intent_type: IntentType):
        """
        Returns songs for given intent if songs are found; none if not
        :param intent:
        :return:
        """

        songs = []
        if intent_type == IntentType.MEDIA:
            # default to instant mix
            songs = self.find_songs(intent)
        elif intent_type == IntentType.ARTIST:
            # return songs by artist
            artist_items = self.search_artist(intent)
            if len(artist_items) > 0:
                songs = self.get_songs_by_artist(artist_items[0].id)
                # shuffle by default for songs by artist
                shuffle(songs)

        return songs

    def find_songs(self, media_name, media_type=None)->[]:
        """
        This is the expected entry point for determining what songs to play

        :param media_name:
        :param media_type:
        :return:
        """

        songs = []
        songs = self.instant_mix_for_media(media_name)
        return songs

    def search_artist(self, artist):
        """
        Helper method to just search Emby for an artist
        :param artist:
        :return:
        """
        return self.search(artist, [MediaItemType.ARTIST.value])

    def search_song(self, song):
        """
        Helper method to just search Emby for songs
        :param song:
        :return:
        """
        return self.search(song, [MediaItemType.SONG.value])

    def search(self, query, include_media_types=[]):
        """
        Searches Emby from a given query
        :param query:
        :param include_media_types:
        :return:
        """
        response = self.client.search(query, include_media_types)
        search_items = EmbyCroft.parse_search_hints_from_response(response)
        return EmbyMediaItem.from_list(search_items)

    def get_instant_mix_songs(self, item_id):
        """
        Requests an instant mix from an Emby item id
        and returns song uris to be played by the Audio Service
        :param item_id:
        :return:
        """
        response = self.client.instant_mix(item_id)
        queue_items = EmbyMediaItem.from_list(
            EmbyCroft.parse_response(response))

        song_uris = []
        for item in queue_items:
            song_uris.append(self.client.get_song_file(item.id))
        return song_uris

    def instant_mix_for_media(self, media_name):
        """
        Method that takes in a media name (artist/song/album) and
        returns an instant mix of song uris to be played

        :param media_name:
        :return:
        """

        items = self.search(media_name)
        self.log.log(20, items)
        if items is None:
            items = []

        item_count = len(items)

        self.log.log(20, 'Found {0} item(s) when searching for {1}'
                     .format(item_count, media_name))

        songs = []
        if item_count > 0:
            songs = self.get_instant_mix_songs(items[0].id)

        return songs

    def get_albums_by_artist(self, artist_id):
        return self.client.get_albums_by_artist(artist_id)

    def get_songs_by_album(self, album_id):
        response = self.client.get_songs_by_album(album_id)
        return self.convert_response_to_playable_songs(response)

    def get_songs_by_artist(self, artist_id):
        response = self.client.get_songs_by_artist(artist_id)
        return self.convert_response_to_playable_songs(response)

    def convert_response_to_playable_songs(self, item_query_response):
        queue_items = EmbyMediaItem.from_list(
            EmbyCroft.parse_response(item_query_response))
        return self.convert_to_playable_songs(queue_items)

    def convert_to_playable_songs(self, songs):
        song_uris = []
        for item in songs:
            song_uris.append(self.client.get_song_file(item.id))
        return song_uris


    @staticmethod
    def parse_search_hints_from_response(response):
        if response.text:
            response_json = response.json()
            return response_json["SearchHints"]

    @staticmethod
    def parse_response(response):
        if response.text:
            response_json = response.json()
            return response_json["Items"]

    def parse_common_phrase(self, phrase: str):
        """
        Attempts to match emby items with phrase
        :param phrase:
        :return:
        """

        logging.log(20, "phrase: " + phrase)
        phrase = phrase.lower()
        # see if phrase contains mb or emby
        if 'mb' in phrase or 'emby' in phrase:
            # remove from phrase
            phrase.replace("mb", "")
            phrase.replace("emby", "")

        results = self.search(phrase)

        if results is None or len(results) is 0:
            return None, None
        else:
            logging.log(20, "Found: " + str(len(results)) + " to parse")
            # the idea here is
            # if an artist is found, return songs from this artist
            # elif an album is found, return songs from this album
            # elif a song is found, return song
            artists = []
            albums = []
            songs = []
            for result in results:
                if result.type == MediaItemType.ARTIST:
                    artists.append(result)
                elif result.type == MediaItemType.ALBUM:
                    albums.append(result)
                elif result.type == MediaItemType.SONG:
                    songs.append(result)
                else:
                    logging.log(20, "Item is not an Artist/Album/Song: " + result.type)

            if artists:
                artist_songs = self.get_songs_by_artist(artists[0].id)
                return 'artist', artist_songs
            elif albums:
                album_songs = self.get_songs_by_album(albums[0].id)
                return 'album', album_songs
            elif songs:
                # if a song(s) matches pick the 1st
                song_songs = self.convert_to_playable_songs(songs)
                return 'song', song_songs
            else:
                return None, None
