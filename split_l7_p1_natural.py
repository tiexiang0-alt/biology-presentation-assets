
from pydub import AudioSegment

def split_l7_p1_natural(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise start and end times for each sentence, 
    # capturing the natural flow and internal pauses.
    # We take consecutive ranges from the original audio to avoid "mechanical" silences.
    
    # S1: 李さんは 毎朝、 コーヒーを 飲みます。
    # S2: 私は、パンと 卵を 食べます。
    # S3: 王さんは、お粥を、 食べます。
    # S4: 昼、食堂で、親子丼を 食べます。
    # S5: 夜、日本のお茶を 飲みます。
    # S6: 茶道は、「一期一会」の、心です。
    
    boundaries = [
        (0, 2450),      # S1: Ends naturally after 'nomimasu'
        (3200, 7350),   # S2: Starts at 'watashi wa', ends after 'tabemasu'
        (7700, 9400),   # S3: Starts at 'wang san wa', ends after 'tabemasu'
        (10500, 13350), # S4: Starts at 'hiru', ends after 'tabemasu'
        (14200, 16400), # S5: Starts at 'yoru', ends after 'nomimasu'
        (17600, 21000)  # S6: Starts at 'sado wa', ends at the very end
    ]
    
    for i, (start, end) in enumerate(boundaries):
        # Extract the segment as is (preserving natural internal silence)
        segment = audio[start:end]
        
        # Apply a very subtle fade in/out (50ms) to prevent clicks, 
        # but keep natural ambient room tone.
        final = segment.fade_in(50).fade_out(50)
        
        out_name = f"l7_p1_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms to {end}ms (Natural Flow)")

if __name__ == "__main__":
    split_l7_p1_natural("lesson_7_part_1.wav")
