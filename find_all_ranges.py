
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def find_all_sentences(file_path):
    audio = AudioSegment.from_wav(file_path)
    # Detect all speech intervals
    ranges = detect_nonsilent(audio, min_silence_len=300, silence_thresh=-40)
    for i, r in enumerate(ranges):
        print(f"Interval {i}: {r} (len: {r[1]-r[0]}ms)")

if __name__ == "__main__":
    find_all_sentences("lesson_7_part_1.wav")
