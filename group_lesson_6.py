
from pydub import AudioSegment, silence

def group_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    # Use a longer silence threshold to find the 5 main sections
    # Trying 1500ms as the separator between major lesson points
    chunks = silence.split_on_silence(audio, min_silence_len=1200, silence_thresh=-40, keep_silence=200)
    
    print(f"Detected {len(chunks)} major chunks.")
    for i, chunk in enumerate(chunks):
        out_name = f"lesson_6_chunk_{i}.wav"
        chunk.export(out_name, format="wav")
        print(f"Chunk {i}: {len(chunk)}ms")

if __name__ == "__main__":
    group_audio("lesson_6.wav")
