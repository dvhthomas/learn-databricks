---
title: "Exercises: Delta Lake"
summary: "Write sensor data to Delta format, inspect the transaction log, and see ACID guarantees in action — locally, without Databricks"
weight: 50
type: exercise
---

## Delta writer (Python, local)

This exercise runs locally using the `deltalake` Python package (delta-rs) — no Spark or Databricks needed. You'll write SCADA sensor data to a Delta table, inspect the transaction log, append data, time-travel, and trigger schema enforcement.

```sh
uv run python modules/02-delta-lake/exercises/delta_writer.py
```

The exercise has `# TODO` markers — fill them in before running. The assertions at the end verify your work.

### What you'll do

1. **Write** a batch of sensor readings as a Delta table
2. **Inspect** the `_delta_log/` directory — read the JSON files and understand every field
3. **Append** a second batch and verify the log grew
4. **Time travel** back to version 0 and confirm the original data is intact
5. **Trigger** a schema enforcement error by adding a column that doesn't exist
6. **Evolve** the schema with `schema_mode="merge"` and verify the new column appears

### After running

Open `data/delta/sensors/_delta_log/00000000000000000000.json` in your editor. Read each line. You should be able to explain:
- What `commitInfo` records and why it matters for auditing
- What `metaData` contains and how it relates to schema enforcement
- What `add` means and why it's the key to how readers find data files
- Why there's no `remove` action in version 0 (but there would be after an UPDATE or DELETE)

---

## Storage cost model (CalcMark)

Time travel is one of Delta Lake's best features — until your cloud storage bill arrives. This CalcMark model works through the real numbers: how much does 30-day VACUUM retention actually cost for a 500-turbine wind utility, and when should you change it?

The model covers:
- **Base storage** across Bronze, Silver, and Gold layers
- **Time travel overhead** — why Bronze (append-only) is cheap but Silver (daily MERGE) and Gold (daily overwrite) are not
- **VACUUM retention trade-offs** — 7-day vs. 30-day vs. 90-day, with dollar amounts
- **3-year projection** compounded at 10% annual fleet growth
- **Break-even analysis** — at what ingest rate does storage cross $1K/month?

### Running the model

```sh
# Evaluate and show all computed values
uv run cm eval modules/02-delta-lake/exercises/delta-storage-costs.cm -v

# Export to HTML for a formatted report
uv run cm eval modules/02-delta-lake/exercises/delta-storage-costs.cm --format html > delta-costs.html
```

### What to look for

After running, check these numbers and make sure you can explain them:

1. **The storage multiplier** — 30-day VACUUM retention roughly doubles your storage vs. current-only. Why does Bronze contribute almost nothing to that overhead?
2. **The cost spread** between 7-day and 90-day retention. Is it large enough to matter? (Hint: compare it to a NERC CIP fine.)
3. **Where storage sits** relative to compute costs. Storage is the smaller line item — but it never scales to zero.

Try changing `daily_ingest = 20 GB` and rerunning to see what happens at larger fleet scale.
