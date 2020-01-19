from unittest.mock import MagicMock
try:
    # this import is not available when unit testing skill, but is required for mycroft-skills ci
    from test.integrationtests.skills.skill_tester import SkillTest
except ImportError:
    pass


def test_runner(skill, example, emitter, loader):

    # Get the skill object from the skill path
    s = [s for s in loader.skills if s and s.root_dir == skill]

    # mock data
    songs = ['song0', 'song1']

    # setup mocks
    s[0].emby_croft = MagicMock()
    s[0].connect_to_emby = MagicMock()
    s[0].connect_to_emby.return_value = True
    s[0].emby_croft.handle_intent.return_value = songs
    server_info = {'ServerName': 'myServer', 'LocalAddress': '127.0.0.1', 'Version': '99'}

    # mocks for diagnostic testing
    s[0].emby_croft.diag_public_server_info.return_value = True, server_info

    return SkillTest(skill, example, emitter).run(loader)
