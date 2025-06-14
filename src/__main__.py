import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from speaker import Speaker
import lyrics
import splitter
import translator
import argparse
import mp3

SPEAKER_DEFAULT = "atlas" # "gaia" | "atlas" | "uranos"
MAX_CONCURRENCY = 1 # Workers

SILENCE_PT_LEFT = 1500 # ms
SILENCE_PT_RIGHT = 0 # ms
SILENCE_EN_LEFT = 1500 # ms
SILENCE_EN_RIGHT = 2000 # ms

SPEED = 0.5 # 1 is normal

def process_sentence(speaker, speaker_name, prefix, i, sentence, length):
    try:
        if not sentence.strip():
            return f"[skip] Empty sentence at {i}"

        dir = f"audios/{prefix}"
        os.makedirs(dir, exist_ok=True)

        base_filename = f"{dir}/{i:06d}"        

        speaker_path = f"samples/{speaker_name}.wav"

        # Translated audio
        translated_file = f"{base_filename}_1_pt.mp3"
        translated = translator.translate(sentence)
        status_translated =  speaker.generate_tts(translated, translated_file, 'pt', speaker_path, SPEED, SILENCE_PT_LEFT, SILENCE_PT_RIGHT)
        lyrics.embed(translated, translated_file, 'por')
        mp3.add_mp3_metadata(translated_file, title=translated, album=prefix, track=i*2-1) 

        # Main audio
        main_file = f"{base_filename}_2_en.mp3"
        status_main = speaker.generate_tts(sentence, main_file, 'en', speaker_path, SPEED,  SILENCE_EN_LEFT, SILENCE_EN_RIGHT)
        lyrics.embed(sentence, main_file)
        mp3.add_mp3_metadata(main_file, title=sentence, album=prefix, track=i*2) 
        return f"[done] prefix={prefix} progress={i}/{length} status=({status_translated}, {status_main})"
    except Exception as e:
        return f"[error] Frase {i+1} '{sentence}': {e}"

def process_all(prefix, sentences, speaker_name):
    speaker = Speaker()

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
        futures = [executor.submit(process_sentence, speaker, speaker_name, prefix, i+1, s, len(sentences)) for i, s in enumerate(sentences)]
        for future in as_completed(futures):
            print(future.result())

def process_text(text, prefix, speaker_name):
    sentences = splitter.split_text_advanced(text)
    process_all(prefix, sentences, speaker_name)

def read_file(filepath):
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

def getArgs():
    parser = argparse.ArgumentParser(description='Read a text file and optionally specify a speaker')
    parser.add_argument('filepath', help='Path to the text file to read')
    parser.add_argument('-s', '--speaker', help='Speaker name (e.g., gaia)', default=SPEAKER_DEFAULT)
    
    # Parse arguments
    args = parser.parse_args()

    return args
    
def main():  
    args = getArgs()

    filepath = args.filepath
    speaker_name = args.speaker

    content = read_file(filepath)
    filename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
    
    prefix = f"{filename_without_ext}_{speaker_name}"

    process_text(content, prefix, speaker_name)

main()