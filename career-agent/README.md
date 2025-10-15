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
🛠️ Tech Used

watchdog for file monitoring

ezodf to write .ods spreadsheets

LibreOffice macros (for color-coding)

Python 3.13+

🧪 Sample Run
🧾 Extracted Title: Security Analyst
🏢 Extracted Company: MegaCorp
✅ Tracker updated in row 4
📄 Processed: Security Analyst - MegaCorp.txt
🧭 Bucket:  Cybersecurity Roles

🔄 To Do

 Optional GUI frontend

 Job deduplication logic

 Auto-open job description in LibreOffice

📜 License

MIT (or any license you want)
