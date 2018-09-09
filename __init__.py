from mycroft import MycroftSkill, intent_file_handler


class Emby(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('emby.intent')
    def handle_emby(self, message):
        self.speak_dialog('emby')


def create_skill():
    return Emby()

