param([string]$Target = (Join-Path $HOME ".agents/skills"))

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (git -C $repoRoot status --porcelain) { throw "Refusing to update: the package checkout has uncommitted changes." }
git -C $repoRoot remote get-url origin *> $null
if ($LASTEXITCODE -ne 0) { throw "Refusing to update: no origin remote is configured for this package." }
git -C $repoRoot pull --ff-only
& (Join-Path $PSScriptRoot "install-windows.ps1") -Target $Target
