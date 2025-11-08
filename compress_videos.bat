@echo off
REM Video Compression Script for Frog Quiz
REM Reduces video size by 80%% while keeping audio quality
REM Requires FFmpeg: https://ffmpeg.org/download.html

echo Compressing frog videos for APK...
echo.

cd assets

for %%f in (*_resized.mp4) do (
    echo Processing %%f...
    ffmpeg -i "%%f" -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart "%%~nf_compressed.mp4"
    echo %%f compressed!
    echo.
)

echo.
echo Done! Compressed videos are ready.
echo Original videos kept as backup.
pause
