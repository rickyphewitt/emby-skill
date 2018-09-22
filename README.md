## Emby
This skill allows audio playback from an emby server

## Description
Stream music from your emby server using mycroft!

## Examples
 - " play instant mix for artist dance gavin dance from emby"


## Contributing
Always looking for bug fixes and features that make the Emby for Mycroft experience better!

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


## Credits
rickyphewitt


