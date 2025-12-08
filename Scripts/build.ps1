# PowerShell script for building backend on Windows
# Equivalent to build.sh for Windows CI/CD

$ErrorActionPreference = "Stop"

# ---------------------
#  CONFIG
# ---------------------

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$CLI_DIR = Join-Path $PROJECT_ROOT "CLI"
$BACKEND_DIR = Join-Path $PROJECT_ROOT "Backend"

$ENTRY_POINT = "CLI"
$OUTPUT_DIR = "dist"

Write-Host "================================================"
Write-Host "  8085 Microprocessor Simulator - CLI Build Script (Windows)"
Write-Host "================================================"
Write-Host ""
Write-Host "Project Root: $PROJECT_ROOT"
Write-Host "CLI Dir:      $CLI_DIR"
Write-Host "Backend Dir:  $BACKEND_DIR"
Write-Host "Output Dir:   $PROJECT_ROOT\$OUTPUT_DIR"
Write-Host ""

# Ensure a project-root virtualenv exists and install requirements there
$VENV_DIR = Join-Path $PROJECT_ROOT ".venv"
if (-not (Test-Path $VENV_DIR)) {
    Write-Host "Creating virtualenv at $VENV_DIR"
    python -m venv $VENV_DIR
} else {
    Write-Host "Using existing virtualenv at $VENV_DIR"
}

# Try to activate the venv (PowerShell activation)
$activateScript = Join-Path $VENV_DIR "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "Warning: Activate script not found at $activateScript — continuing without activation"
}

Write-Host "Upgrading pip and installing project requirements (if present)"
& python -m pip install --upgrade pip
$reqPath = Join-Path $PROJECT_ROOT "requirements.txt"
if (Test-Path $reqPath) {
    & python -m pip install -r $reqPath
} else {
    Write-Host "Warning: requirements.txt not found at $reqPath — continuing"
}

# Clean old builds
Write-Host "Cleaning old builds..."
$pathsToClean = @(
    (Join-Path $PROJECT_ROOT $OUTPUT_DIR),
    (Join-Path $PROJECT_ROOT "build"),
    (Join-Path $PROJECT_ROOT "*.dist"),
    (Join-Path $PROJECT_ROOT "*.build")
)
foreach ($path in $pathsToClean) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Building CLI using Nuitka (onefile)..."
Write-Host ""

Set-Location $PROJECT_ROOT

# Check if Nuitka is installed
try {
    python -m nuitka --version | Out-Null
} catch {
    Write-Host "Error: Nuitka is not installed."
    Write-Host "   Install it with: pip install nuitka"
    exit 1
}

# Build with Nuitka
python -m nuitka `
    --standalone `
    --onefile `
    --follow-imports `
    --enable-plugin=no-qt `
    --python-flag=-m `
    --assume-yes-for-downloads `
    --include-data-files=Backend/M8085/commands_property.yml=Backend/M8085/commands_property.yml `
    --include-data-files=Backend/M8085/docs.yml=Backend/M8085/docs.yml `
    --output-dir=$OUTPUT_DIR `
    $ENTRY_POINT

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Nuitka build failed"
    exit 1
}

Write-Host ""
Write-Host "Nuitka build complete!"
Write-Host ""

# Copy the CLI binary to release directory
Write-Host "Preparing CLI binary for release..."

# Create release directory
if (-not (Test-Path $RELEASE_DIR)) {
    New-Item -ItemType Directory -Path $RELEASE_DIR -Force | Out-Null
}

$SOURCE_BINARY = Join-Path $PROJECT_ROOT "$OUTPUT_DIR\CLI.exe"
$DEST_BINARY = Join-Path $RELEASE_DIR "8085-simulator.exe"

# Check if source binary exists
if (-not (Test-Path $SOURCE_BINARY)) {
    Write-Host "Error: Binary not found at $SOURCE_BINARY"
    Write-Host "   Looking for alternatives..."
    Get-ChildItem -Path (Join-Path $BACKEND_DIR $OUTPUT_DIR) -ErrorAction SilentlyContinue
    exit 1
}

# Copy binary
Copy-Item -Path $SOURCE_BINARY -Destination $DEST_BINARY -Force

Write-Host "CLI binary created: $DEST_BINARY"

# Verify the binary
if (Test-Path $DEST_BINARY) {
    $size = (Get-Item $DEST_BINARY).Length / 1MB
    Write-Host "CLI binary size: $([math]::Round($size, 2)) MB"
} else {
    Write-Host "Warning: CLI binary may not exist at destination"
}

Write-Host ""
Write-Host "================================================"
Write-Host "  Build Summary"
Write-Host "================================================"
Write-Host ""
Write-Host "CLI binary:      $DEST_BINARY"
Write-Host "Output dir:      $PROJECT_ROOT\$OUTPUT_DIR"
Write-Host ""
Write-Host "Usage:"
Write-Host "   Run the CLI: $DEST_BINARY"
Write-Host ""
Write-Host "For development:"
Write-Host "   python -m CLI"
Write-Host ""
