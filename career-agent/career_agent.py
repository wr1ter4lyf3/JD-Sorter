# Current Working Script as of 10-15-2025
import time
import shutil
import subprocess
import re
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === USER PATHS ===
BASE_DIR = Path.home() / "Documents" / "Career" / "job-apps"
INBOX = Path.home() / "Desktop"  # folder to monitor

# ---------- helpers ----------
def sanitize(text: str) -> str:
    return "".join(c for c in text if c not in '<>:"/\\|?*').strip()


def get_role_bucket(text: str) -> str:
    """
    Weighted keyword scoring for job classification.
    Scores Cyber, Helpdesk, and Network roles based on title + JD text.
    Picks whichever has the highest weighted score.
    """

    t = text.lower()

    # keyword groups with weights
    buckets = {
        "Cybersecurity Roles": {
            "keywords": [
                "cyber", "security", "soc", "siem", "incident", "threat",
                "blue team", "detection", "response", "forensics", "infosec",
                "information security", "malware", "risk", "vulnerability"
            ],
            "weight": 2
        },
        "Helpdesk Roles": {
            "keywords": [
                "help desk", "service desk", "desktop support", "technical support",
                "it support", "system support", "troubleshoot", "ticket", "end user"
            ],
            "weight": 1
        },
        "Networking Roles": {
            "keywords": [
                "network", "routing", "switching", "firewall", "vpn",
                "lan", "wan", "tcp", "dns", "dhcp", "cisco"
            ],
            "weight": 1.5
        }
    }

    # initialize scores
    scores = {bucket: 0 for bucket in buckets}

    # count keyword appearances
    for bucket, config in buckets.items():
        for kw in config["keywords"]:
            count = t.count(kw)
            if count:
                scores[bucket] += count * config["weight"]

    # choose the highest-scoring category
    best_bucket = max(scores, key=scores.get)

    # If no matches at all, fall back to "Other Roles"
    if scores[best_bucket] == 0:
        return "Other Roles"

    return best_bucket


def ensure_dirs(bucket: str, title: str, company: str):
    if not company.strip():
        company = "Unknown Company"

    bucket_path = BASE_DIR / bucket
    job_folder = bucket_path / f"{title} - {company}"
    subfolders = ["Job-Description", "Resume-Submitted", "Cover-letter-Submitted", "Correspondences", "Offer"]
    bucket_path.mkdir(parents=True, exist_ok=True)
    job_folder.mkdir(exist_ok=True)
    for sf in subfolders:
        (job_folder / sf).mkdir(exist_ok=True)
    return job_folder

import ezodf

def update_tracker(bucket: str, title: str, company: str, job_folder: Path):
    tracker_path = BASE_DIR / "tracker.ods"

    # Open the ODS file
    doc = ezodf.opendoc(str(tracker_path))
    sheet = doc.sheets[0]  # use first sheet

    # 🧱 Ensure sheet is big enough
    NUM_COLUMNS = 6
    MAX_ROWS = 1000
    current_rows = len(list(sheet.rows()))
    current_cols = len(list(sheet.columns()))

    if current_rows < MAX_ROWS or current_cols < NUM_COLUMNS:
        sheet.reset(size=(MAX_ROWS, NUM_COLUMNS))

    if current_rows < MAX_ROWS or current_cols < NUM_COLUMNS:
        sheet.reset(size=(MAX_ROWS, NUM_COLUMNS))

    # 🔍 Find the first empty row
    row_index = 0
    for row in sheet.rows():
        if not row[0].value:
            break
        row_index += 1

    # 📋 Prepare new row data
    today = datetime.now().strftime("%Y-%m-%d")
    values = [today, company, title, bucket, str(job_folder), "new"]

    # ✍️ Write to the row
    for col_index, value in enumerate(values):
        sheet[row_index, col_index].set_value(value)

    # 💾 Save file
    doc.save()
    print(f"✅ Tracker updated in row {row_index + 1}")


# ---------- extraction logic ----------
import re
from pathlib import Path

def extract_job_info(jd_text: str, fallback_filename: str):
    title, company = "Unknown Role", "Unknown Company"

    # comment out initial parsing for test
    # lines = jd_text.splitlines()
    # for line in lines[:15]:
    #     ...

    # ✅ Only run fallback
    filename = fallback_filename
    parts = filename.split(" - ")
    print(f"🧪 Fallback filename parts: {parts}")
    if len(parts) >= 2:
        title = sanitize(parts[0])
        company = sanitize(" - ".join(parts[1:]))
        print(f"🎯 Fallback extracted: {title} | {company}")

    return title, company


    # Step 2: Smart guess — lines like "Acme Corp is hiring"
    if company == "Unknown Company":
        for line in lines[:30]:
            match = re.match(r"^([\w\s&\-\(\)]+?)\s+(is\s+looking\s+for|is\s+hiring|seeks|seeking)", line.strip(), re.IGNORECASE)
            if match:
                company = sanitize(match.group(1))
                break

            match = re.match(r"^about\s+(.+?):", line.strip(), re.IGNORECASE)
            if match:
                company = sanitize(match.group(1))
                break

    # Step 3: Final fallback — use filename
    if title == "Unknown Role" or company == "Unknown Company":
        filename = Path(fallback_filename).stem  # removes .txt
        parts = filename.split(" - ")
        if len(parts) >= 2:
            title_from_file = sanitize(parts[0])
            company_from_file = sanitize(" - ".join(parts[1:]))

            if title == "Unknown Role":
                title = title_from_file
            if company == "Unknown Company":
                company = company_from_file
                
    # 🧾 Step 4: Final fallback — extract from filename like "Role - Company.txt"
    filename = fallback_filename  # Don't call .stem again!
    parts = filename.split(" - ")
    if len(parts) >= 2:
        print(f"🧪 Parsed from filename: {parts}")
        title_from_file = sanitize(parts[0])
        company_from_file = sanitize(" - ".join(parts[1:]))

        if title == "Unknown Role":
            title = title_from_file
        if company == "Unknown Company":
            company = company_from_file               

    # Final safety
    if not title.strip():
        title = "Unknown Role"
    if not company.strip():
        company = "Unknown Company"

    return title, company

# ---------- main processor ----------
def process_jobfile(txt_path: Path):
    if not txt_path.exists():
        return

    jd_text = txt_path.read_text(encoding="utf-8", errors="ignore")

    # ✅ Use the new helper to extract title + company
    title, company = extract_job_info(jd_text, txt_path.stem)

    # 🧪 Optional debug print
    print(f"🧾 Extracted Title: {title}")
    print(f"🏢 Extracted Company: {company}")

    # ✅ Classify job and create folder
    bucket = get_role_bucket(f"{title} {jd_text}")
    job_folder = ensure_dirs(bucket, title, company)

    # ✅ Move the file into the new folder
    dest = job_folder / "Job-Description" / txt_path.name
    shutil.move(str(txt_path), dest)

    # ✅ Update the tracker
    update_tracker(bucket, title, company, job_folder)

    print(f"📄 Processed: {txt_path.name}")
    print(f"🗂  Moved to: {dest}")
    print(f"🧭  Bucket:  {bucket}\n")

    # ✅ Open the job folder automatically in Explorer
    try:
        subprocess.Popen(["explorer.exe", str(job_folder)])
        print(f"📂 Opened folder: {job_folder}\n")
    except Exception as e:
        print(f"⚠ Could not open Explorer: {e}")


# ---------- watchdog handler ----------
class JDHandler(FileSystemEventHandler):
    def __init__(self, seen):
        super().__init__()
        self.seen = seen

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".txt"):
            return
        path = Path(event.src_path)
        self._maybe_process(path)

    def _maybe_process(self, path: Path):
        if path in self.seen:
            return
        time.sleep(1)  # allow file to finish writing
        if path.exists():
            process_jobfile(path)
            print(f"🧪 File name stem: {path.stem}")
            self.seen.add(path)


# ---------- hybrid loop ----------
def main():
    print(f"👀 Watching {INBOX} ... Press Ctrl+C to stop.\n")
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    seen = set()

    # --- Startup sweep ---
    existing_files = list(INBOX.glob("*.txt"))
    if existing_files:
        print(f"📦 Found {len(existing_files)} existing JD file(s). Processing now...\n")
        for f in existing_files:
            process_jobfile(f)
            seen.add(f)
    else:
        print("🟢 No existing JD files found. Waiting for new ones...\n")

    # --- Start watchdog observer ---
    observer = Observer()
    observer.schedule(JDHandler(seen), str(INBOX), recursive=False)
    observer.start()

    try:
        while True:
            # poll every 5s for missed files
            for f in INBOX.glob("*.txt"):
                if f not in seen:
                    process_jobfile(f)
                    seen.add(f)
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
