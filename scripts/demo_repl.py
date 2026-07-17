"""Live proof: the demo farmer reports a harvest through the real orchestrator.

    python -m scripts.demo_repl

Run data.seed first. This is the pre-bot demoable milestone from CLAUDE.md
(Developer A roadmap item 8).
"""
from __future__ import annotations

import json

from core import db
from core.api import process_harvest_report

result = process_harvest_report(
    farmer_id=6, crop="cabai_rawit_merah", region="garut", days_to_harvest=2, quantity_kg=150
)
print(json.dumps(result, indent=2, ensure_ascii=False))

conn = db.get_connection()
pending = conn.execute(
    "SELECT mr.id, f.name, hr.crop, hr.quantity_kg, hr.harvest_date"
    " FROM match_request mr"
    " JOIN harvest_report hr ON hr.id = mr.harvest_report_id"
    " JOIN farmer f ON f.id = hr.farmer_id"
    " WHERE mr.status = 'pending'"
).fetchall()
print(f"\npending matches for anchor buyer: {len(pending)}")
for row in pending:
    print(f"  match #{row['id']}: {row['name']} — {row['quantity_kg']} kg"
          f" {row['crop']}, harvest {row['harvest_date']}")
