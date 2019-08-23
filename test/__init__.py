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
    s[0].auth_to_emby = MagicMock()
    s[0].auth_to_emby.return_value = True
    s[0].emby_croft.handle_intent.return_value = songs

    return SkillTest(skill, example, emitter).run(loader)
