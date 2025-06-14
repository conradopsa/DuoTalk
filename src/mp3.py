from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

artist="DuoTalk"

def add_mp3_metadata(filename, title=None, album=None, track=None):
    try:
        audio = MP3(filename, ID3=EasyID3)
    except Exception:
        # If there's no ID3 tag yet, create one
        audio = MP3(filename)
        audio.add_tags(ID3=EasyID3)
        audio = MP3(filename, ID3=EasyID3)

    if title:
        audio['title'] = title
    if album:
        audio['album'] = album
    if track:
        audio['tracknumber'] = str(track)
    if artist:
        audio['artist'] = artist

    audio.save()