
from pydub import AudioSegment

def split_l6_p6_v2(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Boundaries based on detected segments
    boundaries = [
        (0, 3200),      # S1
        (3500, 6500),   # S2
        (6800, 9800),   # S3
        (10200, 14000), # S4
        (14200, 17500)  # S5
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p6_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p6_v2("lesson_6_part_6_v2.wav")
