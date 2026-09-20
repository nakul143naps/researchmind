param(
    [string]$Topic = ""
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Test-Path "$scriptDir\.venv\Scripts\Activate.ps1")) {
    throw "Virtual environment not found at $scriptDir\.venv\Scripts\Activate.ps1"
}

& "$scriptDir\.venv\Scripts\Activate.ps1"

$env:OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct"

if ($Topic) {
    Write-Host "Launching app with default topic: $Topic"
    $env:DEFAULT_RESEARCH_TOPIC = $Topic
}

streamlit run app.py
