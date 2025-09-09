import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .speaker import Speaker
from duotalker import splitter, translator, mp3
from threading import Lock
import time

MAX_CONCURRENCY = 30 # Workers

SILENCE_PT_LEFT = 1500 # ms
SILENCE_PT_RIGHT = 0 # ms
SILENCE_EN_LEFT = 1500 # ms
SILENCE_EN_RIGHT = 2000 # ms

SPEED = 0.5 # 1 is normal

OUTPUT_FOLDER = "audios"

lock = Lock()

def write_performance(start, prefix, totalChars):
    generation_time = time.time() - start

    dir = f"{OUTPUT_FOLDER}/{prefix}/performance.log"

    with open(dir, "w") as f:
        f.write(f"generation_time: {generation_time:.2f}s\n")
        f.write(f"chars_count: {totalChars}\n")
        f.write(f"speed: {SPEED}\n")
        f.write(f"max_concurrency: {MAX_CONCURRENCY}\n")

def _process_sentence(speaker_instance, speaker_name, prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        dir = f"{OUTPUT_FOLDER}/{prefix}"
        os.makedirs(dir, exist_ok=True)

        base_filename = f"{dir}/{i:06d}"        

        speaker_path = f"samples/{speaker_name}.wav"

        # Translated audio
        translated_file = f"{base_filename}_1_pt.mp3"
        translated = translator.translate(sentence)
        with lock:
            status_translated = speaker_instance.generate_tts(translated, translated_file, 'pt', speaker_path, SPEED, SILENCE_PT_LEFT, SILENCE_PT_RIGHT)
        mp3.add_lyrics(translated_file, translated, 'por')
        mp3.add_metadata(translated_file, title=translated, album=prefix, track=i*2-1) 

        # Main audio
        main_file = f"{base_filename}_2_en.mp3"
        with lock:
            status_main = speaker_instance.generate_tts(sentence, main_file, 'en', speaker_path, SPEED,  SILENCE_EN_LEFT, SILENCE_EN_RIGHT)
        mp3.add_lyrics(main_file, sentence)
        mp3.add_metadata(main_file, title=sentence, album=prefix, track=i*2) 

        charCount = len(translated) + len(sentence)
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_translated}, {status_main})", charCount
    except Exception as e:
        return f"[error] Phrase {i+1} '{sentence}': {e}"

def _process_all(prefix, sentences, speaker_name):
    start = time.time()
    totalChars = 0

    speaker = Speaker()

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
        futures = [executor.submit(_process_sentence, speaker, speaker_name, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            output, charCount = future.result()
            totalChars+=charCount
            print(output)

    write_performance(start, prefix, totalChars)

def _process_text(text, prefix, speaker_name):
    sentences = splitter.split_text_advanced(text)
    _process_all(prefix, sentences, speaker_name)

def _read_file(filepath):
    """Read and return the contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filepath}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{filepath}' as UTF-8 text.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def start_from_file(filepath, speaker_name):
    content = _read_file(filepath)
    filename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
    
    prefix = f"{filename_without_ext} {speaker_name}"

    _process_text(content, prefix, speaker_name)

def start_from_content(name, content, speaker_name):
    prefix = f"{name} {speaker_name}"

    _process_text(content, prefix, speaker_name)
    
    