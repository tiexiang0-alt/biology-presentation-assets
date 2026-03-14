
from pydub import AudioSegment

def split_l6_p5(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    boundaries = [
        (0, 3500),      # S1: 私の部屋には 電話が ありません。
        (4000, 8500),   # S2: 韓国へは 行きました。中国へは 行きませんでした。
        (9000, 12500),  # S3: 私の誕生日は 4月 20日です。
        (13000, 16500), # S4: 5月 5日は 子供の日です。
        (16800, 21000)  # S5: 来月の 14日に 美術館へ 行きます。
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_p5_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l6_p5("lesson_6_part_5.wav")
