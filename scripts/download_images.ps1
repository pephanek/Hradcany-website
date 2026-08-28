# Stáhne všechny obrázky do assets\images\. Spusťte v PowerShellu z kořene projektu:
#   powershell -ExecutionPolicy Bypass -File scripts\download_images.ps1
$base = "https://900cfd8a63.clvaw-cdnwnd.com/9c4605a2643780500ef1c2ac87facbb9"
$dest = Join-Path (Split-Path $PSScriptRoot -Parent) "assets\images"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$ok = 0; $fail = 0
Get-Content (Join-Path $PSScriptRoot "manifest.txt") | ForEach-Object {
  if ($_ -match "\|") {
    $parts = $_ -split "\|", 2
    $url = "$base/$($parts[0])"
    $out = Join-Path $dest $parts[1]
    try { Invoke-WebRequest -Uri $url -OutFile $out -TimeoutSec 30; $ok++; Write-Host "OK   $($parts[1])" }
    catch { $fail++; Write-Host "FAIL $($parts[1])" -ForegroundColor Red }
  }
}
Write-Host "`nHotovo: $ok stazeno, $fail chyb."
