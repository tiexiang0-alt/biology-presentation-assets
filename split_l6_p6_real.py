
from pydub import AudioSegment

def split_l6_p6_real(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Boundaries for lesson 6 part 6.wav (approx 20 seconds total)
    boundaries = [
        (0, 3200),      # S1: 来年、日本へ 行こうと 思います。
        (4500, 8800),   # S2: 電车で 京都へ 行こうと 思います。
        (9200, 12800),  # S3: 京都の ホテルに 泊まろうと 思います。
        (13200, 17200), # S4: そこで 日本の 友達に 会おうと 思います。
        (17500, 21000)  # S5: 週末は どこへも 行きません。
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p6_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p6_real("lesson_6_part_6_real.wav")
