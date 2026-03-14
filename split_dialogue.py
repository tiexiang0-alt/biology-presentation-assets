
import librosa
import numpy as np
import os
from pydub import AudioSegment

def split_audio(file_path):
    print(f"Loading {file_path}...")
    y, sr = librosa.load(file_path, sr=24000)
    
    # 1. First, find all non-silent intervals to identify likely speech segments
    # use a relatively low top_db to catch soft speech
    intervals = librosa.effects.split(y, top_db=35)
    
    # We expect 5 main turns: S1, S2, S1, S2, S1
    # Let's extract MFCCs for each interval to identify speakers
    segments = []
    for i, (start, end) in enumerate(intervals):
        segment_audio = y[start:end]
        mfcc = librosa.feature.mfcc(y=segment_audio, sr=sr, n_mfcc=13)
        mean_mfcc = np.mean(mfcc, axis=1)
        segments.append({
            'start_sample': start,
            'end_sample': end,
            'start_sec': start / sr,
            'end_sec': end / sr,
            'mfcc': mean_mfcc
        })
    
    # If the previous ffmpeg failed, it's likely because Segment 4 and 5 were merged
    # because the pause between them was too short or quiet.
    # Let's look at the segments we found.
    print(f"Found {len(segments)} discrete speech intervals.")
    for i, s in enumerate(segments):
        print(f"Interval {i+1}: {s['start_sec']:.2f}s - {s['end_sec']:.2f}s")

    # Grouping logic:
    # Sentence 1: Segment 1
    # Sentence 2: Segment 2
    # Sentence 3: Segment 3
    # Sentence 4 & 5: If they are merged, we need to split by speaker timbre change.
    
    final_splits = []
    
    # Simple case: if we found exactly 5 intervals (unlikely if they merged)
    if len(segments) == 5:
        final_splits = [(s['start_sec'], s['end_sec']) for s in segments]
    else:
        # We probably have Segment 4 and 5 joined.
        # Let's analyze the long segment (usually the last one)
        long_segment = segments[-1]
        start_idx = long_segment['start_sample']
        end_idx = long_segment['end_sample']
        
        # Slide a window to find the speaker change
        chunk_size = int(sr * 0.5) # 0.5s window
        hop_size = int(sr * 0.1)  # 0.1s hop
        
        mfccs = []
        times = []
        for i in range(start_idx, end_idx - chunk_size, hop_size):
            chunk = y[i:i+chunk_size]
            m = np.mean(librosa.feature.mfcc(y=chunk, sr=sr, n_mfcc=13), axis=1)
            mfccs.append(m)
            times.append(i / sr)
        
        mfccs = np.array(mfccs)
        # Find the point where MFCCs change significantly (Speaker 2 -> Speaker 1)
        # We look for the maximum distance between adjacent chunks
        diffs = np.linalg.norm(mfccs[1:] - mfccs[:-1], axis=1)
        # Filter for the middle of the segment where the turn is expected
        # Dialogue says: Speaker 2 speaks, then Speaker 1 speaks.
        # So we look for a peak in diffs.
        peak_idx = np.argmax(diffs)
        split_time = times[peak_idx]
        
        print(f"Detected speaker change at approx {split_time:.2f}s")
        
        # Re-construct the 5 sentences
        # Sentence 1, 2, 3 are the first 3 segments
        for i in range(3):
            final_splits.append((segments[i]['start_sec'], segments[i]['end_sec']))
        
        # Sentence 4 is from start of long segment to split_time
        final_splits.append((long_segment['start_sec'], split_time))
        # Sentence 5 is from split_time to end of long segment
        final_splits.append((split_time, long_segment['end_sec']))

    # Export using pydub for precision
    audio = AudioSegment.from_wav(file_path)
    for i, (start, end) in enumerate(final_splits):
        # pydub uses milliseconds
        s_ms = start * 1000
        e_ms = end * 1000
        # Add a tiny buffer
        chunk = audio[max(0, s_ms - 50):min(len(audio), e_ms + 50)]
        out_name = f"d2_sentence_{i+1}.wav"
        chunk.export(out_name, format="wav")
        print(f"Exported {out_name}: {start:.2f}s - {end:.2f}s")

if __name__ == "__main__":
    split_audio("dialogue_2.wav")
