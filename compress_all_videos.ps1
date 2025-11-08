# PowerShell Script to Compress Videos for APK
# This script will guide you through compressing videos

Write-Host "==================== VIDEO COMPRESSION OPTIONS ====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "CURRENT STATUS:" -ForegroundColor Yellow
$assetsPath = ".\assets"
$videos = @("CF", "CSFT", "ESBF", "GGF", "PBF", "PTF", "SBTF", "SMF")

foreach ($video in $videos) {
    $originalFile = Join-Path $assetsPath "$video`_resized.mp4"
    $compressedFile = Join-Path $assetsPath "$video`_mobile.mp4"
    
    if (Test-Path $originalFile) {
        $size = [math]::Round((Get-Item $originalFile).Length / 1MB, 2)
        $status = if (Test-Path $compressedFile) { "[OK] COMPRESSED" } else { "[!!] NEEDS COMPRESSION" }
        $color = if (Test-Path $compressedFile) { "Green" } else { "Red" }
        Write-Host "$status - $video - $size MB" -ForegroundColor $color
    }
}

Write-Host ""
Write-Host "==================== RECOMMENDED APPROACH ====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: HandBrake (EASIEST - Recommended)" -ForegroundColor Green
Write-Host "  1. Download: https://handbrake.fr/downloads.php" -ForegroundColor White
Write-Host "  2. Install and open HandBrake" -ForegroundColor White
Write-Host "  3. Click File -> Open Source -> Select video from assets folder" -ForegroundColor White
Write-Host "  4. Preset: Select Fast 480p30 (or Fast 720p30 for better quality)" -ForegroundColor White
Write-Host "  5. Browse destination: Save as [name]_mobile.mp4 in assets folder" -ForegroundColor White
Write-Host "  6. Click Start Encode" -ForegroundColor White
Write-Host "  7. Repeat for all 8 videos" -ForegroundColor White
Write-Host ""

Write-Host "Option 2: Online Converter (NO INSTALL NEEDED)" -ForegroundColor Green
Write-Host "  1. Visit: https://www.freeconvert.com/video-compressor" -ForegroundColor White
Write-Host "  2. Upload video file" -ForegroundColor White
Write-Host "  3. Target size: 1-2MB per video (70-80 percent compression)" -ForegroundColor White
Write-Host "  4. Download compressed file" -ForegroundColor White
Write-Host "  5. Rename to [name]_mobile.mp4 and save to assets folder" -ForegroundColor White
Write-Host "  6. Repeat for all 8 videos" -ForegroundColor White
Write-Host ""

Write-Host "Option 3: Install FFmpeg (FASTEST - For tech users)" -ForegroundColor Green
Write-Host "  1. Install via Chocolatey: choco install ffmpeg" -ForegroundColor White
Write-Host "     (or download from: https://www.gyan.dev/ffmpeg/builds/)" -ForegroundColor White
Write-Host "  2. After install, run this script again - it will auto-compress all videos" -ForegroundColor White
Write-Host ""

Write-Host "==================== AUTO-DETECT FFMPEG ====================" -ForegroundColor Cyan
Write-Host ""

# Check if FFmpeg is available
$ffmpegAvailable = $false
try {
    $null = ffmpeg -version 2>&1
    $ffmpegAvailable = $true
} catch {
    $ffmpegAvailable = $false
}

if ($ffmpegAvailable) {
    Write-Host "FFmpeg detected! Starting automatic compression..." -ForegroundColor Green
    Write-Host ""
    
    foreach ($video in $videos) {
        $inputFile = Join-Path $assetsPath "$video`_resized.mp4"
        $outputFile = Join-Path $assetsPath "$video`_mobile.mp4"
        
        if (Test-Path $inputFile) {
            if (Test-Path $outputFile) {
                Write-Host "⊘ Skipping $video (already compressed)" -ForegroundColor Yellow
            } else {
                Write-Host "⚙ Compressing $video..." -ForegroundColor Cyan
                $originalSize = [math]::Round((Get-Item $inputFile).Length / 1MB, 2)
                
                ffmpeg -i $inputFile -c:v libx264 -preset slow -crf 28 -c:a aac -b:a 128k -movflags +faststart $outputFile -y 2>&1 | Out-Null
                
                if (Test-Path $outputFile) {
                    $newSize = [math]::Round((Get-Item $outputFile).Length / 1MB, 2)
                    $reduction = [math]::Round((1 - $newSize/$originalSize) * 100, 1)
                    Write-Host "  ✓ $video compressed: $originalSize MB → $newSize MB ($reduction% reduction)" -ForegroundColor Green
                } else {
                    Write-Host "  ✗ Failed to compress $video" -ForegroundColor Red
                }
            }
        }
    }
    
    Write-Host ""
    Write-Host "==================== COMPRESSION COMPLETE ====================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. git add assets/*_mobile.mp4" -ForegroundColor White
    Write-Host "  2. git commit -m 'Add compressed mobile videos for APK'" -ForegroundColor White
    Write-Host "  3. git push" -ForegroundColor White
    Write-Host "  4. Rebuild APK via buildozer or GitHub Actions" -ForegroundColor White
    
} else {
    Write-Host "FFmpeg NOT detected." -ForegroundColor Red
    Write-Host ""
    Write-Host "QUICK INSTALL OPTIONS:" -ForegroundColor Yellow
    Write-Host "  A. Chocolatey (run as Admin): choco install ffmpeg" -ForegroundColor White
    Write-Host "  B. Winget (run as Admin):     winget install Gyan.FFmpeg" -ForegroundColor White
    Write-Host "  C. Manual download:          https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor White
    Write-Host ""
    Write-Host "After installing FFmpeg, run this script again for automatic compression." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "OR use HandBrake/Online converter (no install needed) - see options above." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
