
from pydub import AudioSegment

def split_l7_p1(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Boundaries for 6 sentences in lesson 7 part 1
    # S1: Segs 0-1 (0~4000) 李さんは 毎朝、コーヒーを飲みます。
    # S2: Segs 2-3 (4000~7500) 私はパンと卵を食べます。
    # S3: Segs 4-5 (7500~10000) 王さんはお粥を食べます。
    # S4: Segs 6-7 (10400~13500) 昼、食堂で親子丼を食べます。
    # S5: Segs 8-9 (14000~16800) 夜、日本のお茶を飲みます。
    # S6: Segs 10-11 (17500~21000) 茶道は「一期一会」の心です。
    
    boundaries = [
        (0, 4000),       # S1
        (4000, 7500),    # S2
        (7500, 10300),   # S3
        (10400, 13700),  # S4
        (14000, 17000),  # S5
        (17500, 21500)   # S6
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l7_p1_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms")

if __name__ == "__main__":
    split_l7_p1("lesson_7_part_1.wav")
