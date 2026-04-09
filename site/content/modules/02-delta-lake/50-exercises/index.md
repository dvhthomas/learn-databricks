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
