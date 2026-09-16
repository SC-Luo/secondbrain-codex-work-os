param([string]$Target = (Join-Path $HOME ".agents/skills"))

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skills = @("work-os-project-init", "work-os-start", "work-os-shutdown", "work-os-update")
$missing = $false
Write-Output "Secondbrain Codex Work OS $(Get-Content (Join-Path $repoRoot "VERSION") -Raw)"
foreach ($skill in $skills) {
  $destination = Join-Path $Target $skill
  if (Test-Path (Join-Path $destination "SKILL.md")) {
    Write-Output "INSTALLED $skill"
  } else {
    Write-Error "MISSING $skill"
    $missing = $true
  }
}
if ($missing) { exit 1 }
