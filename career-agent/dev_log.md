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
- Also learned a lot about Python and LibreOffice!
  
| Method | Creates New File? | Keeps Macros? | Best For
|---|---|---|---|
| convert-to ods | ✅ Yes (overwrites or duplicates)	 | ❌ No	Simple formatting, no macros |Simple formatting, no macros
|ezodf direct edit | ❌ No | 	✅ Yes | Updating .ods without breaking anything |

Perfect — here’s a clean, repo-ready write-up you can drop straight into your `dev_log.md` or a README update section 👇

---

### 🧩 2025-10-18 — Tracker Template Overhaul & Macro Redesign

**Summary:**
Spent one focused hour rebuilding the local job tracker from the ground up. The goal was to reduce clutter, align color psychology with emotional workflow, and prepare for future modularity (e.g., config-based color schemes and encryption).

**What I Did:**

* Created a brand-new **`tracker_template.ods`** file to replace the old sheet.
* Updated header structure for clarity and data relevance:

  ```
  Date Applied | Company | Role / Title | App Source | Resume Type | Projects / Portfolio | Status | Contact & Position | Notes
  ```
* Removed redundant “file path” column — automation already manages file organization.
* Added a **visual color legend row** with psychologically aligned meanings:

  * 🟢 *Hired* – Deep green (`#4CAF50`)
  * 💚 *Offer / Negotiating* – Light green (`#A5D6A7`)
  * 🟡 *Interviewing* – Warm yellow (`#FFF176`)
  * 🟠 / 🧡 *Follow-Up* – Two-step orange gradient (`#FFB74D` → `#FB8C00`)
  * 🔴 *Rejected* – Red (`#EF5350`)
  * ⚪ *Archived* – Neutral gray (`#E0E0E0`)
* Rewrote the **ColorCodeJobs macro** to match the new palette and add gradient logic for follow-ups (deepens color after 2+ days).
* Documented the new palette for potential modular configuration (e.g., a hidden “Config” sheet storing RGB values).

**Next Steps / To-Dos:**

* [ ] Integrate the new column order into the `update_tracker()` function.
* [ ] Implement date-aware follow-up automation logic in Python.
* [ ] Test macro triggers on document open / save.
* [ ] Validate color accuracy across different LibreOffice themes.
* [ ] Consider encrypting “Notes” and “Contact & Position” columns later.
