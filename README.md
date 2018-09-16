## Emby
This skill allows audio playback from an emby server

## Description
Stream music from your emby server using mycroft!

## Examples
 - "Play artist from emby"
 - "Play album from emby"
 - "Play song from emby"
 - "Play artist artist1 from emby"
 - "Play album album1 from emby"
 - "Play song song1 from emby"
 - "Play instant mix for artist"
 - "Play instant mix for album"
 - "Play instant mix for song"
 - "Play random"


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

## Credits
rickyphewitt


