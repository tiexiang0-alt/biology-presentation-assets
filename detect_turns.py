
from pydub import AudioSegment, silence

def get_turn_timestamps(file_path):
    audio = AudioSegment.from_wav(file_path)
    # Get all non-silent intervals
    # min_silence_len=300ms, silence_thresh=-40dB
    nonsilent_intervals = silence.detect_nonsilent(audio, min_silence_len=300, silence_thresh=-40)
    
    print("Detected Speech Segments (ms):")
    for i, (start, end) in enumerate(nonsilent_intervals):
        print(f"Segment {i}: {start} to {end} ({end-start}ms)")
        # Export each segment for verification if needed
        audio[start:end].export(f"verify_seg_{i}.wav", format="wav")


import sys
if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "dialogue_2.wav"
    get_turn_timestamps(fname)
