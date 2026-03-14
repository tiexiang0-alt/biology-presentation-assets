
from pydub import AudioSegment

def split_l6_p4(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise boundaries for the 5 sentences based on detection
    # S1: Segments 0 & 1
    # S2: Segments 2 & 3
    # S3: Segments 4 & 5
    # S4: Segment 6
    # S5: Segments 7, 8 & 9
    
    boundaries = [
        (0, 5000),      # S1: 李さんは 先月 友達と 一緒に 京都へ 行きました。
        (5200, 9500),   # S2: 東京から 京都まで 新幹線で 行きました。
        (9700, 14000),  # S3: 京都の 駅から 美術館まで 歩いて 行きました。
        (14200, 16500), # S4: タクシーで 行きませんでした。
        (16800, 22000)  # S5: 夜、 美術館から アパートまで 電車で 帰りました。
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p4_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p4("lesson_6_part_4.wav")
