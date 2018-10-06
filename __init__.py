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

        # register web settings changes
        self.settings.set_changed_callback(self.config_changed_callback)
        self.config_changed_callback()

    def config_changed_callback(self):
        """
        Attempt to connect to the local Emby server

        :return:
        """
        try:
            self.emby_croft = EmbyCroft(
                self.settings["hostname"] + ":" + str(self.settings["port"]),
                self.settings["username"], self.settings["password"])
            self.speak_dialog('configuration_success', self.settings)
        except Exception as e:
            self.speak_dialog('configuration_fail')

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):
        self.log.log(20, message.data)
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


def create_skill():
    return Emby()
