# Career Agent 🧠📁

Automated job application tracker built with Python and LibreOffice.

## ✨ Features

- Watches a folder for new `.txt` job descriptions
- Extracts job title and company (from file or content)
- Auto-buckets jobs into folders (Cyber, Helpdesk, Network)
- Updates `.ods` tracker spreadsheet with new entries
- LibreOffice macro color-codes rows based on status

## 📂 Folder Structure

```bash
job-apps/
└── Cybersecurity Roles/
    └── Security Analyst - MegaCorp/
        ├── Job-Description/
        └── ...
```

## 🧰 System Requirements

To run this automation reliably, you’ll need:

- **Python 3.11+**
  - Required libraries are listed in `requirements.txt` (`watchdog`, `PyPDF2`, `ezodf`)
  - Install them with:
    ```bash
    pip install -r requirements.txt
    ```

- **PowerShell 7+**
  - The PowerShell script (`career_watcher.ps1`) was written and tested using PowerShell 7.
  - Older versions (such as Windows PowerShell 5.x) may cause encoding or background-process issues.

- **LibreOffice**
  - Used to manage and color-code the job tracker (`tracker.ods`).
  - Not required to run the Python automation, but needed for macro functionality.

---

### 🧱 Optional: Verify PowerShell Version

Run this command in PowerShell:
```powershell
$PSVersionTable.PSVersion
```

🧪 Sample Run
🧾 Extracted Title: Security Analyst </br>
🏢 Extracted Company: MegaCorp </br>
✅ Tracker updated in row 4 </br>
📄 Processed: Security Analyst - MegaCorp.txt </br>
🧭 Bucket:  Cybersecurity Roles </br>

🔄 To Do

 Optional GUI frontend

 Job deduplication logic

 Auto-open job description in LibreOffice

 Parse through resume variants and recommend best-fit depending on JD

📜 License

MIT (or any license you want)
