import os
import spacy
from mutagen.id3 import ID3, USLT, ID3NoHeaderError
from deep_translator import GoogleTranslator
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
from pydub import AudioSegment

import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed

nlp = spacy.load("en_core_web_sm")

# Output dir
os.makedirs("audios", exist_ok=True)

def split_sentences(text):
    sentences = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        doc = nlp(line)
        sentences.extend([sent.text.strip() for sent in doc.sents])
    return sentences

def translate_text(text, src='en', dest='pt'):
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        print(f"[translation error] {e}")
        return "[translation error]"

def embed_lyric(text, filename, lang='eng'):
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

def generate_tts_tortoise(text, filename, lang='en', rate="medium", voice='daniel'):
    print("-------- Generate MP3 using pydub conversion --------")
    if os.path.isfile(filename):
        return "skipped"

    if not text.strip():
        raise ValueError("Empty text provided to Tortoise TTS.")

    try:
        # Initialize TTS
        tts = TextToSpeech()
        
        # Load voice
        voice_samples, conditioning_latents = load_voice(voice)
        

        print("-------- gen --------")
        # Generate audio
        gen = tts.tts_with_preset(
            text,
            voice_samples=voice_samples,
            conditioning_latents=conditioning_latents,
            preset="fast"
        )

        print("-------- pcm --------")
        # Step 2: Convert to NumPy and scale to int16
        pcm = gen.cpu().numpy()  # convert from PyTorch tensor to NumPy array
        pcm16 = (pcm * 32767).astype(np.int16)

        print("-------- audioSegment --------")
        # Step 3: Create a pydub AudioSegment
        audio = AudioSegment(
            pcm16.tobytes(), 
            frame_rate=24000,
            sample_width=2,      # 16-bit
            channels=1           # mono
        )

        print("-------- export --------")

        # Step 4: Export to MP3
        audio.export(filename, format="mp3", bitrate="192k")

    except Exception as e:
        raise RuntimeError(f"Tortoise TTS synthesis failed: {e}")

    return "generated"



def process_sentence(prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        base_filename = f"audios/{prefix}_{i:06d}"

        # # Translated audio
        # translated_file = f"{base_filename}_1_pt.mp3"
        # translated = translate_text(sentence)
        # status_translated = generate_tts_tortoise(translated, translated_file, 'pt', 'slow')
        # embed_lyric(translated, translated_file, 'por')

        # # Slow audio
        # slow_file = f"{base_filename}_2_en_slow.mp3"
        # status_slow = generate_tts_tortoise(sentence, slow_file, 'en', 'x-slow')
        # embed_lyric(sentence, slow_file)

        # Main audio
        main_file = f"{base_filename}_3_en.mp3"
        status_main = generate_tts_tortoise(sentence, main_file, 'en', 'slow')
        embed_lyric(sentence, main_file)
        
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_main})"
    except Exception as e:
        return f"[error] Frase {i+1} '{sentence}': {e}"

def process_all(prefix, sentences):
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(process_sentence, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            print(future.result())

def process_text(text, prefix):
    sentences = split_sentences(text)
    process_all(prefix, sentences)


# Exemplo de uso
texto_ingles = """
AUDIO SCRIPT FOR HALF-LIFE
Good morning and welcome to the Black Mesa Transit System. This automated train is provided for the security and convenience of employees of the Black Mesa Research Facility personnel. Please feel free to move about the train or simply sit back and enjoy the ride.
"""

process_text(texto_ingles, "halflife")
