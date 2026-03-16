
from pydub import AudioSegment

def split_l7_p1_final_fix(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Intervals from find_all_ranges.py
    ints = [
        (0, 2377),      # 0
        (3260, 3798),   # 1
        (4155, 5546),   # 2
        (6629, 7253),   # 3
        (7748, 8432),   # 4
        (8865, 9308),   # 5
        (10610, 10895), # 6
        (11261, 13224), # 7
        (14326, 14577), # 8
        (14929, 16250), # 9
        (17716, 18392), # 10
        (18878, 20789)  # 11
    ]
    
    # Grouping logic:
    # S1: Int 0 (Li-san)
    # S2: Int 1 + 2 (Watashi wa + Pan...)
    # S3: Int 3 + 4 + 5 (Wang-san + Okayu + Tabemasu)
    # S4: Int 6 + 7 (Hiru + Shokudo...)
    # S5: Int 8 + 9 (Yoru + Ocha...)
    # S6: Int 10 + 11 (Sado + Ichigo...)
    
    grouping = [
        [0],          # S1
        [1, 2],       # S2
        [3, 4, 5],    # S3
        [6, 7],       # S4
        [8, 9],       # S5
        [10, 11]      # S6
    ]
    
    for i, indices in enumerate(grouping):
        combined = AudioSegment.silent(duration=0)
        for idx in indices:
            part = audio[ints[idx][0]:ints[idx][1]]
            if len(combined) > 0:
                combined += AudioSegment.silent(duration=300) # Natural pause between segments
            combined += part
        
        # Padding
        final = AudioSegment.silent(duration=100) + combined + AudioSegment.silent(duration=100)
        
        out_name = f"l7_p1_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: Merged {indices}")

if __name__ == "__main__":
    split_l7_p1_final_fix("lesson_7_part_1.wav")
