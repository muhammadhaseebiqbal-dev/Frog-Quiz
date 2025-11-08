"""
Simple video compressor using HandBrake CLI or online tools
Since FFmpeg setup is complex, this creates a guide
"""

print("""
==================== VIDEO COMPRESSION GUIDE ====================

Option 1: HandBrake (Easiest - GUI Tool)
----------------------------------------
1. Download HandBrake: https://handbrake.fr/downloads.php
2. Open HandBrake
3. Load video file from assets/
4. Preset: "Fast 480p30" or "Fast 720p30"
5. Audio: Keep AAC 128kbps
6. Save as: [name]_mobile.mp4
7. Repeat for all 8 videos

Expected: 70-80% size reduction (65MB → ~15MB total)

Option 2: Online (Quick but requires upload)
-------------------------------------------
1. Visit: https://www.freeconvert.com/video-compressor
2. Upload each video
3. Target size: 1-2MB per video
4. Download as [name]_mobile.mp4

Option 3: FFmpeg Command Line (If installed)
--------------------------------------------
Run in PowerShell from assets folder:

For each video, run:
ffmpeg -i CF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart CF_mobile.mp4
ffmpeg -i CSFT_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart CSFT_mobile.mp4
ffmpeg -i ESBF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart ESBF_mobile.mp4
ffmpeg -i GGF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart GGF_mobile.mp4
ffmpeg -i PBF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart PBF_mobile.mp4
ffmpeg -i PTF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart PTF_mobile.mp4
ffmpeg -i SBTF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart SBTF_mobile.mp4
ffmpeg -i SMF_resized.mp4 -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart SMF_mobile.mp4

==================== AFTER COMPRESSION ====================

1. Place all *_mobile.mp4 files in assets/ folder
2. Run: git add assets/*_mobile.mp4
3. Run: git commit -m "Add compressed mobile videos for APK"
4. Run: git push

Then rebuild APK - it will use _mobile.mp4 (small) instead of _resized.mp4 (large)

================================================================
""")
