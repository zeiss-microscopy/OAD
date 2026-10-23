param(
    [switch]$Test,
    [string]$ZenApiPackagePath
)

$ErrorActionPreference = "Stop"

$packageRoot = $PSScriptRoot
$repositoryRoot = Split-Path -Parent $packageRoot
$distPath = Join-Path $packageRoot "dist"
$localBuildRoot = Join-Path $repositoryRoot ".build"

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

function Resolve-ZenApiPackagePath {
    param([string]$SourcePath)

    if ([string]::IsNullOrWhiteSpace($SourcePath)) {
        $SourcePath = Join-Path $repositoryRoot "python_packages\zen_api-2026.11.1"
    }

    if (-not (Test-Path (Join-Path $SourcePath "pyproject.toml")) -or
        -not (Test-Path (Join-Path $SourcePath "src\zen_api"))) {
        throw "The supplied zen_api package path is invalid: $SourcePath"
    }

    return (Resolve-Path $SourcePath).Path
}

function Build-LocalZenApiWheel {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath
    )

    $zenApiBuildPath = Join-Path $localBuildRoot "zen_api"
    if (Test-Path $zenApiBuildPath) {
        Remove-Item -Path $zenApiBuildPath -Recurse -Force
    }
    New-Item -ItemType Directory -Path $zenApiBuildPath -Force | Out-Null

    Push-Location $SourcePath
    try {
        Invoke-Python @("-m", "build", "--wheel", "--outdir", $zenApiBuildPath)
    }
    finally {
        Pop-Location
    }

    $wheel = Get-ChildItem -Path $zenApiBuildPath -Filter "zen_api-*.whl" -File |
        Select-Object -First 1
    if ($null -eq $wheel) {
        throw "The local zen_api wheel was not created."
    }

    return $wheel.FullName
}

function Get-PackageVersion {
    param([string]$ProjectPath)

    $metadataPath = Join-Path $ProjectPath "pyproject.toml"
    $version = & python -c 'import sys, tomllib; print(tomllib.loads(open(sys.argv[1], encoding="utf-8").read())["project"]["version"])' $metadataPath
    if ($LASTEXITCODE -ne 0) {
        throw "Package version could not be read from $metadataPath."
    }

    return $version
}

function Build-Documentation {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ZenApiPackagePath
    )

    $zenApiSourcePath = Join-Path $ZenApiPackagePath "src"
    $packageSourcePath = Join-Path $packageRoot "src"
    $generatorPath = Join-Path $repositoryRoot "packaging\generate_mkdocs_pages.py"
    $packagingPath = Join-Path $repositoryRoot "packaging"
    $staticDocsPath = Join-Path $packageRoot "mkdocs_docs"
    $configPath = Join-Path $ZenApiPackagePath "docs\mkdocs_generated.yml"
    $version = Get-PackageVersion -ProjectPath $ZenApiPackagePath
    $protoPath = Join-Path $repositoryRoot "protofiles\proto_$version"

    if (-not (Test-Path $generatorPath)) {
        throw "MkDocs page generator was not found: $generatorPath"
    }
    if (-not (Test-Path $staticDocsPath)) {
        throw "Utility package static docs were not found: $staticDocsPath"
    }

    $originalPythonPath = $env:PYTHONPATH
    $env:PYTHONPATH = @($packageSourcePath, $zenApiSourcePath) -join [IO.Path]::PathSeparator
    try {
        Invoke-Python @(
            $generatorPath,
            "--src_path", $zenApiSourcePath,
            "--packaging_path", $packagingPath,
            "--output_path", $ZenApiPackagePath,
            "--version", $version,
            "--proto_path", $protoPath,
            "--utils_path", $packageRoot
        )

        Invoke-Python @(
            "-m", "mkdocs", "build",
            "--config-file", $configPath,
            "--strict"
        )
    }
    finally {
        $env:PYTHONPATH = $originalPythonPath
    }
}

$ZenApiPackagePath = Resolve-ZenApiPackagePath -SourcePath $ZenApiPackagePath

if ($Test) {
    Write-Host "Building local zen_api dependency from: $ZenApiPackagePath"
    $zenApiWheelPath = Build-LocalZenApiWheel -SourcePath $ZenApiPackagePath
    Invoke-Python @("-m", "pip", "install", "--force-reinstall", $zenApiWheelPath)
}

if (Test-Path $distPath) {
    Remove-Item -Path $distPath -Recurse -Force
}

Push-Location $packageRoot
try {
    Invoke-Python @("-m", "build")
    Invoke-Python @("-m", "twine", "check", (Join-Path $distPath "*.whl"), (Join-Path $distPath "*.tar.gz"))
    Build-Documentation -ZenApiPackagePath $ZenApiPackagePath

    if ($Test) {
        Invoke-Python @("-m", "pip", "install", "--no-deps", "-e", ".[dev]")
        Invoke-Python @("-m", "pytest")
    }
}
finally {
    Pop-Location
}

Write-Host "Distributions created in $distPath"
Get-ChildItem -Path $distPath -File | Select-Object -ExpandProperty Name