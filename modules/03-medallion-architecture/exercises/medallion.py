"""
Module 3: Medallion Architecture hands-on exercise.

Implements Bronze → Silver → Gold manually using deltalake and pandas.
The point of doing it manually is to feel exactly what DLT (Module 4) automates.

    uv run python modules/03-medallion-architecture/exercises/medallion.py
"""

import shutil
from pathlib import Path

import pandas as pd
from deltalake import DeltaTable, write_deltalake
from rich.console import Console
from rich.panel import Panel

console = Console()

BRONZE_PATH = Path("data/delta/bronze")
SILVER_PATH = Path("data/delta/silver")
SILVER_REJECTED_PATH = Path("data/delta/silver_rejected")
GOLD_PATH = Path("data/delta/gold")


def reset() -> None:
    """Remove all Delta tables from a previous run."""
    for path in [BRONZE_PATH, SILVER_PATH, SILVER_REJECTED_PATH, GOLD_PATH]:
        if path.exists():
            shutil.rmtree(path)


def section(title: str) -> None:
    console.print(Panel(f"[bold]{title}[/bold]", expand=False))


# ---------------------------------------------------------------------------
# Bronze: raw, unmodified, append-only
# ---------------------------------------------------------------------------

section("Bronze: raw ingestion")

reset()

raw = pd.read_json("data/sample.json")
raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
raw["ingested_at"] = pd.Timestamp.now(tz="UTC")

# TODO: Write raw to BRONZE_PATH as a Delta table
# Mode: "append" (Bronze is always append — never overwrite)
# Bronze stores exactly what arrived: no filtering, no transformation


bronze_dt = DeltaTable(str(BRONZE_PATH))
console.print(f"Bronze rows: {len(bronze_dt.to_pandas())}")
console.print(f"Bronze schema: {[f.name for f in bronze_dt.schema().fields]}")

# ---------------------------------------------------------------------------
# Silver: validated, cleaned, typed
# ---------------------------------------------------------------------------

section("Silver: validation and cleaning")

bronze_df = DeltaTable(str(BRONZE_PATH)).to_pandas()

# TODO: Define a validity mask for good readings
# Valid if: value is between -50 and 100, sensor_id is not null, timestamp is not null
# is_valid = ...

# TODO: Separate valid and invalid readings
# valid_df = bronze_df[is_valid].copy()
# rejected_df = bronze_df[~is_valid].copy()

# TODO: On valid readings:
# - Add a "processed_at" column with current timestamp
# - Rename or normalize any columns if needed
# For this exercise, the data is already clean except for the outlier we planted

# TODO: Write valid readings to SILVER_PATH (mode="append")
# TODO: Write rejected readings to SILVER_REJECTED_PATH (mode="append")
# Include a "rejection_reason" column in the rejected table


silver_dt = DeltaTable(str(SILVER_PATH))
rejected_dt = DeltaTable(str(SILVER_REJECTED_PATH))

silver_count = len(silver_dt.to_pandas())
rejected_count = len(rejected_dt.to_pandas())

console.print(f"Silver rows (valid): {silver_count}")
console.print(f"Rejected rows: {rejected_count}")
console.print(f"Rejection rate: {rejected_count / (silver_count + rejected_count):.1%}")

# The sample data has one reading with value=999.9 — it should be rejected
assert rejected_count >= 1, "Expected at least one rejected reading (value=999.9)"

# ---------------------------------------------------------------------------
# Gold: business-ready aggregates
# ---------------------------------------------------------------------------

section("Gold: hourly aggregates")

silver_df = DeltaTable(str(SILVER_PATH)).to_pandas()

# TODO: Compute hourly statistics per sensor
# Group by sensor_id and hour (truncate timestamp to hour)
# Aggregate: avg_temp_c, max_temp_c, min_temp_c, reading_count
# Also add: warning_count (readings > 35°C), critical_count (readings > 40°C)

# Hint: use pd.Grouper or timestamp flooring for the hour
# silver_df["hour"] = silver_df["timestamp"].dt.floor("h")

# gold_df = silver_df.groupby(...).agg(...).reset_index()

# TODO: Write gold_df to GOLD_PATH (mode="overwrite" — Gold is recomputed, not appended)


gold_dt = DeltaTable(str(GOLD_PATH))
gold_df = gold_dt.to_pandas()

console.print(f"Gold rows: {len(gold_df)}")
console.print(gold_df.to_string())

# ---------------------------------------------------------------------------
# Reflection: what DLT does for you
# ---------------------------------------------------------------------------

section("What this exercise didn't give you")

console.print("""
Things you wrote manually that DLT handles automatically:
  - Dependency ordering (Bronze must complete before Silver runs)
  - Incremental processing (only process new Bronze rows, not all of them)
  - Retry logic (what if the Silver write fails halfway?)
  - Quality metrics dashboard (rejection rate over time, not just right now)
  - Lineage tracking (which Gold rows came from which Bronze rows?)
  - Re-running without duplicates (idempotency)

That's Module 4. Come back to this script after Module 4 and notice
how much smaller the DLT version is.
""")
