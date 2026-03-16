
from pydub import AudioSegment

def split_l7_p1_refined(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # 12 segments grouped into 6 sentences
    # Segs: 0&1, 2&3, 4&5, 6&7, 8&9, 10&11
    # We split at the large silence gaps detected previously.
    
    # Midpoints of the large silences (>1s)
    # 0-3.8 (S1)
    # 4.1-7.3 (S2)
    # 7.7-9.3 (S3) -- wait, the gap after 9.3 is 1.3s
    # 10.6-13.2 (S4) -- gap after 13.2 is 1.1s
    # 14.3-16.3 (S5) -- gap after 16.3 is 1.5s
    # 17.7-20.8 (S6)
    
    # Let's use precise segments and merge them with a slight gap.
    segs = [
        (0, 2377), (3260, 3798),      # S1
        (4155, 5546), (6629, 7253),    # S2
        (7748, 8432), (8865, 9308),    # S3
        (10610, 10895), (11261, 13224),# S4
        (14326, 14577), (14929, 16250),# S5
        (17716, 18392), (18878, 20789) # S6
    ]
    
    for i in range(6):
        part1 = audio[segs[i*2][0]:segs[i*2][1]]
        part2 = audio[segs[i*2+1][0]:segs[i*2+1][1]]
        
        # Merge with a small natural silence (300ms) to preserve rhythm
        combined = part1 + AudioSegment.silent(duration=300) + part2
        
        # Add padding at both ends
        final = AudioSegment.silent(duration=100) + combined + AudioSegment.silent(duration=100)
        
        out_name = f"l7_p1_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: Merged Seg {i*2} and {i*2+1}")

if __name__ == "__main__":
    split_l7_p1_refined("lesson_7_part_1.wav")
