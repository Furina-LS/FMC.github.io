# ===================================================================
# Create Hidden Desktop Shortcut for Mouse Clicker
# Creates a shortcut that runs without showing terminal window
# ===================================================================

# Define paths
$scriptPath = $PSScriptRoot
$vbsFile = Join-Path -Path $scriptPath -ChildPath "MouseClicker.vbs"
$desktopPath = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path -Path $desktopPath -ChildPath "Mouse Clicker.lnk"

# Check if the VBS file exists
if (-not (Test-Path -Path $vbsFile -PathType Leaf)) {
    Write-Host "ERROR: VBS wrapper file not found at: $vbsFile" -ForegroundColor Red
    Write-Host "Please ensure MouseClicker.vbs is in the same directory as this script." -ForegroundColor Yellow
    pause
    exit 1
}

# Create shortcut
Write-Host "Creating desktop shortcut for Mouse Clicker (hidden terminal)..." -ForegroundColor Green

try {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $vbsFile
    $shortcut.WorkingDirectory = $scriptPath
    $shortcut.Description = "Mouse Clicker - Double click to launch (hidden terminal)"
    $shortcut.Save()
    
    Write-Host ""
    Write-Host "===================================================================" -ForegroundColor Green
    Write-Host "Desktop shortcut 'Mouse Clicker' has been updated successfully!" -ForegroundColor Green
    Write-Host "===================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📌 How to Use:" -ForegroundColor Cyan
    Write-Host "1. Double click the 'Mouse Clicker' icon on your desktop" -ForegroundColor Cyan
    Write-Host "2. The Mouse Clicker will start without showing any terminal window" -ForegroundColor Cyan
    Write-Host "3. The Mouse Clicker window will open automatically" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎯 Features:"
    Write-Host "   - No terminal window shown during startup"
    Write-Host "   - Press F9 to start/stop clicking"
    Write-Host "   - Adjust clicking speed with slider"
    Write-Host "   - Real-time status display"
    Write-Host "   - System tray support"
    Write-Host ""
    Write-Host "✅ Now you can enjoy a clean, terminal-free experience!" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to create shortcut: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

pause
