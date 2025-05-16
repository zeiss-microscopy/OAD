# ZEN API Playground

## Remarks

Owner: Sebastian Rhode

This folder contains experimental files to play around and test ZEN API functionality.

## Python Environment

In order to use ZEN API from Python one needs to create a suitable python environment.
In case one needs a new environment here please create on freshly using the `env_zenapi.yml`

### Prerequisites

* Make sure the ZEN API gateway is installed
* Generate the control token
* Install conda or [miniconda](https://docs.anaconda.com/free/miniconda/) or [miniforge](https://conda-forge.org/miniforge/) base environment 

Open CMD or PowerShell etc. and create a new python environment:

    conda env create --file env_zenapi.yml
    conda activate zenapi

> **IMPORTANT**: Feel free to use your own environment and install only the packages you really need.

## Creation of python files for ZEN API

In order to use ZEN API from Python the respective python files need to be created based on the protofiles (with the help of the betterproto package).

> **IMPORTANT**: If you use the example from this repository you do not need to **translate** the *.proto files into python code anymore!

* make sure RMS_ZEN (may using the respective feature branch) is up to date
* make sure RMS_ZENAPI is up-to-date
* open console and activate the desired python environment

> **IMPORTANT**: The folder below might need to be adapted to your specific needs!

    protoc -I F:\AzureDevOps\RMS_ZEN\ZenApi\proto -I F:\AzureDevOps\RMS_ZENAPI\Source\Tools\ZenApi.Tools.DocBuilder\include --python_betterproto_out=f:\AzureDevOps\RMS_Users\Playground\ZEN_API\ F:\AzureDevOps\RMS_ZEN\ZenApi\proto\zen_api\acquisition\v1alpha\*.proto

### Automation

```powershell
# !!! THESE NEED TO BE UPDATED TO YOUR LOCAL PATH etc. !!!

$path_rms_zen = "F:\AzureDevOps\RMS_ZEN"
$rms_zen_branch = "develop"

$path_rms_zenapi = "F:\AzureDevOps\RMS_ZENAPI"
$rms_zenapi_branch = "develop"
$condaenv = "zen"
$path_rms_zen_proto_public = Join-Path -Path $path_rms_zen -ChildPath "ZenApi\proto\Public"
$path_rms_zen_proto_internal = Join-Path -Path $path_rms_zen -ChildPath "ZenApi\proto\Internal"
$path_rms_zenapi_include = Join-Path -Path $path_rms_zenapi -ChildPath "Source\Tools\ZenApi.Tools.DocBuilder\include"
$path_betterproto_out_public = "F:\AzureDevOps\RMS_Users\Playground\ZEN_API\public"
$path_betterproto_out_internal = "F:\AzureDevOps\RMS_Users\Playground\ZEN_API\internal"

# Check if the directory exists
if (-Not (Test-Path -Path $path_betterproto_out_internal)) {
    # Create the directory if it does not exist
    New-Item -Path $path_betterproto_out_internal -ItemType Directory
    Write-Host "Directory created: $path_betterproto_out_internal"
} else {
    Write-Host "Directory already exists: $path_betterproto_out_internal"
}

# Check if the directory exists
if (-Not (Test-Path -Path $path_betterproto_out_public)) {
    # Create the directory if it does not exist
    New-Item -Path $path_betterproto_out_public -ItemType Directory
    Write-Host "Directory created: $path_betterproto_out_public"
} else {
    Write-Host "Directory already exists: $path_betterproto_out_public"
}


$git_update_zen_develop = $true
$git_update_fb = $true
$git_update_zenapi = $true
$create_python_zenapi_public = $true
$create_python_zenapi_internal = $true


# update the repos if needed
if ($git_update_zen_develop)
{
    Set-Location -Path $path_rms_zen
    Write-Output "Update RMS-ZEN Develop ..."
    git checkout "develop"
    git pull
}

# update the repos if needed
if ($git_update_fb)
{
    Set-Location -Path $path_rms_zen
    Write-Output "Update RMS-ZEN Feature Branch: $rms_zen_branch"
    git checkout $rms_zen_branch
    git pull
}

# update the repos if needed
if ($git_update_zenapi)
{
    Set-Location -Path $path_rms_zenapi
    Write-Output "Update RMS_ZENAPI"
    git checkout $rms_zenapi_branch
    git pull
}


# create python files from public protofiles using python-betterproto
if ($create_python_zenapi_public)
{
    # switch to the actual python environment
    Write-Output "--------------------------------------------------------------------------------" 
    Write-Output "Switch to Environment: $condaenv"
    conda activate $condaenv

    # check the paths
    Write-Output "Directory with *.proto files: $path_rms_zen_proto_public"
    Write-Output $path_rms_zenapi_include
    Write-Output "ZEN API Working Directory: $path_betterproto_out_public"

    # create the python files from proto files for all APIs
    $ErrorActionPreference = "SilentlyContinue"

    # create filist of files to be translated
    $protolist = dir -Path $path_rms_zen_proto_public -Filter *.proto -Recurse | %{$_.FullName}

    # translate from proto to python
    Write-Output "--------------------------------------------------------------------------------"
    
    protoc -I $path_rms_zen_proto_public -I $path_rms_zenapi_include --python_betterproto_out=$path_betterproto_out_public $protolist

    # show the list of translated files
    foreach ($single in $protolist) {
        Write-Output "Creating Python-Files for: $single"
    }
}

# create python files from public protofiles using python-betterproto
if ($create_python_zenapi_internal)
{
    # switch to the actual python environment
    Write-Output "--------------------------------------------------------------------------------" 
    Write-Output "Switch to Environment: $condaenv"
    conda activate $condaenv

    # check the paths
    Write-Output "Directory with *.proto files: $path_rms_zen_proto_internal"
    Write-Output $path_rms_zenapi_include
    Write-Output "ZEN API Working Directory: $path_betterproto_out_internal"

    # create the python files from proto files for all APIs
    $ErrorActionPreference = "SilentlyContinue"

    # create filist of files to be translated
    $protolist = dir -Path $path_rms_zen_proto_internal -Filter *.proto -Recurse | %{$_.FullName}

    # translate from proto to python
    Write-Output "--------------------------------------------------------------------------------"
    
    #protoc -I $path_rms_zen_proto_internal -I $path_rms_zenapi_include --python_betterproto_out=$zenapi_workdir $protolist
    protoc -I $path_rms_zen_proto_internal -I $path_rms_zenapi_include --python_betterproto_out=$path_betterproto_out_internal $protolist

    # show the list of translated files
    foreach ($single in $protolist) {
        Write-Output "Creating Python-Files for: $single"
    }
}

$ErrorActionPreference = "Continue" # reset to default

pause
```

After this completed one should have the following folder structure (or something similar) inside the target folder.

```
.
└── target_folder/
    ├── public/
        ├── zen_api/
        │   ├── acquisition/
        │   │   ├── v1alpha/
        │   │   │   └── __init__.py
        │   │   └── __init__.py
        │   └── __init__.py
        ├── __init__.py
    ├── internal/
        ├── zen_api/
        │   ├── acquisition/
        │   │   ├── v1alpha/
        │   │   │   └── __init__.py
        │   │   └── __init__.py
        │   └── __init__.py
        ├── __init__.py
    ├── your_zenapi_scripts.py
        └── ...
```

## Configuration

Make sure the `config.ini` is updated with the correct values. An example is shown here:

```ini
[api]
host = 127.0.0.1
port = 5000
cert_file = C:\ProgramData\Carl Zeiss\ZenApiGateway\Certificates\ZenApiPersonalSigningRootCA.pem
control-token = 73b96e379c53466fab6e5d75e360bec8

[image_streaming]
host = 127.0.0.1
port = 5280
```
