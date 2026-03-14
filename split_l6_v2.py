
from pydub import AudioSegment

def split_l6_v2(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise segments from detection
    boundaries = [
        (347, 2446),  # 1. スミスさんは アメリカから 来ました。
        (3144, 4721), # 2. 明日、 会社へ 行きません。
        (5455, 6388), # 3. どこへ 行きますか。
        (7101, 8535), # 4. 京都の 美術館に 行きます。
        (9256, 10911) # 5. 週末は 温泉に 行きます。
    ]
    
    for i, (start, end) in enumerate(boundaries):
        # Add a tiny bit of padding
        chunk = audio[max(0, start-50):min(len(audio), end+50)]
        out_name = f"l6_sentence_{i+1}.wav"
        chunk.export(out_name, format="wav")
        print(f"Exported {out_name}: {start} to {end}")

if __name__ == "__main__":
    split_l6_v2("lesson_6_v2.wav")
