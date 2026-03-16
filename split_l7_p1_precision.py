
from pydub import AudioSegment

def split_l7_p1_final_calibration(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Recalibrated boundaries to strictly separate "Watashi wa" from "Wang-san wa" (osanwa)
    # S1: (0, 2800) -> Li-san wa...
    # S2: (3200, 6000) -> Watashi wa... Ends before Wang-san wa (which starts at ~6600)
    # S3: (6500, 9800) -> Wang-san wa... (osanwa)
    # S4: (10500, 13700) -> Hiru...
    # S5: (14200, 16800) -> Yoru...
    # S6: (17500, 21171) -> Sado wa...
    
    boundaries = [
        (0, 2800),      # S1
        (3200, 6000),   # S2: Cut before 6600 to remove Wang-san wa
        (6500, 9800),   # S3: Start of Wang-san wa (osanwa)
        (10500, 13700), # S4
        (14200, 17000), # S5
        (17500, 21171)  # S6
    ]
    
    for i, (start, end) in enumerate(boundaries):
        segment = audio[start:end]
        # Preserve natural rhythm and room tone
        final = segment.fade_in(50).fade_out(50)
        
        out_name = f"l7_p1_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms (Precision Calibration)")

if __name__ == "__main__":
    split_l7_p1_final_calibration("lesson_7_part_1.wav")
