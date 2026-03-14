
import librosa
import numpy as np
import os
from pydub import AudioSegment

def split_dialogue_final(file_path):
    print(f"Loading {file_path}...")
    y, sr = librosa.load(file_path, sr=24000)
    
    # Based on previous analysis, these are the likely Turn boundaries
    # We will refine them by finding the actual silence in these regions
    candidates = [5.2, 9.5, 11.0, 16.5]
    
    # Final boundaries
    boundaries = [0.0]
    
    for c in candidates:
        # Look for silence around the candidate (+/- 0.5s)
        start_search = int((c - 0.5) * sr)
        end_search = int((c + 0.5) * sr)
        search_window = y[start_search:end_search]
        
        # Find the point with minimum energy in this window
        rms = librosa.feature.rms(y=search_window, frame_length=512, hop_length=128)[0]
        min_idx = np.argmin(rms)
        silence_pos = (start_search + min_idx * 128) / sr
        boundaries.append(silence_pos)
        
    boundaries.append(len(y) / sr)
    
    print("Identified speaker turn boundaries:")
    for i in range(len(boundaries)-1):
        print(f"Turn {i+1}: {boundaries[i]:.2f}s - {boundaries[i+1]:.2f}s")

    # Export
    audio = AudioSegment.from_wav(file_path)
    for i in range(5):
        s_ms = boundaries[i] * 1000
        e_ms = boundaries[i+1] * 1000
        # Crop leading/trailing silence within the segment
        segment = audio[s_ms : e_ms]
        
        # Strip exact silence to make it clean
        # (Using a simple dB threshold)
        out_audio = segment.strip_silence(silence_thresh=-35, padding=100)
        
        out_name = f"d2_sentence_{i+1}.wav"
        out_audio.export(out_name, format="wav")
        print(f"Exported {out_name}")

if __name__ == "__main__":
    split_dialogue_final("dialogue_2.wav")
