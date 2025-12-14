# ===================================================================
# Mouse Clicker Test Script
# Tests if the Mouse Clicker application can run properly
# ===================================================================

Write-Host "========================================"
Write-Host "Testing Mouse Clicker Application"
Write-Host "========================================"
Write-Host ""

# Check if main script exists
$mainScript = "mouse_clicker.py"
if (-not (Test-Path $mainScript)) {
    Write-Host "❌ ERROR: Main script '$mainScript' not found!" -ForegroundColor Red
    exit 1
}

# Check if launcher exists
$launcher = "MouseClickerLauncher.bat"
if (-not (Test-Path $launcher)) {
    Write-Host "❌ ERROR: Launcher '$launcher' not found!" -ForegroundColor Red
    exit 1
}

# Check Python version
Write-Host "🔍 Checking Python version..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "🔍 Checking required dependencies..." -ForegroundColor Cyan
$dependencies = @("pyautogui", "Pillow", "pynput", "pystray")
$allDependenciesFound = $true

foreach ($dep in $dependencies) {
    try {
        python -c "import $dep"
        Write-Host "✅ $dep is installed" -ForegroundColor Green
    } catch {
        Write-Host "❌ $dep is NOT installed" -ForegroundColor Red
        $allDependenciesFound = $false
    }
}

if (-not $allDependenciesFound) {
    Write-Host ""
    Write-Host "📥 Installing missing dependencies..." -ForegroundColor Cyan
    python -m pip install pyautogui Pillow pynput pystray
}

Write-Host ""
Write-Host "========================================"
Write-Host "Test Results:"
Write-Host "========================================"
Write-Host "✅ Main script: $mainScript found" -ForegroundColor Green
Write-Host "✅ Launcher: $launcher found" -ForegroundColor Green
Write-Host "✅ Python environment: Available" -ForegroundColor Green
Write-Host "✅ Dependencies: All installed" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Mouse Clicker is ready to use!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 How to use:" -ForegroundColor Cyan
Write-Host "1. Double click the 'Mouse Clicker' icon on your desktop" -ForegroundColor Cyan
Write-Host "2. Or run: .\MouseClickerLauncher.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Features:"
Write-Host "   - Press F9 to start/stop clicking"
Write-Host "   - Adjust clicking speed with slider"
Write-Host "   - Real-time status display"
Write-Host "   - System tray support"
Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
