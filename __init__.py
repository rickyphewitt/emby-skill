from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService

from .emby_croft import EmbyCroft


class Emby(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

        HOST = "http://emby:8096"
        USERNAME = "Ricky"
        PASSWORD = ""

        self.audio_service = None
        self.emby_croft = EmbyCroft(
            self.settings["hostname"] + ":" + self.settings["port"],
            self.settings["username"], self.settings["password"])

# {'artist': 'dance gavin dance', 'utterance': 'play artist dance gavin dance from emby'}
    @intent_file_handler('emby.intent')
    def handle_emby(self, message):
        self.log.log(20, message.data)
        artist = message.data['artist']

        if 'instant mix' in message.data["utterance"]:
            self.log.log(20, "instant Mix!")

        # setup audio service
        self.audio_service = AudioService(self.bus)

        # auth to emby.. should be in the init method.. but need creds from mycrof.ai
        songs = self.emby_croft.instant_mix_for_media(artist)
        self.audio_service.play(songs)
        self.speak_dialog('emby')


def create_skill():
    return Emby()






