"""
Asset Compression Script
Compresses videos (reduces video size, keeps original audio quality) and images in the assets folder
"""
import os
import subprocess
from pathlib import Path
from PIL import Image
import shutil

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
        print("  Please install FFmpeg from: https://ffmpeg.org/download.html")
        return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg timeout")
        return False

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return file_path.stat().st_size / 1024 / 1024

def get_audio_info(video_path):
    """Get audio codec and bitrate information from video"""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name,bit_rate,sample_rate,channels',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 4:
                return {
                    'codec': lines[0],
                    'bitrate': lines[1],
                    'sample_rate': lines[2],
                    'channels': lines[3]
                }
        return None
    except Exception as e:
        print(f"Error getting audio info: {e}")
        return None

def compress_video_keep_audio(input_path, output_path, crf=28, preset='medium'):
    """
    Compress video while keeping original audio quality
    
    Args:
        input_path: Input video file
        output_path: Output video file
        crf: Constant Rate Factor (18-28 recommended, lower = better quality, 23 is default)
        preset: Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
    """
    try:
        print(f"\n{'='*60}")
        print(f"Compressing: {input_path.name}")
        print(f"{'='*60}")
        
        original_size = get_file_size_mb(input_path)
        print(f"Original size: {original_size:.2f} MB")
        
        # Get original audio info
        audio_info = get_audio_info(input_path)
        if audio_info:
            print(f"Audio codec: {audio_info['codec']}")
            print(f"Audio bitrate: {audio_info['bitrate']} bps")
        
        print(f"\nCompressing with CRF={crf}, preset={preset}")
        print("Video: H.264 compression")
        print("Audio: Copy original (no quality loss)")
        
        # Compress video but copy audio stream (keeps original quality)
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-c:v', 'libx264',      # Use H.264 video codec
            '-crf', str(crf),       # Constant Rate Factor for quality
            '-preset', preset,      # Encoding speed/compression efficiency
            '-c:a', 'copy',         # Copy audio stream without re-encoding
            '-movflags', '+faststart',  # Enable fast start for web playback
            '-y',                   # Overwrite output file
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            new_size = get_file_size_mb(output_path)
            savings = ((original_size - new_size) / original_size) * 100
            
            print(f"\n✓ Success!")
            print(f"  Original: {original_size:.2f} MB")
            print(f"  Compressed: {new_size:.2f} MB")
            print(f"  Saved: {savings:.1f}% ({original_size - new_size:.2f} MB)")
            return True
        else:
            print(f"\n✗ Error during compression:")
            print(result.stderr[-500:])  # Show last 500 chars of error
            return False
            
    except subprocess.TimeoutExpired:
        print("\n✗ Timeout during compression (video too large?)")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def compress_image(input_path, output_path, quality=85, max_dimension=1920):
    """
    Compress and optimize image
    
    Args:
        input_path: Input image file
        output_path: Output image file
        quality: JPEG quality (1-100, default 85)
        max_dimension: Maximum width or height in pixels (default 1920)
    """
    try:
        print(f"\n{'='*60}")
        print(f"Compressing: {input_path.name}")
        print(f"{'='*60}")
        
        original_size = input_path.stat().st_size / 1024  # KB
        print(f"Original size: {original_size:.2f} KB")
        
        img = Image.open(input_path)
        print(f"Original dimensions: {img.width}x{img.height}")
        print(f"Original mode: {img.mode}")
        
        # Resize if too large (maintain aspect ratio)
        if img.width > max_dimension or img.height > max_dimension:
            if img.width > img.height:
                new_width = max_dimension
                new_height = int(img.height * (max_dimension / img.width))
            else:
                new_height = max_dimension
                new_width = int(img.width * (max_dimension / img.height))
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"Resized to: {img.width}x{img.height}")
        
        # Convert to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if 'A' in img.mode:
                bg.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                bg.paste(img)
            img = bg
            print(f"Converted to RGB")
        
        # Determine output format
        output_format = 'JPEG'
        if output_path.suffix.lower() == '.png':
            output_format = 'PNG'
            # For PNG, use optimize and set compression level
            img.save(output_path, output_format, optimize=True, compress_level=9)
        else:
            # For JPEG
            img.save(output_path, output_format, quality=quality, optimize=True, progressive=True)
        
        new_size = output_path.stat().st_size / 1024  # KB
        savings = ((original_size - new_size) / original_size) * 100
        
        print(f"\n✓ Success!")
        print(f"  Original: {original_size:.2f} KB")
        print(f"  Compressed: {new_size:.2f} KB")
        print(f"  Saved: {savings:.1f}% ({original_size - new_size:.2f} KB)")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def backup_folder(source_dir):
    """Create a backup of the assets folder"""
    backup_dir = source_dir.parent / f"{source_dir.name}_backup"
    
    if backup_dir.exists():
        print(f"\n⚠ Backup folder already exists: {backup_dir}")
        response = input("Overwrite existing backup? (y/n): ").strip().lower()
        if response != 'y':
            print("Backup skipped")
            return False
        shutil.rmtree(backup_dir)
    
    print(f"\nCreating backup: {backup_dir}")
    shutil.copytree(source_dir, backup_dir)
    print("✓ Backup created successfully")
    return True

def compress_all_videos(assets_dir, crf=28, preset='medium', backup=True):
    """Compress all video files in assets folder"""
    print("\n" + "="*60)
    print("VIDEO COMPRESSION (RETAIN ORIGINAL AUDIO)")
    print("="*60)
    
    # Find all video files
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(assets_dir.glob(ext))
    
    if not video_files:
        print("\n✗ No video files found")
        return
    
    print(f"\nFound {len(video_files)} video file(s)")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {video.name} ({get_file_size_mb(video):.2f} MB)")
    
    # Create backup if requested
    if backup:
        print("\n" + "-"*60)
        if not backup_folder(assets_dir):
            response = input("\nContinue without backup? (y/n): ").strip().lower()
            if response != 'y':
                print("Compression cancelled")
                return
    
    # Compress each video
    success_count = 0
    for video in video_files:
        # Create temporary output file
        temp_output = video.parent / f"{video.stem}_temp_compressed{video.suffix}"
        
        if compress_video_keep_audio(video, temp_output, crf=crf, preset=preset):
            # Replace original with compressed version
            video.unlink()
            temp_output.rename(video)
            success_count += 1
        else:
            # Clean up failed temp file
            if temp_output.exists():
                temp_output.unlink()
    
    print(f"\n{'='*60}")
    print(f"Compression complete: {success_count}/{len(video_files)} videos compressed")
    print("="*60)

def compress_all_images(assets_dir, quality=85, max_dimension=1920, backup=True):
    """Compress all image files in assets folder"""
    print("\n" + "="*60)
    print("IMAGE COMPRESSION")
    print("="*60)
    
    # Find all image files
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(assets_dir.glob(ext))
    
    if not image_files:
        print("\n✗ No image files found")
        return
    
    print(f"\nFound {len(image_files)} image file(s)")
    for i, img in enumerate(image_files, 1):
        size_kb = img.stat().st_size / 1024
        print(f"  {i}. {img.name} ({size_kb:.2f} KB)")
    
    # Create backup if requested
    if backup:
        print("\n" + "-"*60)
        if not backup_folder(assets_dir):
            response = input("\nContinue without backup? (y/n): ").strip().lower()
            if response != 'y':
                print("Compression cancelled")
                return
    
    # Compress each image
    success_count = 0
    for img_path in image_files:
        # Determine output path (keep original extension if PNG, convert to JPG otherwise)
        if img_path.suffix.lower() == '.png':
            temp_output = img_path.parent / f"{img_path.stem}_temp_compressed.png"
        else:
            temp_output = img_path.parent / f"{img_path.stem}_temp_compressed.jpg"
        
        if compress_image(img_path, temp_output, quality=quality, max_dimension=max_dimension):
            # Replace original with compressed version
            img_path.unlink()
            temp_output.rename(img_path)
            success_count += 1
        else:
            # Clean up failed temp file
            if temp_output.exists():
                temp_output.unlink()
    
    print(f"\n{'='*60}")
    print(f"Compression complete: {success_count}/{len(image_files)} images compressed")
    print("="*60)

def main():
    """Main function - Automatic compression with aggressive settings"""
    print("\n" + "="*60)
    print("AUTOMATIC ASSET COMPRESSION")
    print("Aggressive compression for smaller APK size")
    print("="*60)
    
    # Check for assets folder
    assets_dir = Path('assets')
    if not assets_dir.exists():
        print("\n✗ 'assets' folder not found in current directory")
        print(f"  Current directory: {Path.cwd()}")
        return
    
    print(f"\n✓ Assets folder found: {assets_dir.absolute()}")
    
    # Check FFmpeg
    has_ffmpeg = check_ffmpeg()
    if not has_ffmpeg:
        print("\n⚠ FFmpeg not found - skipping video compression")
        print("  Only images will be compressed")
    
    # Automatic configuration (aggressive compression)
    print("\n" + "-"*60)
    print("COMPRESSION SETTINGS (AUTOMATIC)")
    print("-"*60)
    
    # Aggressive settings for maximum compression
    crf = 30  # Higher CRF = more compression (28-32 is good for APK)
    preset = 'medium'  # Balance between speed and compression
    quality = 75  # Lower quality for smaller files (75-80 is good)
    max_dimension = 1080  # HD resolution (good for mobile)
    backup = True
    
    if has_ffmpeg:
        print(f"\n📹 Video Settings:")
        print(f"   CRF: {crf} (more compression)")
        print(f"   Preset: {preset}")
        print(f"   Audio: Copy original (no quality loss)")
    
    print(f"\n🖼️ Image Settings:")
    print(f"   Quality: {quality}%")
    print(f"   Max Dimension: {max_dimension}px")
    
    print(f"\n💾 Backup: Yes (original files will be saved)")
    
    print("\n" + "="*60)
    print("STARTING COMPRESSION...")
    print("="*60)
    
    # Process videos
    if has_ffmpeg:
        compress_all_videos(assets_dir, crf=crf, preset=preset, backup=backup)
        backup = False  # Don't backup again for images
    
    # Process images
    compress_all_images(assets_dir, quality=quality, max_dimension=max_dimension, backup=backup)
    
    print("\n" + "="*60)
    print("✅ ALL DONE!")
    print("="*60)
    print("\n✓ Asset compression complete")
    print(f"✓ Original files backed up to: assets_backup/")
    print("\n💡 Next steps:")
    print("   1. Check the compressed files")
    print("   2. Test the app to ensure quality is acceptable")
    print("   3. If satisfied, commit and push to trigger APK build")
    print("   4. If not satisfied, restore from backup and adjust settings")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

