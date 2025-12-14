# PowerShell script to create a desktop shortcut for Mouse Clicker

# Define paths
$ScriptPath = $PSScriptRoot
$BatchFile = Join-Path -Path $ScriptPath -ChildPath "MouseClicker.bat"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath "Mouse Clicker.lnk"

# Check if batch file exists
if (-not (Test-Path -Path $BatchFile)) {
    Write-Host "Error: MouseClicker.bat not found in the same directory." -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit
}

# Create shortcut
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatchFile
$Shortcut.IconLocation = "imageres.dll,146"  # Use default mouse icon
$Shortcut.Description = "Mouse Clicker - Press F9 to start/stop"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host "\nDouble-click the shortcut to launch Mouse Clicker."
Write-Host "Use F9 key to start/stop clicking."

Read-Host "Press Enter to exit..."
