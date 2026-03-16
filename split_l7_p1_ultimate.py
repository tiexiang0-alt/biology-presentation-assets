
from pydub import AudioSegment

def split_l7_p1_final_v3(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Strictly re-grouping based on the 13 detected phrases:
    # Ints: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ints = [
        (263, 2391),   # 0: S1
        (3259, 3801),  # 1: S2 start (Watashi wa)
        (4154, 5560),  # 2: S2 end (Pan to... tabemasu)
        (6629, 7256),  # 3: S3 start (Ou-san wa)
        (7748, 8433),  # 4: S3 mid (Okayu o)
        (8855, 9321),  # 5: S3 end (Tabemasu)
        (10600, 10896),# 6: S4 start (Hiru)
        (11255, 13237),# 7: S4 end (Shokudo de...)
        (14326, 14578),# 8: S5 start (Yoru)
        (14929, 16268),# 9: S5 end (Ocha o...)
        (17708, 18397),# 10: S6 start (Sado wa)
        (18877, 20804) # 11+12: S6 end (Ichigo ichie...)
    ]
    
    # Map sentences to intervals
    mapping = [
        [0],          # S1
        [1, 2],       # S2
        [3, 4, 5],    # S3
        [6, 7],       # S4
        [8, 9],       # S5
        [10, 11]      # S6
    ]
    
    for i, indices in enumerate(mapping):
        combined = AudioSegment.silent(duration=0)
        for idx in indices:
            start, end = ints[idx]
            # Add a small buffer around each speech chunk
            chunk = audio[max(0, start-150):min(len(audio), end+150)]
            if len(combined) > 0:
                # Use a very short, natural interval between phrases in a sentence
                combined += AudioSegment.silent(duration=200)
            combined += chunk
        
        # Soft fades for naturalness
        final = combined.fade_in(50).fade_out(50)
        
        out_name = f"l7_p1_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: Corrected Grouping {indices}")

if __name__ == "__main__":
    split_l7_p1_final_v3("lesson_7_part_1.wav")
