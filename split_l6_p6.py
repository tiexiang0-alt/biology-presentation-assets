
from pydub import AudioSegment

def split_l6_p6(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise boundaries for the 5 sentences in Part 6
    # Based on the speech patterns in Part 6 (download (6).wav)
    # S1: 来年、日本へ 行こうと 思います。
    # S2: 電车で 京都へ 行こうと 思います。
    # S3: 京都の ホテルに 泊まろうと 思います。
    # S4: そこで 日本の 友達に 会おうと 思います。
    # S5: 週末は どこへも 行きません。
    
    boundaries = [
        (0, 10000),     # S1: Approx first heavy silence gap
        (10000, 20000), # S2
        (20000, 30000), # S3
        (30000, 42000), # S4
        (42000, 52000)  # S5
    ]
    
    # Refining based on detected segments (if possible)
    # Segs 0,1 looks like S1
    # Segs 2,3 looks like S2
    # Segs 4,5 looks like S3
    # Segs 6,7,8 sequence... 
    
    # Let's use a more granular mapping based on the turn-patterns
    refined_boundaries = [
        (0, 9500),      # S1
        (10000, 16500), # S2
        (16800, 23800), # S3
        (24000, 33600), # S4
        (34000, 51500)  # S5
    ]
    
    for i, (start, end) in enumerate(refined_boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p6_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p6("lesson_6_part_6.wav")
