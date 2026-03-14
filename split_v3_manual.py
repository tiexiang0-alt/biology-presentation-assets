
from pydub import AudioSegment

def final_split_with_groups(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Precise boundaries based on segment analysis
    # S1 Segments 0,1: ends at 3390. Next starts at 4029. Split at 3700.
    # S2 Segments 2,3,4: ends at 7625. Next starts at 8102. Split at 7850.
    # S3 Segments 5,6: ends at 10761. Next starts at 11230. Split at 11000.
    # S4 Segments 7,8,9: ends at 16326. Next starts at 16690. Split at 16500.
    # S5 Segments 10,11,12: ends at 20491.
    
    delimiters = [3700, 7850, 11000, 16500]
    
    # Create start/end pairs
    points = [0] + delimiters + [len(audio)]
    
    for i in range(5):
        start = points[i]
        end = points[i+1]
        chunk = audio[start:end]
        
        # Strip exact silence to keep it tight
        # Using -40dB threshold
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        
        out_name = f"d2_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms - {end}ms")

if __name__ == "__main__":
    final_split_with_groups("dialogue_2.wav")
