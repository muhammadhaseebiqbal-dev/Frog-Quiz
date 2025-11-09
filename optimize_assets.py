"""
Asset Optimization Utility
Helps reduce video and image file sizes for better app performance
"""
import os
import subprocess
from pathlib import Path
from PIL import Image

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg found: {version}")
            return True
        else:
            print("✗ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        print("  Download from: https://ffmpeg.org/download.html")
        return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg timeout")
        return False

def get_video_info(video_path):
    """Get video file information"""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration,size,bit_rate',
            '-show_entries', 'stream=codec_name,width,height',
            '-of', 'default=noprint_wrappers=1',
            str(video_path)
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"\nVideo Info: {video_path.name}")
            print(result.stdout)
        else:
            print(f"Error getting info for {video_path.name}")
    except Exception as e:
        print(f"Error: {e}")

def compress_video_audio(input_path, output_path, audio_bitrate='32k'):
    """
    Compress video audio track (since spectrograms don't need high quality audio)
    
    Args:
        input_path: Input video file
        output_path: Output video file
        audio_bitrate: Audio bitrate (default 32k for voice, can go lower)
    """
    try:
        print(f"\nCompressing audio: {input_path.name}")
        print(f"Audio bitrate: {audio_bitrate}")
        
        # Compress audio while keeping video unchanged
        result = subprocess.run([
            'ffmpeg', '-i', str(input_path),
            '-c:v', 'copy',  # Copy video stream (no re-encoding)
            '-c:a', 'aac',   # Use AAC audio codec
            '-b:a', audio_bitrate,  # Set audio bitrate
            '-y',  # Overwrite output file
            str(output_path)
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            original_size = input_path.stat().st_size / 1024 / 1024  # MB
            new_size = output_path.stat().st_size / 1024 / 1024  # MB
            savings = ((original_size - new_size) / original_size) * 100
            
            print(f"✓ Success!")
            print(f"  Original: {original_size:.2f} MB")
            print(f"  Compressed: {new_size:.2f} MB")
            print(f"  Saved: {savings:.1f}%")
            return True
        else:
            print(f"✗ Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Timeout during compression")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def compress_image(input_path, output_path, quality=85, max_width=1920):
    """
    Compress image while maintaining aspect ratio
    
    Args:
        input_path: Input image file
        output_path: Output image file
        quality: JPEG quality (1-100, default 85)
        max_width: Maximum width in pixels (default 1920)
    """
    try:
        print(f"\nCompressing image: {input_path.name}")
        
        img = Image.open(input_path)
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized to: {max_width}x{new_height}")
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        
        # Save with compression
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        original_size = input_path.stat().st_size / 1024  # KB
        new_size = output_path.stat().st_size / 1024  # KB
        savings = ((original_size - new_size) / original_size) * 100
        
        print(f"✓ Success!")
        print(f"  Original: {original_size:.2f} KB")
        print(f"  Compressed: {new_size:.2f} KB")
        print(f"  Saved: {savings:.1f}%")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def process_assets():
    """Process all assets in the assets folder"""
    assets_dir = Path('assets')
    
    if not assets_dir.exists():
        print("✗ assets/ directory not found")
        return
    
    # Check FFmpeg
    has_ffmpeg = check_ffmpeg()
    
    # Process videos
    if has_ffmpeg:
        print("\n" + "="*50)
        print("VIDEO AUDIO COMPRESSION")
        print("="*50)
        
        video_files = list(assets_dir.glob('*_resized.mp4'))
        if not video_files:
            print("No *_resized.mp4 videos found")
        
        for video in video_files:
            # Create optimized version
            output = video.parent / f"{video.stem}_optimized.mp4"
            
            # Show current info
            get_video_info(video)
            
            # Compress audio to 32k (good enough for frog calls)
            compress_video_audio(video, output, audio_bitrate='32k')
    
    # Process images
    print("\n" + "="*50)
    print("IMAGE COMPRESSION")
    print("="*50)
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg']
    image_files = []
    for ext in image_extensions:
        image_files.extend(assets_dir.glob(ext))
    
    if not image_files:
        print("No images found")
    
    for img_path in image_files:
        # Skip already optimized images
        if '_optimized' in img_path.stem:
            continue
            
        # Create optimized version
        output = img_path.parent / f"{img_path.stem}_optimized.jpg"
        
        # Compress image
        compress_image(img_path, output, quality=85, max_width=1920)

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*60)
    print("FROG QUIZ - ASSET OPTIMIZATION UTILITY")
    print("="*60)
    print("\nOptions:")
    print("1. Check FFmpeg installation")
    print("2. Process all assets (videos + images)")
    print("3. Compress video audio only")
    print("4. Compress images only")
    print("5. Show video information")
    print("0. Exit")
    print()

if __name__ == '__main__':
    while True:
        show_menu()
        choice = input("Choose an option (0-5): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            check_ffmpeg()
        elif choice == '2':
            process_assets()
        elif choice == '3':
            if check_ffmpeg():
                assets_dir = Path('assets')
                videos = list(assets_dir.glob('*_resized.mp4'))
                for i, video in enumerate(videos, 1):
                    print(f"{i}. {video.name}")
                
                if videos:
                    idx = input(f"\nChoose video (1-{len(videos)}) or 'all': ").strip()
                    if idx.lower() == 'all':
                        for video in videos:
                            output = video.parent / f"{video.stem}_optimized.mp4"
                            compress_video_audio(video, output)
                    elif idx.isdigit() and 1 <= int(idx) <= len(videos):
                        video = videos[int(idx) - 1]
                        output = video.parent / f"{video.stem}_optimized.mp4"
                        compress_video_audio(video, output)
        elif choice == '4':
            assets_dir = Path('assets')
            images = [f for f in assets_dir.glob('*') 
                     if f.suffix.lower() in ['.png', '.jpg', '.jpeg'] 
                     and '_optimized' not in f.stem]
            
            for i, img in enumerate(images, 1):
                print(f"{i}. {img.name}")
            
            if images:
                idx = input(f"\nChoose image (1-{len(images)}) or 'all': ").strip()
                if idx.lower() == 'all':
                    for img in images:
                        output = img.parent / f"{img.stem}_optimized.jpg"
                        compress_image(img, output)
                elif idx.isdigit() and 1 <= int(idx) <= len(images):
                    img = images[int(idx) - 1]
                    output = img.parent / f"{img.stem}_optimized.jpg"
                    compress_image(img, output)
        elif choice == '5':
            if check_ffmpeg():
                assets_dir = Path('assets')
                videos = list(assets_dir.glob('*.mp4'))
                for video in videos:
                    get_video_info(video)
        else:
            print("Invalid option")
        
        input("\nPress Enter to continue...")
