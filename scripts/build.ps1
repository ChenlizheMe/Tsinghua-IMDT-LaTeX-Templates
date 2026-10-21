param(
    [ValidateSet('All', 'Report', 'Form')]
    [string]$Target = 'All',
    [switch]$Clean
)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$buildRoot = Join-Path $projectRoot 'build'
if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw 'Install TeX Live or MiKTeX with XeLaTeX, BibTeX and latexmk first.'
}
New-Item -ItemType Directory -Force -Path $buildRoot,
    (Join-Path $buildRoot 'chapters'), (Join-Path $buildRoot 'appendices') | Out-Null
$targets = switch ($Target) {
    'Report' { 'imdt-proposal-report.tex' }
    'Form'   { 'imdt-topic-work-plan.tex' }
    'All'    { 'imdt-proposal-report.tex'; 'imdt-topic-work-plan.tex' }
}
Push-Location $projectRoot
try {
    foreach ($document in $targets) {
        if ($Clean) {
            & latexmk -C "-outdir=$buildRoot" $document
        } else {
            & latexmk -xelatex "-outdir=$buildRoot" $document
        }
        if ($LASTEXITCODE -ne 0) { throw "Build failed: $document" }
    }
} finally {
    Pop-Location
}
if (-not $Clean) { Write-Host "PDF output: $buildRoot" }
