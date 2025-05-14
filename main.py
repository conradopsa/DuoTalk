import os
import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from mutagen.id3 import ID3, USLT, ID3NoHeaderError
from mutagen.mp3 import MP3


from deep_translator import GoogleTranslator
import spacy

nlp = spacy.load("en_core_web_sm")

# Cria diretório de saída
os.makedirs("audios", exist_ok=True)

# Initialize AWS Polly
polly_client = boto3.Session().client("polly")

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
        return "[erro na tradução]"

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

def generate_tts_polly(text, filename, lang='en', rate="medium"):
    if os.path.isfile(filename):
        # print("[WARN]: File already exists, so nothing to do on generate_tts_polly")
        return "skiped"

    if not text.strip():
        raise ValueError("Empty text provided to Polly.")

    if lang == 'pt':
        voice_id = 'Vitoria'
    else:
        voice_id='Joanna'

    ssmlText = f"""
        <speak>
            <prosody rate="{rate}">
                {text}
            </prosody>
        </speak>
    """

    try:
        response = polly_client.synthesize_speech(
            TextType="ssml",
            Text=ssmlText,
            VoiceId=voice_id,
            OutputFormat='mp3',
            LanguageCode='en-US' if lang == 'en' else 'pt-BR'
        )
        with open(filename, 'wb') as f:
            f.write(response['AudioStream'].read())
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Polly synthesis failed: {e}")
    
    return "generated"

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_sentence(prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        base_filename = f"audios/{prefix}_{i:06d}"

        # Translated audio
        translated_file = f"{base_filename}_1_pt.mp3"
        translated = translate_text(sentence)
        status_translated = generate_tts_polly(translated, translated_file, 'pt', 'slow')
        embed_lyric(translated, translated_file, 'por')

        # Slow audio
        slow_file = f"{base_filename}_2_en_slow.mp3"
        status_slow = generate_tts_polly(sentence, slow_file, 'en', 'x-slow')
        embed_lyric(sentence, slow_file)

        # Main audio
        main_file = f"{base_filename}_3_en.mp3"
        status_main = generate_tts_polly(sentence, main_file, 'en', 'slow')
        embed_lyric(sentence, main_file)
        
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_translated},{status_slow},{status_main})"
    except Exception as e:
        return f"[error] Frase {i+1} '{sentence}': {e}"

def process_all(prefix, sentences):
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(process_sentence, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            print(future.result())

def process_text(text, prefix):
    sentences = split_sentences(text)
    process_all(prefix, sentences)


# Exemplo de uso
texto_ingles = """
Good morning. 
"""

process_text(texto_ingles, "good_morning")
