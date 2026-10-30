<#
.SYNOPSIS
Build and validate the zen_api_utils wheel and source distribution.

.DESCRIPTION
Uses Python from the active environment, which must have build and twine installed.
Even when run locally in the omezarr environment, python -m build creates an
isolated build environment and downloads Hatchling into it.

Without BuildIndexUrl, pip uses its configured package sources. HTTP 401 from a
private feed is an authentication failure, not evidence that Hatchling is missing
or that the wrong Python environment is active. Repair the feed authentication
or explicitly select PyPI where your package-source policy permits it.

.PARAMETER BuildIndexUrl
Optional HTTPS package index URL without embedded credentials. Temporarily
bypasses pip configuration files and extra indexes during build and validation.
The original environment settings are restored on success or failure; pip
configuration files and installed project packages are not changed.

.EXAMPLE
.\zen_api_utils\build_package.ps1
Build from the repository root using the active environment and configured feed.

.EXAMPLE
.\zen_api_utils\build_package.ps1 -BuildIndexUrl https://pypi.org/simple
Build using public PyPI instead of a private feed that returns HTTP 401.
This override is opt-in; omitting it continues to use the configured feed.
#>
[CmdletBinding()]
param(
    [uri]$BuildIndexUrl
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false

$packageRoot = $PSScriptRoot
$distPath = Join-Path $packageRoot "dist"

if ($BuildIndexUrl -and (-not $BuildIndexUrl.IsAbsoluteUri -or
    $BuildIndexUrl.Scheme -ne 'https' -or $BuildIndexUrl.UserInfo)) {
    throw "BuildIndexUrl must be an absolute HTTPS URL without embedded credentials."
}

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & python @Arguments | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code ${LASTEXITCODE}: python $($Arguments -join ' ')"
    }
}

Invoke-Python @("-c", "import build, twine")

if (Test-Path $distPath) {
    Remove-Item -Path $distPath -Recurse -Force
}

$originalPipSettings = @{}
Push-Location $packageRoot
try {
    if ($BuildIndexUrl) {
        foreach ($name in @('PIP_CONFIG_FILE', 'PIP_INDEX_URL', 'PIP_EXTRA_INDEX_URL')) {
            $originalPipSettings[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
        }
        $env:PIP_CONFIG_FILE = if ([IO.Path]::DirectorySeparatorChar -eq '\') { 'nul' } else { '/dev/null' }
        $env:PIP_INDEX_URL = $BuildIndexUrl.AbsoluteUri
        $env:PIP_EXTRA_INDEX_URL = $null
    }
    Invoke-Python @("-m", "build")
    Invoke-Python @("-m", "twine", "check", (Join-Path $distPath "*.whl"), (Join-Path $distPath "*.tar.gz"))
}
finally {
    foreach ($name in $originalPipSettings.Keys) {
        if ($null -eq $originalPipSettings[$name]) {
            [Environment]::SetEnvironmentVariable($name, [NullString]::Value, 'Process')
        }
        else {
            [Environment]::SetEnvironmentVariable($name, $originalPipSettings[$name], 'Process')
        }
    }
    Pop-Location
}

Write-Host "Distributions created in $distPath"
Get-ChildItem -Path $distPath -File | Select-Object -ExpandProperty Name