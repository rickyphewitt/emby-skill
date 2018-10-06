import pytest
from unittest import TestCase, mock
from emby_croft import EmbyCroft
from emby_client import MediaItemType, EmbyMediaItem

HOST = "http://emby:8096"
USERNAME = "Ricky"
PASSWORD = ""

"""
This test file is expected to have tests using mock's and using a real emby server
The expectation is that there will be 2 tests 1 that are exactly the same
1 that will utilize mocks for the calls to the emby server and another that
will actually call the Emby server and handle real responses. There is probably
a better way to do this but I'm lazy :)

"""


class TestEmbyCroft(object):
    # Emby server responses for mocked tests
    auth_server_response = {"User":{"Name":"UsernameHere","ServerId":"92fcf358310b4fa3ab856f7d10a8e6a0","Id":"4c8f86063b3e40f5a32ca020dd4ff60e","HasPassword":"false","HasConfiguredPassword":"false","HasConfiguredEasyPassword":"false","EnableAutoLogin":"true","LastLoginDate":"2018-09-19T12:31:25.9023096Z","LastActivityDate":"2018-09-19T12:31:25.9153650Z","Configuration":{"AudioLanguagePreference":"","PlayDefaultAudioTrack":"true","SubtitleLanguagePreference":"","DisplayMissingEpisodes":"false","GroupedFolders":[],"SubtitleMode":"None","DisplayCollectionsView":"false","EnableLocalPassword":"false","OrderedViews":["7e64e319657a9516ec78490da03edccb","4514ec850e5ad0c47b58444e17b6346c","f137a2dd21bbc1b99aa5c0f6bf02a805","bea99aea7b2571dd050f0aaac602f6c7","165db2549e77c71dacef0e83a95cc5de","9d7ad6afe9afa2dab1a2f6e00ad28fa6","36639a1729d2b576b60863a7b3b82349","e2fd3840dabe769e02751e41017c2b87"],"LatestItemsExcludes":["165db2549e77c71dacef0e83a95cc5de"],"MyMediaExcludes":[],"HidePlayedInLatest":"true","RememberAudioSelections":"true","RememberSubtitleSelections":"true","EnableNextEpisodeAutoPlay":"true"},"Policy":{"IsAdministrator":"true","IsHidden":"false","IsDisabled":"false","BlockedTags":[],"EnableUserPreferenceAccess":"true","AccessSchedules":[],"BlockUnratedItems":[],"EnableRemoteControlOfOtherUsers":"true","EnableSharedDeviceControl":"true","EnableRemoteAccess":"true","EnableLiveTvManagement":"true","EnableLiveTvAccess":"true","EnableMediaPlayback":"true","EnableAudioPlaybackTranscoding":"true","EnableVideoPlaybackTranscoding":"true","EnablePlaybackRemuxing":"true","EnableContentDeletion":"true","EnableContentDeletionFromFolders":[],"EnableContentDownloading":"true","EnableSyncTranscoding":"true","EnableMediaConversion":"true","EnabledDevices":[],"EnableAllDevices":"true","EnabledChannels":[],"EnableAllChannels":"true","EnabledFolders":[],"EnableAllFolders":"true","InvalidLoginAttemptCount":0,"EnablePublicSharing":"true","RemoteClientBitrateLimit":0,"AuthenticationProviderId":"Emby.Server.Implementations.Library.DefaultAuthenticationProvider"}},"SessionInfo":{"PlayState":{"CanSeek":"false","IsPaused":"false","IsMuted":"false","RepeatMode":"RepeatNone"},"AdditionalUsers":[],"Capabilities":{"PlayableMediaTypes":[],"SupportedCommands":[],"SupportsMediaControl":"false","SupportsPersistentIdentifier":"true","SupportsSync":"false"},"RemoteEndPoint":"10.11.12.249","PlayableMediaTypes":[],"Id":"51fc1c10655c18a3e13374649134f714","ServerId":"92fcf358310b4fa3ab856f7d10a8e6a0","UserId":"4c8f86063b3e40f5a32ca020dd4ff60e","UserName":"Ricky","Client":"mycroft","LastActivityDate":"2018-09-19T12:31:25.9153650Z","DeviceName":"mark1","DeviceId":"34343","ApplicationVersion":"0.1","SupportedCommands":[],"SupportsRemoteControl":"false"},"AccessToken":"4056e539cb60488f921ddc52fabe154e","ServerId":"92fcf358310b4fa3ab856f7d10a8e6a0"}

    @pytest.mark.live
    def test_auth(self):
        emby_client = EmbyCroft(HOST, USERNAME, PASSWORD)
        assert emby_client.client.auth is not None

    @pytest.mark.mocked
    def test_auth_mock(self):
        with mock.patch('requests.post') as MockRequestsPost:
            response = MockResponse(200, TestEmbyCroft.auth_server_response)
            MockRequestsPost.return_value = response
            emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

            assert emby_croft.client.auth.token is\
                   TestEmbyCroft.auth_server_response["AccessToken"]
            assert emby_croft.client.auth.user_id is\
                   TestEmbyCroft.auth_server_response["User"]["Id"]

    @pytest.mark.live
    def test_instant_mix(self):
        album = "This is how the wind shifts"
        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

        songs = emby_croft.instant_mix_for_media(album)
        assert songs is not None

    @pytest.mark.live
    def test_instant_mix(self):
        album = "This is how the wind shifts"
        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

        songs = emby_croft.instant_mix_for_media(album)
        assert songs is not None

    @pytest.mark.mocked
    def test_instant_mix(self):
        with mock.patch('requests.post') as MockRequestsPost:
            album = "This is how the wind shifts"
            response = MockResponse(200, TestEmbyCroft.auth_server_response)
            MockRequestsPost.return_value = response
            emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)

            songs = emby_croft.instant_mix_for_media(album)
            assert songs is not None

    @pytest.mark.live
    def test_search_for_song(self):
        song = "And I Told Them I Invented Times New Roman"

        emby_croft = EmbyCroft(HOST, USERNAME, PASSWORD)
        songs = emby_croft.search_song(song)
        assert len(songs) == 3
        for song_item in songs:
            assert song in song_item.name
            assert song_item.id is not None
            assert song_item.type == MediaItemType.SONG


class MockResponse:
    def __init__(self, status_code, json_data):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data