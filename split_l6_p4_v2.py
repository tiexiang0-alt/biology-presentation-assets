
from pydub import AudioSegment

def resplit_l6_p4_strict_5(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Re-calculating boundaries for 5 independent files
    # Based on the previous detection:
    # Segs 0,1: Li-san... (0-5000)
    # Segs 2,3: Tokyo-Kyoto... (5200-9500)
    # Segs 4,5: Kyoto station... (9700-13500)
    # Seg 6: Taxi... (14200-16500)
    # Segs 7,8,9: Night... (16800-21500)
    
    boundaries = [
        (0, 5000),      # S1: 李さんは 先月...
        (5200, 9500),   # S2: 東京から 京都まで...
        (9700, 13800),  # S3: 京都の 駅から...
        (14200, 16500), # S4: タクシーで...
        (16800, 21500)  # S5: 夜、 美術馆から...
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p4_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    resplit_l6_p4_strict_5("lesson_6_part_4.wav")
