import os
from pydub import AudioSegment
import torch
from TTS.api import TTS

class Speaker:
    def __init__(self):
        # Initialize once when creating the instance
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig'
        ])
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # print(TTS().list_models())

        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(self.device)

    def generate_tts(self, text, filename, lang, speaker, speed, silence_left, silence_right):
        if os.path.isfile(filename):
            return "skipped"

        if not text.strip():
            raise ValueError("Empty text provided to Tortoise TTS.")

        try:
            wav_filename = filename+".wav" 
            self.tts.tts_to_file(
                text=text, 
                speaker_wav=speaker, 
                language=lang, 
                file_path=wav_filename, 
                speed=speed,
                split_sentences=False
            )
            
            audio = AudioSegment.from_wav(wav_filename)

            # Creating silence
            silence_left_audio = AudioSegment.silent(duration=silence_left)
            silence_right_audio = AudioSegment.silent(duration=silence_right)

            # Convert WAV to MP3 and Adding silence to fhe final
            (silence_left_audio + audio + silence_right_audio).export(filename, format="mp3")

            print("filename filename filename "+ filename)
            
            # Clean up temporary file
            os.unlink(wav_filename)
        except Exception as e:
            raise RuntimeError(f"TTS synthesis failed: {e}")

        return "generated"

