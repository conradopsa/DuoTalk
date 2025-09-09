import os
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import torch
import psutil

from auralis import TTS, TTSRequest

from .silence_detector import remove_ending_silence

class Speaker:
    def __init__(self):
        print("---------------------- INIT ----------------------")
        # # Initialize once when creating the instance
        # torch.serialization.add_safe_globals([
        #     'TTS.tts.configs.xtts_config.XttsConfig'
        # ])
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # print(TTS().list_models())

        print(f"🔍 DIAGNÓSTICO DO SISTEMA:")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM Total: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        print(f"RAM Total: {psutil.virtual_memory().total / 1024**3:.1f}GB")
        print(f"RAM Disponível: {psutil.virtual_memory().available / 1024**3:.1f}GB")
        print(f"Swap: {psutil.swap_memory().total / 1024**3:.1f}GB")

        self.tts = TTS().from_pretrained(
            "AstraMindAI/xttsv2", 
            gpt_model='AstraMindAI/xtts2-gpt', 
            # max_concurrency=1,
            # max_seq_len_to_capture=1024, 
            # device="gpu"           
        )

        print("---------------------- INITIATE ----------------------")

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
            
            # self.tts.tts_to_file(
            #     text=text, 
            #     speaker_wav=speaker, 
            #     language=lang, 
            #     file_path=wav_filename, 
            #     speed=speed,
            #     split_sentences=False,
            #     temperature=0.2, # default = 0.65
            #     repetition_penalty=6.0, # default = 2.0
            #     length_penalty=0.5, # default = 1.0
            #     # top_p=0.8, # default = 0.8
            #     # top_k=20, # default = 50
            #     enable_text_splitting=False,
            #     num_beams=6
            # )

            # Generate speech
            request = TTSRequest(
                text=text,
                speaker_files=[speaker],                
                language=lang,
                repetition_penalty=6.0,
                length_penalty=0.5,
                # num_beams=6
            )

            with torch.no_grad():                
                output = self.tts.generate_speech(request)
            
            # torch.cuda.empty_cache()

            output.save(wav_filename)
                
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

