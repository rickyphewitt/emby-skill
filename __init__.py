from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService

from .emby_croft import EmbyCroft


class Emby(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.audio_service = AudioService(self.bus)

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):
        HOST = "http://emby:8096"
        USERNAME = "Ricky"
        PASSWORD = ""

        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
        artists = emby_croft.search_artist(message)
        song = emby_croft.play(artists[0].id)
        self.audio_service.play(song)
        self.speak_dialog('emby')


def create_skill():
    return Emby()






