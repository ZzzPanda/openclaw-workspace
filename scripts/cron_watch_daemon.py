#!/usr/bin/env python3
"""
Real-time cron run logger: watches OpenClaw JSONL files and writes new entries to PostgreSQL immediately.
Uses fswatch for event-driven monitoring instead of polling.
"""
import json
import os
import sys
import fcntl
import atexit
import signal
from datetime import datetime
from pathlib import Path

import psycopg2

# Paths
CRON_RUNS_DIR = os.path.expanduser("~/.openclaw/cron/runs")
JOBS_FILE = os.path.expanduser("~/.openclaw/cron/jobs.json")
PID_FILE = "/tmp/cron_watch_daemon.pid"
LOG_FILE = "/tmp/cron_watch_daemon.log"

# PG connect
conn = psycopg2.connect("dbname=postgres user=roger")
cur = conn.cursor()

# Load job metadata
with open(JOBS_FILE) as f:
    jobs_data = json.load(f)

job_meta = {}
for job in jobs_data.get("jobs", []):
    job_id = job.get("id", "")
    delivery = job.get("delivery", {})
    job_meta[job_id] = {
        "name": job.get("name", "unknown"),
        "delivery_target": delivery.get("to", ""),
        "delivery_channel": delivery.get("channel", ""),
    }


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def upsert_record(record, job_id):
    """Insert a single finished run, skip if already exists."""
    if record.get("action") != "finished":
        return

    run_at_ms = record.get("runAtMs")
    if not run_at_ms:
        return

    # Check duplicate
    cur.execute(
        "SELECT 1 FROM cron_job_runs WHERE job_id = %s AND run_at = to_timestamp(%s / 1000.0)",
        (job_id, run_at_ms)
    )
    if cur.fetchone():
        return

    meta = job_meta.get(job_id, {
        "name": job_id,
        "delivery_target": "",
        "delivery_channel": ""
    })

    run_at = datetime.fromtimestamp(run_at_ms / 1000) if run_at_ms else None
    next_run_at = datetime.fromtimestamp(record["nextRunAtMs"] / 1000) if record.get("nextRunAtMs") else None

    cur.execute("""
        INSERT INTO cron_job_runs
            (job_id, job_name, delivery_target, delivery_channel, status, error,
             summary, duration_ms, run_at, next_run_at, run_log, message_content)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        job_id,
        meta["name"],
        meta["delivery_target"],
        meta["delivery_channel"],
        record.get("status", "unknown"),
        record.get("error"),
        record.get("summary"),
        record.get("durationMs"),
        run_at,
        next_run_at,
        json.dumps(record),
        record.get("summary"),
    ))
    conn.commit()
    log(f"✅ Inserted: {meta['name']} | {record.get('status')} | run_at={run_at}")


# Track file positions (inode -> offset)
file_positions = {}

def process_file(filepath):
    """Read only new lines from a file since last read."""
    try:
        stat = os.stat(filepath)
        inode = (stat.st_dev, stat.st_ino)
    except FileNotFoundError:
        return

    current_pos = file_positions.get(inode, 0)

    try:
        with open(filepath, "r") as f:
            # Seek to last known position
            f.seek(current_pos)
            new_lines = f.readlines()
            if not new_lines:
                return
            # Update position
            new_pos = f.tell()
            file_positions[inode] = new_pos

            job_id = Path(filepath).stem  # filename without .jsonl
            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    upsert_record(record, job_id)
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        log(f"❌ Error reading {filepath}: {e}")


def signal_handler(sig, frame):
    log("Shutting down watcher...")
    conn.close()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Ensure single instance
    with open(PID_FILE, "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        f.write(str(os.getpid()))
    atexit.register(lambda: os.unlink(PID_FILE) if os.path.exists(PID_FILE) else None)

    # Seed initial positions (read all existing content, don't re-insert)
    log("Seeding file positions...")
    for filename in os.listdir(CRON_RUNS_DIR):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(CRON_RUNS_DIR, filename)
            try:
                stat = os.stat(filepath)
                inode = (stat.st_dev, stat.st_ino)
                with open(filepath, "r") as f:
                    f.seek(0, 2)  # EOF
                    file_positions[inode] = f.tell()
            except Exception:
                pass

    log(f"Watching {CRON_RUNS_DIR} for changes...")

    import subprocess
    proc = subprocess.Popen(
        ["/usr/local/bin/fswatch", "-r", "-o", CRON_RUNS_DIR],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in proc.stdout:
        # fswatch prints the changed file path
        filepath = line.strip()
        if filepath.endswith(".jsonl"):
            process_file(filepath)

    proc.wait()
