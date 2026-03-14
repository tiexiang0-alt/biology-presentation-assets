
from pydub import AudioSegment

def split_tight(file_path):
    audio = AudioSegment.from_wav(file_path)
    
    # Tightening the boundaries to avoid any bleed-over
    # S1 ends at 3390ms. We'll cut it at 3600ms.
    # S2 starts at 4029ms.
    # S2 ends at 7625ms. We'll cut it at 7800ms.
    # S3 starts at 8102ms.
    # S3 ends at 10761ms. We'll cut it at 11000ms.
    # S4 starts at 11230ms.
    # S4 ends at 16326ms. We'll cut it at 16500ms.
    # S5 starts at 16690ms.
    
    boundaries = [
        (0, 3600),     # S1: 佐藤さん、お疲れ様でした。これからまっすぐ帰りますか。
        (3900, 7850),  # S2: お疲れ様でした。はい、アパートまで歩いて帰ります。
        (8000, 11000), # S3: 歩いてですか。それは大変ですね。
        (11150, 16400),# S4: ええ。たしか、李さんは明日フランス人の友達と一緒に箱根へ行きますね。
        (16600, 20490) # S5: はい、新宿から電車で行きます。じゃあ、お先に失礼します。
    ]
    
    for i, (start, end) in enumerate(boundaries):
        chunk = audio[start:end]
        # Clean up silence
        trimmed = chunk.strip_silence(silence_thresh=-40, padding=50)
        out_name = f"d2_sentence_{i+1}.wav"
        trimmed.export(out_name, format="wav")
        print(f"Exported {out_name}: {start}ms - {end}ms (size: {len(trimmed)}ms)")

if __name__ == "__main__":
    split_tight("dialogue_2.wav")
