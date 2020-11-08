[![Build Status](https://travis-ci.com/rickyphewitt/emby-skill.svg?branch=master)](https://travis-ci.com/rickyphewitt/emby-skill)
# Emby
This skill allows audio playback from an Emby server

## About 
Stream music from your Emby server using Mycroft! Play all songs by an artist or an instant mix of any artist/album/song in your Emby library. 

## Examples 
* "Play Dance Gavin Dance From Emby"
* "Play Artist Thrice From Emby"
* "Play Album Deadweight From Emby"
* "Play Playlist Rockin Tunes From Emby"
* "Play Song Stitch From Emby"


## Common Play Framework
This skill supports the common play framework! This means you don't have to specify "Emby" in your intent. For Example
* "Play The Beatles"

## Credits 
rickyphewitt

## Category
**Music**

## Tags
#Emby,#Music

## Contributing
Always looking for bug fixes, features, translation, and feedback that make the Emby for Mycroft experience better!

## Troubleshooting
### Setup Connection Info
* Ensure your host, port, username, and password are set at https://account.mycroft.ai/skills
### Check Server Connection
* "Check Emby"
    * This will attempt to connect then authenticate to your Emby server using the connection info provided above

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


