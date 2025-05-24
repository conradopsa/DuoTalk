import os
import spacy
from mutagen.id3 import ID3, USLT, ID3NoHeaderError
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import torch
from TTS.api import TTS
from concurrent.futures import ThreadPoolExecutor, as_completed

SPEAKER = "gaia" # "gaia" | "uranos" | "atlas" | "conrado"
MAX_CONCURRENCY = 1 # Workers
SILENCE_BETWEEN = 2000 # Seconds
SPEED = 0.8 # 1 is normal

torch.serialization.add_safe_globals([
    'TTS.tts.configs.xtts_config.XttsConfig'
])

device = "cuda" if torch.cuda.is_available() else "cpu"

nlp = spacy.load("en_core_web_sm")

print(TTS().list_models())

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)

def split_audio_text_advanced(text, min_chunk_size=3, target_chunk_size=5, max_chunk_size=8):
    """
    Advanced version with better phrase boundary detection.
    """
    import re
    
    text = text.strip()
    if not text:
        return []
    
    # Split into sentences first
    sentences = re.split(r'[.!?]+', text)
    all_chunks = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        words = sentence.split()
        if len(words) <= max_chunk_size:
            # If sentence is short enough, keep it as one chunk
            all_chunks.append(sentence)
            continue
        
        # Split longer sentences
        chunks = []
        current_chunk = []
        
        for i, word in enumerate(words):
            current_chunk.append(word)
            
            should_break = False
            
            # Force break at max size
            if len(current_chunk) >= max_chunk_size:
                should_break = True
            
            # Look for natural breaks after reaching target size
            elif len(current_chunk) >= target_chunk_size:
                # Break after commas
                if word.endswith(','):
                    should_break = True
                
                # Break before conjunctions and prepositions
                elif i + 1 < len(words):
                    next_word = words[i + 1].lower()
                    break_words = [
                        'and', 'or', 'but', 'yet', 'so', 'for', 'nor',  # conjunctions
                        'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from',  # prepositions
                        'the', 'a', 'an', 'this', 'that', 'these', 'those'  # articles
                    ]
                    if next_word in break_words:
                        should_break = True
            
            if should_break or i == len(words) - 1:
                chunk_text = ' '.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)
                current_chunk = []
        
        all_chunks.extend(chunks)
    
    return all_chunks

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

def generate_tts(text, filename, lang='en', speed=SPEED):
    print("-------- Generate --------")
    if os.path.isfile(filename):
        return "skipped"

    if not text.strip():
        raise ValueError("Empty text provided to Tortoise TTS.")

    try:
        wav_filename = filename+".wav" 
        tts.tts_to_file(
            text=text, 
            speaker_wav=f"samples/{SPEAKER}.wav", 
            language=lang, 
            file_path=wav_filename, 
            speed=speed,
            split_sentences=False
        )

        
        audio = AudioSegment.from_wav(wav_filename)

        # Creating silence
        silence = AudioSegment.silent(duration=SILENCE_BETWEEN)

        # Convert WAV to MP3 and Adding silence to fhe final
        (audio + silence).export(filename, format="mp3")

        print("filename filename filename "+ filename)
        
        # Clean up temporary file
        os.unlink(wav_filename)
    except Exception as e:
        raise RuntimeError(f"TTS synthesis failed: {e}")

    return "generated"



def process_sentence(prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        dir = f"audios/{prefix}"
        os.makedirs(dir, exist_ok=True)

        base_filename = f"{dir}/{i:06d}"        

        # Translated audio
        translated_file = f"{base_filename}_1_pt.mp3"
        translated = translate_text(sentence)
        status_translated = generate_tts(translated, translated_file, 'pt')
        embed_lyric(translated, translated_file, 'por')

        # Main audio
        main_file = f"{base_filename}_2_en.mp3"
        status_main = generate_tts(sentence, main_file, 'en')
        embed_lyric(sentence, main_file)
        
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_translated}, {status_main})"
    except Exception as e:
        return f"[error] Frase {i+1} '{sentence}': {e}"

def process_all(prefix, sentences):
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
        futures = [executor.submit(process_sentence, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            print(future.result())

def process_text(text, prefix):
    sentences = split_audio_text_advanced(text)
    process_all(prefix, sentences)


# Exemplo de uso
texto_ingles = """
AUDIO SCRIPT FOR Halflife.
Good morning and welcome to the Black Mesa Transit System. This automated train is provided for the security and convenience of employees of the Black Mesa Research Facility personnel. Please feel free to move about the train or simply sit back and enjoy the ride.
"""

process_text(texto_ingles, f"halflife_{SPEAKER}")
