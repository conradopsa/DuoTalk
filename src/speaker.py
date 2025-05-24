import os
from pydub import AudioSegment
import torch
from TTS.api import TTS

torch.serialization.add_safe_globals([
    'TTS.tts.configs.xtts_config.XttsConfig'
])

device = "cuda" if torch.cuda.is_available() else "cpu"

print(TTS().list_models())

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)

def generate_tts(text, filename, lang, speaker, speed, silence_between):
    if os.path.isfile(filename):
        return "skipped"

    if not text.strip():
        raise ValueError("Empty text provided to Tortoise TTS.")

    try:
        wav_filename = filename+".wav" 
        tts.tts_to_file(
            text=text, 
            speaker_wav=speaker, 
            language=lang, 
            file_path=wav_filename, 
            speed=speed,
            split_sentences=False
        )

        
        audio = AudioSegment.from_wav(wav_filename)

        # Creating silence
        silence = AudioSegment.silent(duration=silence_between)

        # Convert WAV to MP3 and Adding silence to fhe final
        (audio + silence).export(filename, format="mp3")

        print("filename filename filename "+ filename)
        
        # Clean up temporary file
        os.unlink(wav_filename)
    except Exception as e:
        raise RuntimeError(f"TTS synthesis failed: {e}")

    return "generated"

