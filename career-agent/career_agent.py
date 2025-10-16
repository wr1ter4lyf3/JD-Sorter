# Current Working Script as of 10-16-2025
import time
import shutil
import subprocess
import re
import sys
import datetime
from pathlib import Path
from datetime import datetime as dt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ezodf
from PyPDF2 import PdfReader

# === LOGGING ===
log_path = Path.home() / "Documents" / "Career" / "scripts" / "job_sorter.log"
sys.stdout = open(log_path, "a", encoding="utf-8")
sys.stderr = sys.stdout
print(f"\n--- Job Sorter started at {datetime.datetime.now()} ---\n")

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

    scores = {bucket: 0 for bucket in buckets}

    for bucket, config in buckets.items():
        for kw in config["keywords"]:
            count = t.count(kw)
            if count:
                scores[bucket] += count * config["weight"]

    best_bucket = max(scores, key=scores.get)
    if scores[best_bucket] == 0:
        return "Other Roles"

    return best_bucket


# ---------- PDF to TXT converter ----------
def pdf_to_txt(pdf_path: Path) -> Path:
    """
    Converts a PDF job description into a text file.
    """
    txt_path = pdf_path.with_suffix(".txt")
    try:
        reader = PdfReader(str(pdf_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        txt_path.write_text(text, encoding="utf-8")
        print(f"✅ Converted {pdf_path.name} to {txt_path.name}")
        return txt_path
    except Exception as e:
        print(f"⚠ PDF conversion failed for {pdf_path.name}: {e}")
        return pdf_path


# ---------- folder + tracker logic ----------
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


def update_tracker(bucket: str, title: str, company: str, job_folder: Path):
    tracker_path = BASE_DIR / "tracker.ods"

    doc = ezodf.opendoc(str(tracker_path))
    sheet = doc.sheets[0]

    NUM_COLUMNS = 6
    MAX_ROWS = 1000
    current_rows = len(list(sheet.rows()))
    current_cols = len(list(sheet.columns()))

    if current_rows < MAX_ROWS or current_cols < NUM_COLUMNS:
        sheet.reset(size=(MAX_ROWS, NUM_COLUMNS))

    row_index = 0
    for row in sheet.rows():
        if not row[0].value:
            break
        row_index += 1

    today = dt.now().strftime("%Y-%m-%d")
    values = [today, company, title, bucket, str(job_folder), "new"]

    for col_index, value in enumerate(values):
        sheet[row_index, col_index].set_value(value)

    doc.save()
    print(f"✅ Tracker updated in row {row_index + 1}")


# ---------- job info extraction ----------
def extract_job_info(jd_text: str, fallback_filename: str):
    title, company = "Unknown Role", "Unknown Company"

    filename = fallback_filename
    parts = filename.split(" - ")
    print(f"🧪 Fallback filename parts: {parts}")
    if len(parts) >= 2:
        title = sanitize(parts[0])
        company = sanitize(" - ".join(parts[1:]))
        print(f"🎯 Fallback extracted: {title} | {company}")

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

    title, company = extract_job_info(jd_text, txt_path.stem)

    print(f"🧾 Extracted Title: {title}")
    print(f"🏢 Extracted Company: {company}")

    bucket = get_role_bucket(f"{title} {jd_text}")
    job_folder = ensure_dirs(bucket, title, company)

    dest = job_folder / "Job-Description" / txt_path.name
    shutil.move(str(txt_path), dest)

    update_tracker(bucket, title, company, job_folder)

    print(f"📄 Processed: {txt_path.name}")
    print(f"🗂  Moved to: {dest}")
    print(f"🧭  Bucket:  {bucket}\n")

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
        if event.is_directory:
            return
        path = Path(event.src_path)

        if path.suffix.lower() == ".pdf":
            print(f"📄 Detected PDF: {path.name} → converting to text...")
            path = pdf_to_txt(path)

        if path.suffix.lower() == ".txt":
            self._maybe_process(path)

    def _maybe_process(self, path: Path):
        if path in self.seen:
            return
        time.sleep(1)
        if path.exists():
            process_jobfile(path)
            print(f"🧪 File name stem: {path.stem}")
            self.seen.add(path)


# ---------- hybrid loop ----------
def main():
    print(f"👀 Watching {INBOX} ... Press Ctrl+C to stop.\n")
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    seen = set()

    existing_files = list(INBOX.glob("*.txt"))
    if existing_files:
        print(f"📦 Found {len(existing_files)} existing JD file(s). Processing now...\n")
        for f in existing_files:
            process_jobfile(f)
            seen.add(f)
    else:
        print("🟢 No existing JD files found. Waiting for new ones...\n")

    observer = Observer()
    observer.schedule(JDHandler(seen), str(INBOX), recursive=False)
    observer.start()

    try:
        while True:
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
