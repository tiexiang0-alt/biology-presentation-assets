
from pydub import AudioSegment

def split_l7_p2(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise groupings based on phrase analysis
    mapping = [
        (259, 4100),    # S1: 朝、私は...
        (4900, 8500),   # S2: そして、机で...
        (9250, 12050),  # S3: 午后、友達と...
        (12800, 16300), # S4: 夕方、公园で...
        (17000, 20500)  # S5: 野球は 日本で...
    ]
    
    for i, (start, end) in enumerate(mapping):
        # Extract and add a bit of room tone buffer
        segment = audio[max(0, start-100):min(len(audio), end+100)]
        # Fades to prevent clicks
        final = segment.fade_in(50).fade_out(50)
        
        out_name = f"l7_p2_sentence_{i+1}.wav"
        final.export(out_name, format="wav")
        print(f"Exported {out_name}: {start} to {end}")

if __name__ == "__main__":
    split_l7_p2("lesson_7_part_2.wav")
