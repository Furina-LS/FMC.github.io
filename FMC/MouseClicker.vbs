' ===================================================================
' Mouse Clicker VBScript Wrapper
' Runs the Mouse Clicker without showing a terminal window
' ===================================================================

Option Explicit

Dim objShell, strBatPath, strArgs

' Get the path to the batch file (same directory as this VBS file)
strBatPath = Replace(WScript.ScriptFullName, WScript.ScriptName, "MouseClickerLauncher.bat")

' Create a shell object
Set objShell = CreateObject("WScript.Shell")

' Run the batch file hidden (0 = hidden, 1 = normal window, 2 = minimized)
objShell.Run Chr(34) & strBatPath & Chr(34), 0, False

' Clean up
Set objShell = Nothing
