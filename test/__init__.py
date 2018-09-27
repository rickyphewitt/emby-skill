from unittest.mock import MagicMock
from test.integrationtests.skills.skill_tester import SkillTest


def test_runner(skill, example, emitter, loader):

    # Get the skill object from the skill path
    s = [s for s in loader.skills if s and s.root_dir == skill]

    # replace emby_croft with a mock
    s[0].emby_croft = MagicMock()
    # Set return value of instant mix for media
    s[0].emby_croft.instant_mix_for_media.return_value = ['http://song.url.awesome']

    return SkillTest(skill, example, emitter).run(loader)
