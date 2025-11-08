# FFmpeg Auto-Compression Script
# Run this AFTER installing FFmpeg (winget install Gyan.FFmpeg)

Write-Host "=============== FFMPEG AUTO-COMPRESSION ===============" -ForegroundColor Cyan
Write-Host ""

# Check FFmpeg
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "FFmpeg found: $ffmpegVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "ERROR: FFmpeg not found!" -ForegroundColor Red
    Write-Host "Install first: winget install Gyan.FFmpeg" -ForegroundColor Yellow
    Write-Host "Then restart PowerShell and run this script again." -ForegroundColor Yellow
    exit 1
}

$videos = @("CF", "CSFT", "ESBF", "GGF", "PBF", "PTF", "SBTF", "SMF")
$totalOriginal = 0
$totalCompressed = 0

foreach ($video in $videos) {
    $inputFile = ".\assets\$video`_resized.mp4"
    $outputFile = ".\assets\$video`_mobile.mp4"
    
    if (Test-Path $inputFile) {
        if (Test-Path $outputFile) {
            Write-Host "[SKIP] $video (already exists)" -ForegroundColor Yellow
        } else {
            $origSize = [math]::Round((Get-Item $inputFile).Length / 1MB, 2)
            Write-Host "[WORK] Compressing $video ($origSize MB)..." -ForegroundColor Cyan
            
            # FFmpeg compression command
            $ffmpegArgs = @(
                "-i", $inputFile,
                "-c:v", "libx264",
                "-preset", "slow",
                "-crf", "28",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                $outputFile,
                "-y"
            )
            
            $process = Start-Process -FilePath "ffmpeg" -ArgumentList $ffmpegArgs -NoNewWindow -Wait -PassThru
            
            if ($process.ExitCode -eq 0 -and (Test-Path $outputFile)) {
                $newSize = [math]::Round((Get-Item $outputFile).Length / 1MB, 2)
                $saved = [math]::Round($origSize - $newSize, 2)
                $percent = [math]::Round(($saved / $origSize) * 100, 1)
                Write-Host "[DONE] $video - $origSize MB -> $newSize MB (saved $saved MB, $percent percent)" -ForegroundColor Green
                $totalOriginal += $origSize
                $totalCompressed += $newSize
            } else {
                Write-Host "[FAIL] $video compression failed" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""
Write-Host "=============== COMPRESSION COMPLETE ===============" -ForegroundColor Green
if ($totalOriginal -gt 0) {
    $totalSaved = [math]::Round($totalOriginal - $totalCompressed, 2)
    $totalPercent = [math]::Round(($totalSaved / $totalOriginal) * 100, 1)
    Write-Host "Total: $totalOriginal MB -> $totalCompressed MB" -ForegroundColor White
    Write-Host "Saved: $totalSaved MB ($totalPercent percent reduction)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. git add assets/*_mobile.mp4"
Write-Host "  2. git commit -m 'Add compressed mobile videos for APK'"
Write-Host "  3. git push"
Write-Host "  4. Rebuild APK"
Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
