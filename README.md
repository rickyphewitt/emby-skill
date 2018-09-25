# <img src='https://rawgithub.com/FortAwesome/Font-Awesome/master/advanced-options/raw-svg/solid/play.svg' card_color='#52B54B' width='50' height='50' style='vertical-align:bottom'/> Emby
This skill allows audio playback from an Emby server

## About 
Stream music from your Emby server using Mycroft! Right now you can play an instant mix of any artist/album/song in your Emby library. 

## Examples 
* "Play Dance Gavin Dance From Emby"

## Credits 
rickyphewitt

## Category
**Music**

## Tags
#Emby,#Music
    
## Coming Soon
- Play artist Thrice from Emby
    * Shuffles all Thrice songs
- Play album This is how the wind shifts from Emby
    * Plays the album This is how the wind shifts 

## Contributing
Always looking for bug fixes and features that make the Emby for Mycroft a experience better!

### Dev Notes
Skill is broken down into 3 main parts
* emby_client.py
    * An intentionally lean synchronous Emby client
* emby_croft.py
    * Logic layer between Emby client and Mycroft
* __init__.py
    * Mycroft skill hooks

### Testing
* Unit tests should be added to the test/unit directory

This test files are expected to have tests using mocks and using a real Emby server.
The expectation is that there will be 2 tests that are exactly the same;
1 that will utilize mocks for the calls to the Emby server and another that
will actually call the Emby server and handle real responses. 
They will be distinguished by pytest marks. All tests marked with 'mocked' will be ran
on each push to git via travis CI. 


