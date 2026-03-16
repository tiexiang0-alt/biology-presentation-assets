
from pydub import AudioSegment

def scan_volume(file_path):
    audio = AudioSegment.from_wav(file_path)
    for i in range(5000, 7500, 100):
        chunk = audio[i:i+100]
        print(f"Time {i}ms: RMS {chunk.rms}")

if __name__ == "__main__":
    scan_volume("lesson_7_part_1.wav")
