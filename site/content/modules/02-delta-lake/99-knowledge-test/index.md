---
title: "Knowledge Test: Delta Lake"
summary: "Validate your understanding of the transaction log, ACID guarantees, schema enforcement, and how Delta compares to Iceberg"
weight: 99
type: test
tags:
  - delta-lake
  - acid
  - transaction-log
  - iceberg
---

## Oral questions

**Must know cold:**

1. Explain what `_delta_log/` contains and why it exists. Don't say "it's a transaction log" — explain mechanically what's in the JSON files and how a reader uses them to assemble the current table.

2. Your SCADA pipeline crashes halfway through writing a batch of turbine readings. What happens to the data? Walk through why a Delta table is fine but a raw Parquet directory would be corrupt.

3. What does "time travel" mean in Delta Lake? Give a scenario at the wind utility where you'd actually use it in production — not just "it's cool."

4. A turbine firmware update adds a new `blade_ice_detection` column to the SCADA data. What happens when the pipeline writes this data to your Delta table? What should you do about it?

5. What's the difference between Delta Lake and Apache Iceberg? If a customer says "our cloud team standardized on Iceberg," what do you tell them about Databricks?

6. Explain what MERGE does and why it matters for IoT data. Use the "sensor recalibration with corrected readings" example.

**Know the shape:**

7. What is Z-ordering and when would you use it? What's replacing it? (Two sentences.)

8. What is UniForm and what problem does it solve? (Two sentences.)

## Code challenge

Run `modules/02-delta-lake/exercises/delta_writer.py`:

```sh
uv run python modules/02-delta-lake/exercises/delta_writer.py
```

You should be able to:

- [ ] Explain what each section of the script does before running it
- [ ] Open `data/delta/sensors/_delta_log/00000000000000000000.json` and explain what you see — what do `add`, `commitInfo`, `metaData` mean?
- [ ] Run the time travel query and explain how Delta knew what data to return
- [ ] Trigger the schema enforcement error and explain why it happened
- [ ] Explain what happens when you use `schema_mode="merge"` — what changed in the log?

## The interview question

Practice until fluent:

> "A customer says their data lake is a mess — files everywhere, no consistency, analysts can't trust the data. The quarterly compliance report doesn't add up. What do you recommend?"

A good answer: start with diagnosis (is it a format problem, an access problem, a quality problem?). Propose Delta Lake for the storage layer — explain what ACID gives them (no more partial writes, consistent reads). Mention schema enforcement as the "garbage in, garbage out" fix. Bring up time travel for auditability. Tie it to the medallion architecture (Module 3) as the structural fix, and Unity Catalog (Module 5) for governance. Be honest: Delta Lake alone doesn't fix bad pipeline logic — it just makes storage reliable.
