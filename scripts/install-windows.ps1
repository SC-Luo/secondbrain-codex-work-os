param(
  [string]$Target = (Join-Path $HOME ".agents/skills"),
  [ValidateSet("link", "copy")][string]$Mode = "link",
  [switch]$DryRun,
  [string]$GlobalAgentsTarget
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skills = @("work-os-project-init", "work-os-start", "work-os-shutdown", "work-os-update")

function Invoke-WorkOsAction([scriptblock]$Action, [string]$Description) {
  if ($DryRun) { Write-Output "DRY RUN: $Description" } else { & $Action }
}

Invoke-WorkOsAction { New-Item -ItemType Directory -Force -Path $Target | Out-Null } "create $Target"
foreach ($skill in $skills) {
  $source = Join-Path $repoRoot "skills/$skill"
  $destination = Join-Path $Target $skill
  if (-not (Test-Path (Join-Path $source "SKILL.md"))) { throw "Missing source skill: $source" }
  if (Test-Path $destination) {
    Write-Warning "Skipped existing destination: $destination"
    continue
  }
  if ($Mode -eq "link") {
    Invoke-WorkOsAction { New-Item -ItemType SymbolicLink -Path $destination -Target $source | Out-Null } "link $destination to $source"
  } else {
    Invoke-WorkOsAction { Copy-Item -Recurse -Path $source -Destination $destination } "copy $source to $destination"
  }
}

if ($GlobalAgentsTarget) {
  if (Test-Path $GlobalAgentsTarget) {
    Write-Warning "Skipped existing global AGENTS target: $GlobalAgentsTarget"
  } else {
    $parent = Split-Path -Parent $GlobalAgentsTarget
    Invoke-WorkOsAction { New-Item -ItemType Directory -Force -Path $parent | Out-Null } "create $parent"
    Invoke-WorkOsAction { Copy-Item (Join-Path $repoRoot "agents/GLOBAL_AGENTS.md") $GlobalAgentsTarget } "create $GlobalAgentsTarget"
  }
}

Write-Output "Work OS $(Get-Content (Join-Path $repoRoot "VERSION") -Raw) installation completed."
