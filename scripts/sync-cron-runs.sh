#!/bin/bash
# Sync new OpenClaw cron runs to PostgreSQL
# Run via: python3 ~/.openclaw/workspace/scripts/cron_runs_to_pg.py

python3 ~/.openclaw/workspace/scripts/cron_runs_to_pg.py 2>&1 | tail -1
