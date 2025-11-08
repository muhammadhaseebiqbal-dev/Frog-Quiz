"""
Video Compression Script for Frog Quiz APK
Reduces video size by 70-80% while maintaining audio quality
Uses moviepy (pure Python, no FFmpeg needed)
"""
import os
from pathlib import Path

print("Installing moviepy if needed...")
os.system("pip install moviepy")

from moviepy.editor import VideoFileClip

def compress_video(input_path, output_path, target_bitrate="500k"):
    """Compress video to reduce file size for APK"""
    print(f"\nCompressing: {input_path.name}")
    print(f"Original size: {input_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    clip = VideoFileClip(str(input_path))
    
    # Write compressed version
    clip.write_videofile(
        str(output_path),
        bitrate=target_bitrate,
        audio_bitrate="128k",
        codec="libx264",
        preset="slow",
        threads=4,
        ffmpeg_params=["-crf", "28"]
    )
    
    clip.close()
    
    print(f"Compressed size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    reduction = (1 - output_path.stat().st_size / input_path.stat().st_size) * 100
    print(f"Size reduction: {reduction:.1f}%")

def main():
    assets_dir = Path(__file__).parent / "assets"
    
    videos = [
        "CF_resized.mp4",
        "CSFT_resized.mp4", 
        "ESBF_resized.mp4",
        "GGF_resized.mp4",
        "PBF_resized.mp4",
        "PTF_resized.mp4",
        "SBTF_resized.mp4",
        "SMF_resized.mp4"
    ]
    
    total_original = 0
    total_compressed = 0
    
    for video_name in videos:
        input_path = assets_dir / video_name
        if not input_path.exists():
            print(f"⚠️  Skipping {video_name} - not found")
            continue
        
        # Output as _mobile.mp4
        output_name = video_name.replace("_resized.mp4", "_mobile.mp4")
        output_path = assets_dir / output_name
        
        try:
            compress_video(input_path, output_path)
            total_original += input_path.stat().st_size
            total_compressed += output_path.stat().st_size
        except Exception as e:
            print(f"❌ Error compressing {video_name}: {e}")
    
    print("\n" + "="*50)
    print(f"Total original: {total_original / 1024 / 1024:.2f} MB")
    print(f"Total compressed: {total_compressed / 1024 / 1024:.2f} MB")
    print(f"Total saved: {(total_original - total_compressed) / 1024 / 1024:.2f} MB")
    print(f"Reduction: {(1 - total_compressed / total_original) * 100:.1f}%")
    print("="*50)
    print("\n✅ Done! Use *_mobile.mp4 files for APK build")

if __name__ == "__main__":
    main()
