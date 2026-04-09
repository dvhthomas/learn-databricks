"""
Module 2: Delta Lake hands-on exercise.

Runs locally — no Databricks needed.
Uses the `deltalake` package (delta-rs), which is Delta without Spark.

    uv run python modules/02-delta-lake/exercises/delta_writer.py

Work through each section. The TODOs are where you fill in the logic.
The assertions at the end tell you if you got it right.
"""

import json
import shutil
from pathlib import Path

import pandas as pd
from deltalake import DeltaTable
from rich.console import Console
from rich.panel import Panel

console = Console()
DATA_DIR = Path("data/delta/sensors")


def load_sample_data() -> pd.DataFrame:
    """Load the committed sample data."""
    raw = pd.read_json("data/sample.json")
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    return raw


def section(title: str) -> None:
    console.print(Panel(f"[bold]{title}[/bold]", expand=False))


# ---------------------------------------------------------------------------
# Section 1: Write sensor readings as a Delta table
# ---------------------------------------------------------------------------

section("1. Writing to Delta Lake")

# Clean up any previous run
if DATA_DIR.exists():
    shutil.rmtree(DATA_DIR)

readings = load_sample_data()
console.print(f"Loaded {len(readings)} readings")

# TODO: Write `readings` as a Delta table to DATA_DIR
# Use write_deltalake() from the deltalake package
# Mode should be "overwrite" for the first write


console.print(f"Delta table written to {DATA_DIR}")

# ---------------------------------------------------------------------------
# Section 2: Inspect the transaction log
# ---------------------------------------------------------------------------

section("2. Reading the transaction log")

log_dir = DATA_DIR / "_delta_log"
log_files = sorted(log_dir.glob("*.json"))

console.print(f"Log files: {[f.name for f in log_files]}")

# TODO: Read and print the first log file (00000000000000000000.json)
# Parse it as JSON (each line is a separate JSON object)
# Print each entry with its key so you can see the structure

first_log = log_files[0]
with open(first_log) as f:
    for line in f:
        entry = json.loads(line)
        # TODO: print the entry keys and a summary of what each one means

# Questions to answer in comments:
# - What does "commitInfo" tell you?
# - What does "metaData" contain?
# - What does "add" record?


# ---------------------------------------------------------------------------
# Section 3: Add more data (version 2)
# ---------------------------------------------------------------------------

section("3. Appending a second batch")

# New hour of readings — slightly different values
new_readings = load_sample_data().copy()
new_readings["timestamp"] = new_readings["timestamp"] + pd.Timedelta(hours=1)
new_readings["value"] = new_readings["value"] + 1.0

# TODO: Append new_readings to the existing Delta table
# Mode should be "append", not "overwrite"


# Verify we now have more rows
dt = DeltaTable(str(DATA_DIR))
total = dt.to_pandas()
console.print(f"Total rows after append: {len(total)} (expected ~40)")
assert len(total) > 20, "Expected more rows after append"

# Check the log — there should be a second file now
log_files = sorted(log_dir.glob("*.json"))
console.print(f"Log files now: {[f.name for f in log_files]}")
assert len(log_files) == 2, "Expected two log entries after two writes"

# ---------------------------------------------------------------------------
# Section 4: Time travel
# ---------------------------------------------------------------------------

section("4. Time travel")

# TODO: Query the Delta table at version 0 (before the append)
# Use DeltaTable with the `version` parameter, then call .to_pandas()

# version_0_df = DeltaTable(str(DATA_DIR), version=0).to_pandas()

# TODO: assert that version 0 has fewer rows than the current table

console.print("Time travel to version 0: ✓")

# ---------------------------------------------------------------------------
# Section 5: Schema enforcement
# ---------------------------------------------------------------------------

section("5. Schema enforcement")

# Create a DataFrame with an extra column that doesn't exist in the table
bad_readings = load_sample_data().copy()
bad_readings["humidity"] = 55.0  # new column not in schema

schema_error_raised = False
try:
    # TODO: Try to write bad_readings to the Delta table in append mode
    # This should raise an error because of the schema mismatch
    pass
except Exception as e:
    schema_error_raised = True
    console.print(f"[green]Schema enforcement caught: {type(e).__name__}[/green]")
    console.print(f"Message: {e}")

assert schema_error_raised, "Expected schema enforcement to reject the write"

# Now try again with schema evolution enabled
# TODO: Write bad_readings with schema_mode="merge" to allow the new column
# After this write, the table schema should include "humidity"


dt_after_evolve = DeltaTable(str(DATA_DIR))
assert "humidity" in dt_after_evolve.schema().to_pandas().columns.tolist() or \
       "humidity" in [f.name for f in dt_after_evolve.schema().fields], \
       "Expected humidity column after schema evolution"

console.print("[green]Schema evolution with merge: ✓[/green]")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

section("Summary")

dt_final = DeltaTable(str(DATA_DIR))
console.print(f"Final table version: {dt_final.version()}")
console.print(f"Final row count: {len(dt_final.to_pandas())}")
console.print(f"Log files: {len(list(log_dir.glob('*.json')))}")

console.print("\n[bold]Questions to answer before validation:[/bold]")
console.print("1. What is in each log file? What does each JSON key mean?")
console.print("2. How does time travel work mechanically? (Hint: it's all in the log)")
console.print("3. Why did the schema enforcement fail, and what exactly changed when you used merge?")
console.print("4. At what point was data actually written to Parquet files?")
