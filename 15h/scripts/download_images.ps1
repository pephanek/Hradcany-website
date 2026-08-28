# Stahne obrazky clanku z hradcany-stamps.com (Webnode CDN) do 15h/assets/img/
# Spustte v PowerShellu:  powershell -ExecutionPolicy Bypass -File download_images.ps1
$root = Split-Path -Parent $PSScriptRoot
$dst  = Join-Path $root "assets\img"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$lines = Get-Content (Join-Path $PSScriptRoot "manifest.txt")
$i=0
foreach ($line in $lines) {
  $parts = $line -split "`t"
  if ($parts.Count -lt 2) { continue }
  $url = $parts[0]; $file = Join-Path $dst $parts[1]
  $i++
  if (Test-Path $file) { Write-Host "[$i] skip  $($parts[1])"; continue }
  try {
    Invoke-WebRequest -Uri $url -OutFile $file -UseBasicParsing
    Write-Host "[$i] OK    $($parts[1])"
  } catch { Write-Warning "[$i] CHYBA $url : $_" }
  Start-Sleep -Milliseconds 150
}
Write-Host "Hotovo. Obrazky jsou v $dst"
