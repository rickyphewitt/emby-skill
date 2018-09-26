from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService

from .emby_croft import EmbyCroft


class Emby(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self.audio_service = None

        try:
            self.emby_croft = EmbyCroft(
                self.settings["hostname"] + ":" + str(self.settings["port"]),
                self.settings["username"], self.settings["password"])
        except Exception as e:
            self.log.log(20, e)
            self.speak('Failed to connect to Emby. Please check your'
                       ' configuration at Mycroft.ai')

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):
        self.log.log(20, message.data)
        media = message.data['media']

        # setup audio service
        self.audio_service = AudioService(self.bus)

        songs = []
        try:
            songs = self.emby_croft.instant_mix_for_media(media)
            self.audio_service.play(songs)
            self.speak_playing(media)
        except Exception as e:
            self.log.log(20, e)
            self.speak("Unable to find or play " + media +
                       ". Please try again")

    def speak_playing(self, media):
        data = dict()
        data['media'] = media
        self.speak_dialog('emby', data)

    def stop(self):
        pass


def create_skill():
    return Emby()
