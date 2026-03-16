
from pydub import AudioSegment

def split_l6_p7(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise boundaries for the 4 parts in Part 7
    # Based on turn patterns:
    # S1: Segs 0-1 (0 to 4800)
    # S2: Segs 2-4 (5000 to 8600)
    # S3 (Conversation): Segs 5-6 (9000 to 12600)
    # S4: Seg 7 (13000 to 16500)
    
    boundaries = [
        (0, 4800),      # S1: 李さんは 先月 佐藤さんと...
        (5000, 8800),   # S2: 王さんは 10月に...
        (9000, 12800),  # S3: いつ フランスへ... 行きます。
        (13000, 16500)  # S4: 大阪の 駅から...
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p7_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p7("lesson_6_part_7.wav")
