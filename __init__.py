import hashlib
from mycroft import intent_file_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.skills.audioservice import AudioService
from mycroft.api import DeviceApi

from .emby_croft import EmbyCroft


class Emby(CommonPlaySkill):

    def __init__(self):
        super().__init__()
        self._setup = False
        self.audio_service = None
        self.emby_croft = None
        self.device_id = hashlib.md5(
            ('Emby'+DeviceApi().identity.uuid).encode())\
            .hexdigest()

    def initialize(self):
        pass

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):

        self.log.log(20, message.data)

        # first thing is connect to emby or bail
        if not self.auth_to_emby():
            self.speak_dialog('configuration_fail')
            return

        # determine intent
        intent, intent_type = EmbyCroft.determine_intent(message.data)

        songs = []
        try:
            songs = self.emby_croft.handle_intent(intent, intent_type)
        except Exception as e:
            self.log.log(20, e)
            self.speak_dialog('play_fail', {"media": intent})

        if not songs or len(songs) < 1:
            self.log.log(20, 'No songs Returned')
            self.speak_dialog('play_fail', {"media": intent})
        else:
            # setup audio service and play
            self.audio_service = AudioService(self.bus)
            self.speak_playing(intent)
            self.audio_service.play(songs, message.data['utterance'])

    def speak_playing(self, media):
        data = dict()
        data['media'] = media
        self.speak_dialog('emby', data)

    def stop(self):
        pass

    def CPS_start(self, phrase, data):
        """ Starts playback.

            Called by the playback control skill to start playback if the
            skill is selected (has the best match level)
        """
        # setup audio service
        self.audio_service = AudioService(self.bus)
        self.audio_service.play(data[phrase])

    def CPS_match_query_phrase(self, phrase):
        """ This method responds whether the skill can play the input phrase.

            The method is invoked by the PlayBackControlSkill.

            Returns: tuple (matched phrase(str),
                            match level(CPSMatchLevel),
                            optional data(dict))
                     or None if no match was found.
        """
        # first thing is connect to emby or bail
        if not self.auth_to_emby():
            return None

        self.log.log(20, phrase)
        match_type, songs = self.emby_croft.parse_common_phrase(phrase)

        if match_type and songs:
            match_level = None
            if match_type is not None:
                self.log.log(20, 'Found match of type: ' + match_type)

                if match_type == 'song' or match_type == 'album':
                    match_level = CPSMatchLevel.TITLE
                elif match_type == 'artist':
                    match_level = CPSMatchLevel.ARTIST

                self.log.log(20, 'match level' + str(match_level))

            song_data = dict()
            song_data[phrase] = songs

            self.log.log(20, "First 3 item urls returned")
            max_songs_to_log = 3
            songs_logged = 0
            for song in songs:
                self.log.log(20, song)
                songs_logged = songs_logged + 1
                if songs_logged >= max_songs_to_log:
                    break

            return phrase, match_level, song_data
        else:
            return None

    def auth_to_emby(self):
        """
        Attempts to auth to the server based on the config
        returns true/false on success/failure respectively

        :return:
        """
        auth_success = False
        try:
            self.emby_croft = EmbyCroft(
                self.settings["hostname"] + ":" + str(self.settings["port"]),
                self.settings["username"], self.settings["password"],
                self.device_id)
            auth_success = True
        except Exception as e:
            self.log.log(20, "failed to connect to emby, error: {0}".format(str(e)))

        return auth_success


def create_skill():
    return Emby()
