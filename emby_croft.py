import logging
import json
try:
    # this import works when installing/running the skill
    # note the relative '.'
    from .emby_client import EmbyClient, MediaItemType, EmbyMediaItem
except (ImportError, SystemError):
    # when running unit tests the '.' from above fails so we exclude it
    from emby_client import EmbyClient, MediaItemType, EmbyMediaItem


class EmbyCroft(object):

    def __init__(self, host, username, password):
        self.log = logging.getLogger(__name__)
        self.client = EmbyClient(host, username, password)

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
            EmbyCroft.parse_instant_mix_from_response(response))

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

    @staticmethod
    def parse_search_hints_from_response(response):
        if response.text:
            response_json = json.loads(response.text)
            return response_json["SearchHints"]

    @staticmethod
    def parse_instant_mix_from_response(response):
        if response.text:
            response_json = json.loads(response.text)
            return response_json["Items"]
