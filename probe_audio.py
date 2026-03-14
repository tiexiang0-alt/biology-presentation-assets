
import librosa
import numpy as np
from pydub import AudioSegment, silence

def probe_audio(file_path):
    print(f"Probing {file_path} for detailed turns...")
    audio = AudioSegment.from_wav(file_path)
    
    # Use a very sensitive silence detection
    # min_silence_len=100ms, silence_thresh=-40dB
    chunks = silence.split_on_silence(audio, min_silence_len=100, silence_thresh=-40, keep_silence=50)
    
    print(f"Detected {len(chunks)} possible small phrases.")
    for i, chunk in enumerate(chunks):
        chunk.export(f"probe_chunk_{i}.wav", format="wav")
        print(f"Chunk {i}: length {len(chunk)}ms")

if __name__ == "__main__":
    probe_audio("dialogue_2.wav")
