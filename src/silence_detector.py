from pydub import AudioSegment
from pydub.silence import detect_silence

def remove_ending_silence(audio: AudioSegment, silence_thresh=-50.0, min_silence_len=1000, tolerance=100) -> AudioSegment:
    silence = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    if silence:
        last_silence_start, last_silence_end = silence[-1]
        # If the silence ends at or very close to the end of the audio
        if len(audio) - last_silence_end <= tolerance:
            return audio[:last_silence_start]

    return audio