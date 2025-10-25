from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT, ID3NoHeaderError

ARTIST="DuoVox"
MAX_TRACK_NUM=200

def add_metadata(filename, title, album, track):
    try:
        audio = MP3(filename, ID3=EasyID3)
    except Exception:
        # If there's no ID3 tag yet, create one
        audio = MP3(filename)
        audio.add_tags(ID3=EasyID3)
        audio = MP3(filename, ID3=EasyID3)


    disc_number = ((track - 1) // MAX_TRACK_NUM) + 1
    track_in_disc = ((track - 1) % MAX_TRACK_NUM) + 1

    audio['tracknumber'] = str(track_in_disc)
    audio['discnumber'] = str(disc_number)
    audio['album'] = f"{album} {disc_number}"
    audio['title'] = title
    audio['artist'] = ARTIST

    audio.save()


def add_lyrics(filename, text, lang='eng'):
    try:
        try:
            audio = ID3(filename)
        except ID3NoHeaderError:
            audio = ID3()

        # Remove old lyrics to avoid duplicates
        audio.delall("USLT")

        lyrics_tag = USLT(
            encoding=3,
            lang=lang[:3],  # 'eng' or 'por'
            desc="TTS Text",
            text=text
        )
        audio.add(lyrics_tag)
        audio.save(filename)
    except Exception as e:
        raise RuntimeError(f"Failed to add lyrics: {e}")