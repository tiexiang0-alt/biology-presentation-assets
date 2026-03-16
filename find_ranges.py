
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def find_sub_segments(file_path):
    audio = AudioSegment.from_wav(file_path)
    # Focus on the first 5 seconds
    clip = audio[:5000]
    # Detect nonsilent parts with shorter silence threshold
    # The default is 500ms, let's try 100ms
    ranges = detect_nonsilent(clip, min_silence_len=100, silence_thresh=-40)
    print(ranges)

if __name__ == "__main__":
    find_sub_segments("lesson_7_part_1.wav")
