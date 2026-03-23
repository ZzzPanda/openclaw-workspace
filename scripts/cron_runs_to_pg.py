#!/usr/bin/env python3
"""
Parse OpenClaw cron job runs from JSONL files and insert into PostgreSQL.
"""
import json
import os
from datetime import datetime

import psycopg2

# Paths
CRON_RUNS_DIR = os.path.expanduser("~/.openclaw/cron/runs")
JOBS_FILE = os.path.expanduser("~/.openclaw/cron/jobs.json")

# PG connect
conn = psycopg2.connect("dbname=postgres user=roger")
cur = conn.cursor()

# Load job metadata (name, delivery)
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

print(f"Loaded {len(job_meta)} job definitions")

# Process each JSONL file
total_inserted = 0
total_skipped = 0

for filename in os.listdir(CRON_RUNS_DIR):
    if not filename.endswith(".jsonl"):
        continue

    job_id = filename.replace(".jsonl", "")
    meta = job_meta.get(job_id, {
        "name": job_id,
        "delivery_target": "",
        "delivery_channel": ""
    })

    filepath = os.path.join(CRON_RUNS_DIR, filename)
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Skip non-finished actions
            if record.get("action") != "finished":
                continue

            run_at_ms = record.get("runAtMs")
            if run_at_ms:
                cur.execute(
                    "SELECT 1 FROM cron_job_runs WHERE job_id = %s AND run_at = to_timestamp(%s / 1000.0)",
                    (job_id, run_at_ms)
                )
                if cur.fetchone():
                    total_skipped += 1
                    continue

            run_at = datetime.fromtimestamp(record["runAtMs"] / 1000) if record.get("runAtMs") else None
            next_run_at = datetime.fromtimestamp(record["nextRunAtMs"] / 1000) if record.get("nextRunAtMs") else None

            # run_log = full JSONL entry
            # message_content = summary (what was sent/delivered)
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
                json.dumps(record),           # full run_log
                record.get("summary"),         # message_content
            ))
            total_inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted: {total_inserted}, Skipped (duplicate): {total_skipped}")
