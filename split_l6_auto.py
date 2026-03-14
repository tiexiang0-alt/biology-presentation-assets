
from pydub import AudioSegment, silence

def split_by_largest_gaps(file_path, num_parts=5):
    audio = AudioSegment.from_wav(file_path)
    # Detect all silence intervals
    min_silence = 300
    thresh = -40
    silence_intervals = silence.detect_silence(audio, min_silence_len=min_silence, silence_thresh=thresh)
    
    # Calculate durations of silences
    # silences are (start, end)
    gaps = []
    for i, (start, end) in enumerate(silence_intervals):
        # Ignore silence at the very start/end
        if start < 100 or end > len(audio) - 100:
            continue
        gaps.append({'start': start, 'end': end, 'duration': end - start})
    
    # Sort gaps by duration descending
    sorted_gaps = sorted(gaps, key=lambda x: x['duration'], reverse=True)
    
    # Pick top (num_parts - 1) gaps
    best_gaps = sorted_gaps[:num_parts-1]
    # Sort by time
    best_gaps = sorted(best_gaps, key=lambda x: x['start'])
    
    # Split points are the midpoints of these gaps
    split_points = [ (g['start'] + g['end']) // 2 for g in best_gaps ]
    
    points = [0] + split_points + [len(audio)]
    
    for i in range(num_parts):
        chunk = audio[points[i]:points[i+1]]
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=100)
        out_name = f"l6_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {points[i]}ms to {points[i+1]}ms")

if __name__ == "__main__":
    split_by_largest_gaps("lesson_6.wav")
