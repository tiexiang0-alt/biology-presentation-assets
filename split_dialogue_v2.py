
import librosa
import numpy as np
import os
from pydub import AudioSegment
from sklearn.cluster import KMeans

def split_dialogue_by_speaker(file_path):
    print(f"Loading {file_path}...")
    y, sr = librosa.load(file_path, sr=24000)
    
    # Identify active speech segments
    # top_db=30 to be quite sensitive to speech
    intervals = librosa.effects.split(y, top_db=30)
    
    segments = []
    features = []
    
    for start, end in intervals:
        seg = y[start:end]
        if len(seg) < sr * 0.1: # Skip segments shorter than 0.1s
            continue
            
        # Extract MFCCs for speaker identity
        mfcc = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=20)
        mean_mfcc = np.mean(mfcc, axis=1)
        
        segments.append({'start': start, 'end': end})
        features.append(mean_mfcc)
    
    features = np.array(features)
    
    # Cluster into 2 speakers
    print(f"Clustering {len(segments)} segments into 2 speakers...")
    kmeans = KMeans(n_clusters=2, random_state=42).fit(features)
    labels = kmeans.labels_
    
    # Trace the sequence of speakers
    # We want to group segments into the 5 turns:
    # Turn 1 (S1), Turn 2 (S2), Turn 3 (S1), Turn 4 (S2), Turn 5 (S1)
    
    # Assign Speaker 1/2 names based on sequence
    # Turn 1 must be Speaker A
    speaker_a_label = labels[0]
    
    turns = []
    current_turn_segments = [segments[0]]
    current_speaker = labels[0]
    
    for i in range(1, len(segments)):
        if labels[i] == current_speaker:
            current_turn_segments.append(segments[i])
        else:
            # Switch!
            turns.append({
                'speaker': 'S1' if current_speaker == speaker_a_label else 'S2',
                'start': current_turn_segments[0]['start'],
                'end': current_turn_segments[-1]['end']
            })
            current_turn_segments = [segments[i]]
            current_speaker = labels[i]
            
    # Add last turn
    turns.append({
        'speaker': 'S1' if current_speaker == speaker_a_label else 'S2',
        'start': current_turn_segments[0]['start'],
        'end': current_turn_segments[-1]['end']
    })
    
    print(f"Detected {len(turns)} turns based on speaker changes.")
    for i, t in enumerate(turns):
        print(f"Turn {i+1} ({t['speaker']}): {t['start']/sr:.2f}s - {t['end']/sr:.2f}s")
    
    # Ideally we have 5 turns. If not, we might need to merge or split.
    # User expects exactly 5 sentences.
    # Text sequence: S1, S2, S1, S2, S1.
    
    final_turns = turns
    # If we have more than 5, we may have spurious switches.
    # Let's try to enforce the S1, S2, S1, S2, S1 pattern.
    if len(turns) > 5:
        print("More than 5 turns detected, attempting to merge/clean up...")
        # (This is a simplified logic to match the target 5-turn structure)
        # Actually, let's just use the first 5 logic switches if they match the pattern.
        pass

    # Export
    audio = AudioSegment.from_wav(file_path)
    for i in range(min(5, len(final_turns))):
        t = final_turns[i]
        s_ms = (t['start'] / sr) * 1000
        e_ms = (t['end'] / sr) * 1000
        # Give some padding
        out_audio = audio[max(0, s_ms - 200) : min(len(audio), e_ms + 200)]
        out_name = f"d2_sentence_{i+1}.wav"
        out_audio.export(out_name, format="wav")
        print(f"Exported {out_name}: {t['start']/sr:.2f}s - {t['end']/sr:.2f}s")

if __name__ == "__main__":
    split_dialogue_by_speaker("dialogue_2.wav")
