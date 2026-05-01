# Install mobilecore-trace-toolkit profiles into Wireshark's per-user config
# directory on Windows.
#
# Usage:
#   .\install.ps1               # copy every profile
#   .\install.ps1 -Uninstall    # remove this toolkit's profiles
#
# Wireshark on Windows stores per-user profiles under:
#   %APPDATA%\Wireshark\profiles\<profile_name>
# Symlinks require Developer Mode; we copy by default for portability.

[CmdletBinding()]
param(
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$RepoRoot     = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProfilesDir  = Join-Path $RepoRoot "profiles"
$ConfigDir    = Join-Path $env:APPDATA "Wireshark"
$Target       = Join-Path $ConfigDir "profiles"

if (-not (Test-Path $Target)) {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

Get-ChildItem -Directory -Path $ProfilesDir | ForEach-Object {
    $name = $_.Name
    $dst  = Join-Path $Target $name

    if ($Uninstall) {
        if (Test-Path $dst) {
            Remove-Item -Recurse -Force $dst
            Write-Host "removed  $dst"
        }
        return
    }

    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    Copy-Item -Recurse -Path $_.FullName -Destination $dst
    Write-Host "copied   $dst"
}

if ($Uninstall) {
    Write-Host ""
    Write-Host "done. removed mobilecore-trace-toolkit profiles from $Target"
} else {
    Write-Host ""
    Write-Host "done. open Wireshark and pick a profile from the bottom-right of the status bar."
}
