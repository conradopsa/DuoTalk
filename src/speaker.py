import os
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import torch
from TTS.api import TTS
from silence_detector import remove_ending_silence

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
        
        # fixing xtts model bug in portuguese (model speak "ponto" on the final of every speak)
        if lang == "pt" and text.endswith('.'):
            text = text[:-1]

        try:
            wav_filename = filename+".wav" 
            
            self.tts.tts_to_file(
                text=text, 
                speaker_wav=speaker, 
                language=lang, 
                file_path=wav_filename, 
                speed=speed,
                split_sentences=False,
                temperature=0.2, # default = 0.65
                repetition_penalty=6.0, # default = 2.0
                length_penalty=0.5, # default = 1.0
                # top_p=0.8, # default = 0.8
                # top_k=20, # default = 50
                enable_text_splitting=False,
                num_beams=6
            )
            
            audio = AudioSegment.from_wav(wav_filename)

            audioCleaned = remove_ending_silence(audio)

            white_noise = WhiteNoise()
            # Creating silence
            silence_left_audio = white_noise.to_audio_segment(duration=silence_left).apply_gain(-80)
            silence_right_audio = white_noise.to_audio_segment(duration=silence_right).apply_gain(-80)

            # Convert WAV to MP3 and Adding silence to fhe final
            (silence_left_audio + audioCleaned + silence_right_audio).export(filename, format="mp3")

            print("filename filename filename "+ filename)
            
            # Clean up temporary file
            os.unlink(wav_filename)
        except Exception as e:
            raise RuntimeError(f"TTS synthesis failed: {e}")

        return "generated"

