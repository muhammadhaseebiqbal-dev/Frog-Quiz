# Simple Video Compression Status Check
Write-Host "=============== VIDEO COMPRESSION STATUS ===============" -ForegroundColor Cyan
Write-Host ""

$videos = @("CF", "CSFT", "ESBF", "GGF", "PBF", "PTF", "SBTF", "SMF")
$totalOriginal = 0
$totalCompressed = 0
$compressedCount = 0

foreach ($video in $videos) {
    $original = ".\assets\$video`_resized.mp4"
    $compressed = ".\assets\$video`_mobile.mp4"
    
    if (Test-Path $original) {
        $origSize = [math]::Round((Get-Item $original).Length / 1MB, 2)
        $totalOriginal += $origSize
        
        if (Test-Path $compressed) {
            $compSize = [math]::Round((Get-Item $compressed).Length / 1MB, 2)
            $totalCompressed += $compSize
            $compressedCount++
            Write-Host "[OK]   $video - Original: $origSize MB, Compressed: $compSize MB" -ForegroundColor Green
        } else {
            Write-Host "[TODO] $video - $origSize MB - NEEDS COMPRESSION" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Videos compressed: $compressedCount / 8" -ForegroundColor White
Write-Host "  Original total: $totalOriginal MB" -ForegroundColor White
if ($totalCompressed -gt 0) {
    Write-Host "  Compressed total: $totalCompressed MB" -ForegroundColor White
    $saved = [math]::Round($totalOriginal - $totalCompressed, 2)
    $percent = [math]::Round(($saved / $totalOriginal) * 100, 1)
    Write-Host "  Space saved: $saved MB ($percent percent)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=============== COMPRESSION OPTIONS ===============" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1: HandBrake (Easiest, GUI)" -ForegroundColor Green
Write-Host "  Download: https://handbrake.fr/downloads.php"
Write-Host "  Preset: Fast 480p30"
Write-Host "  Save each as: [name]_mobile.mp4"
Write-Host ""
Write-Host "Option 2: Online (No install)" -ForegroundColor Green
Write-Host "  Visit: https://www.freeconvert.com/video-compressor"
Write-Host "  Target: 1-2MB per video"
Write-Host ""
Write-Host "Option 3: Install FFmpeg (then run compress_with_ffmpeg.ps1)" -ForegroundColor Green
Write-Host "  Run as Admin: winget install Gyan.FFmpeg"
Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
