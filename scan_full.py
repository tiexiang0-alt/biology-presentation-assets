
from pydub import AudioSegment

def scan_full(file_path):
    audio = AudioSegment.from_wav(file_path)
    for i in range(0, 21000, 500):
        chunk = audio[i:i+500]
        print(f"{i}ms: RMS {chunk.rms}")

if __name__ == "__main__":
    scan_full("lesson_7_part_1.wav")
