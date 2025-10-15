# Dev Log

## 🧩 2025-10-15 — Bug Hunt: Company Name Missing, File Name Directories LibreOffice Spreadsheet listing "Unknown Company" 

**Symptom:**  
All job entries were saved with "Unknown Company" even when the filename contained the company name.

**Diagnosis:**  
- Extraction logic worked for title, but not company.
- The final fallback (filename parsing) was indented inside a conditional — so it was never hit.
- `return` was also incorrectly indented, exiting too early.

**Fix:**  
- Unindented and centralized the fallback block in `extract_job_info()`
- Made sure company fallback kicks in if the name is still `"Unknown Company"` after all parsing attempts

**Lesson:**  
- Always test fallbacks *explicitly*
- Use debug prints to confirm what each logic block actually hits
- DRY (Don't Repeat Yourself) redundancy tests are important
