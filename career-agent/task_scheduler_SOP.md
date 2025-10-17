# Add Start-up Code to Windows Task Scheduler

Task scheduler allows the code to run automatically when logging in.

1. Open Task Scheduler (search for it in the Start menu)

2. Click Create Basic Task...

<img width="1335" height="893" alt="image" src="https://github.com/user-attachments/assets/ad322d0a-6cca-4256-a6ce-93414d6da375" /></br></br>


<img width="868" height="607" alt="image" src="https://github.com/user-attachments/assets/c23906a6-cfb9-4d9a-a0c2-6c4ad0f7dd13" />



3. Name it something like:

Job Sorter Watcher

4. Trigger: “When I log on”

5. Action: “Start a program”

6. Program/script:

`powershell.exe`


7. Add arguments:

`-ExecutionPolicy Bypass -File "C:\Users\Student\Documents\Career\scripts\job_watcher_launcher.ps1"`


Finish the wizard.

✅ Done!
Next time you log in, your Job Sorter watcher will start automatically in the background.


## 🚀 Bonus: Manual One-Click Shortcut

If you want a desktop shortcut too:

Right-click your .ps1 file → Create shortcut

Right-click the shortcut → Properties

In Target, add:

`powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Student\Documents\Career\scripts\job_watcher_launcher.ps1"`

Change icon (optional 😎)

Now you’ve got both automatic and manual launch options.
