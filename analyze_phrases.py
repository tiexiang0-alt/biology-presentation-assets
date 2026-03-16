
import sys
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def analyze_phrases(file_path):
    print(f"Analyzing {file_path}...")
    audio = AudioSegment.from_wav(file_path)
    # Detect nonsilent parts with 200ms threshold
    phrases = detect_nonsilent(audio, min_silence_len=200, silence_thresh=-40)
    for i, p in enumerate(phrases):
        print(f"Phrase {i}: {p} len={p[1]-p[0]}ms")

if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "lesson_7_part_1.wav"
    analyze_phrases(fn)
