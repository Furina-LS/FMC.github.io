# ===================================================================
# Create Desktop Shortcut for Mouse Clicker Launcher
# ===================================================================

# Define paths
$scriptPath = $PSScriptRoot
$batchFile = Join-Path -Path $scriptPath -ChildPath "MouseClickerLauncher.bat"
$desktopPath = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path -Path $desktopPath -ChildPath "Mouse Clicker.lnk"

# Check if the batch file exists
if (-not (Test-Path -Path $batchFile -PathType Leaf)) {
    Write-Host "ERROR: Batch file not found at: $batchFile" -ForegroundColor Red
    Write-Host "Please ensure MouseClickerLauncher.bat is in the same directory as this script." -ForegroundColor Yellow
    pause
    exit 1
}

# Create shortcut
Write-Host "Creating desktop shortcut for Mouse Clicker..." -ForegroundColor Green

try {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $batchFile
    $shortcut.WorkingDirectory = $scriptPath
    $shortcut.Description = "Mouse Clicker - Double click to launch"
    $shortcut.Save()
    
    Write-Host ""
    Write-Host "==================================================================="
    Write-Host "Desktop shortcut 'Mouse Clicker' has been created successfully!" -ForegroundColor Green
    Write-Host "==================================================================="
    Write-Host ""
    Write-Host "📌 How to Use:" -ForegroundColor Cyan
    Write-Host "1. Double click the 'Mouse Clicker' icon on your desktop"
    Write-Host "2. A launcher will appear briefly to start the application"
    Write-Host "3. The Mouse Clicker window will open automatically"
    Write-Host ""
    Write-Host "🎯 Features:" -ForegroundColor Cyan
    Write-Host "- Press F9 to START/STOP clicking"
    Write-Host "- Adjust clicking speed with slider"
    Write-Host "- Real-time status display"
    Write-Host "- Professional-looking interface"
    Write-Host ""
    Write-Host "⚠️  Note: This uses Python, so make sure you have Python 3.x installed!"
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to create shortcut: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

pause
