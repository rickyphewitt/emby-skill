from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService

from .emby_croft import EmbyCroft


class Emby(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self._setup = False
        self.audio_service = None
        self.emby_croft = None

    def initialize(self):
        pass

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):

        self.log.log(20, message.data)

        # first thing is connect to emby or bail
        if not self.auth_to_emby():
            self.speak_dialog('configuration_fail')
            return

        media = message.data['media']

        # setup audio service
        self.audio_service = AudioService(self.bus)

        songs = []
        try:
            songs = self.emby_croft.find_songs(media)
        except Exception as e:
            self.log.log(20, e)
            self.speak_dialog('play_fail', {"media": media})

        if len(songs) < 1:
            self.speak_dialog('play_fail', {"media": media})
        else:
            self.speak_playing(media)
            self.audio_service.play(songs)

    def speak_playing(self, media):
        data = dict()
        data['media'] = media
        self.speak_dialog('emby', data)

    def stop(self):
        pass

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
                self.settings["username"], self.settings["password"])
            auth_success = True
        except Exception as e:
            self.log.log(20, "failed to connect to emby, error: {0}".format(str(e)))

        return auth_success


def create_skill():
    return Emby()
