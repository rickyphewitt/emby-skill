from .emby_client import EmbyClient, MediaItemType, EmbyMediaItem
import json

class EmbyCroft(object):

    def __init__(self, host, username, password):
        self.client = EmbyClient(host, username, password)
        self.now_playing_queue = []
        self.now_playing_queue_track = 0

    def search_artist(self, artist):
        return self.search(artist, [MediaItemType.ARTIST.value])

    def search_song(self, song):
        return self.search(song, [MediaItemType.SONG.value])

    def search(self, query, include_media_types):
        response = self.client.search(query, include_media_types)
        search_items = EmbyCroft.parse_search_hints_from_response(response)
        return EmbyMediaItem.from_list(search_items)

    def play(self, item_id):
        response = self.client.instant_mix(item_id)
        queue_items = EmbyCroft.parse_instant_mix_from_response(response)
        self.now_playing_queue = EmbyMediaItem.from_list(queue_items)

        # play 1st song
        return self.client.get_song_file(self.now_playing_queue[self.now_playing_queue_track].id)

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