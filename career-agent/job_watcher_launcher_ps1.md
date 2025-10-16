# Current as of 10-16-25

```PowerShell # === job_watcher_launcher.ps1 ===
# Runs the Job Sorter Python automation at startup

Write-Host "🚀 Launching Job Sorter..."

# --- Path to Python ---
$python = "C:\Users\Student\AppData\Local\Programs\Python\Python313\python.exe"

# --- Path to your script ---
$script = "C:\Users\Student\Documents\Career\scripts\career_agent_hybrid_v2.py"

# --- Start it in the background ---
Start-Process -FilePath $python -ArgumentList "`"$script`"" -WindowStyle Hidden

Write-Host "✅ Job Sorter started successfully!"
```
