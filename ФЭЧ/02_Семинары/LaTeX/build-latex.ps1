param(
    [string]$DocDir,
    [string]$DocFile
)

$docDirLeaf = Split-Path -Path $DocDir -Leaf

if ($docDirLeaf -eq 'parts') {
    $latexDir = Split-Path -Path $DocDir -Parent
    $outDir = Join-Path -Path $latexDir -ChildPath 'build_parts'
    $pdfTarget = Join-Path -Path $latexDir -ChildPath ($DocFile + '.pdf')
}
else {
    $latexDir = $DocDir
    $outDir = Join-Path -Path $latexDir -ChildPath 'build_final'
    $projectRoot = Split-Path -Path $latexDir -Parent
    $pdfTarget = Join-Path -Path $projectRoot -ChildPath ($DocFile + '.pdf')
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$texPath = Join-Path -Path $DocDir -ChildPath ($DocFile + '.tex')

Push-Location $DocDir

& latexmk `
    -pdf `
    -interaction=nonstopmode `
    -synctex=1 `
    -file-line-error `
    -outdir="$outDir" `
    "$texPath"

$latexmkExitCode = $LASTEXITCODE

Pop-Location

$builtPdf = Join-Path -Path $outDir -ChildPath ($DocFile + '.pdf')

if (Test-Path -Path $builtPdf) {
    Copy-Item -Path $builtPdf -Destination $pdfTarget -Force
    Write-Host ('PDF copied to: ' + $pdfTarget)
}
else {
    Write-Host ('PDF was not created: ' + $builtPdf)
}

exit $latexmkExitCode