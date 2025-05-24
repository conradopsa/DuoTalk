from mutagen.id3 import ID3, USLT, ID3NoHeaderError

def embed(text, filename, lang='eng'):
    try:
        try:
            audio = ID3(filename)
        except ID3NoHeaderError:
            audio = ID3()

        # Remove old lyrics to avoid duplicates
        audio.delall("USLT")

        lyrics_tag = USLT(
            encoding=3,
            lang=lang[:3],  # 'eng' or 'pt'
            desc="TTS Text",
            text=text
        )
        audio.add(lyrics_tag)
        audio.save(filename)
    except Exception as e:
        raise RuntimeError(f"Failed to add lyrics: {e}")