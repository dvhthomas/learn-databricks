---
title: "Exercises: Medallion Architecture"
summary: "Build a three-layer pipeline from raw SCADA readings to analyst-ready aggregates — manually — so you feel exactly what DLT automates in Module 4"
weight: 50
type: exercise
---

## Medallion pipeline (Python, local)

This exercise runs locally using the `deltalake` Python package (delta-rs) — no Spark or Databricks needed. You will build a complete Bronze-to-Silver-to-Gold pipeline for wind turbine SCADA data, handling validation, rejection tracking, and aggregation.

```sh
uv run python modules/03-medallion-architecture/exercises/medallion.py
```

The exercise has `# TODO` markers — fill them in before running. The assertions at the end verify your work.

### What you will do

1. **Bronze:** Write raw SCADA readings as a Delta table in append mode. No transformation beyond adding an `ingested_at` timestamp. The 999.9 C reading goes in.
2. **Silver:** Validate readings against range and null checks. Valid readings go to the Silver table. Invalid readings go to `silver_rejected` with a rejection reason. The 999.9 C reading should be caught here.
3. **Gold:** Aggregate validated Silver readings into hourly statistics per sensor — average, max, min, reading count, plus warning and critical counts based on business thresholds.
4. **Reflect:** Read the "What this exercise didn't give you" section at the end. It lists everything you wrote manually that DLT handles automatically. Come back to this list after Module 4.

### What to pay attention to

- **Why does Bronze use `mode="append"`?** Because Bronze is immutable and append-only. You never overwrite Bronze.
- **Why does Gold use `mode="overwrite"`?** Because Gold is derived — it is recomputed from Silver, not accumulated.
- **What happens if you run the script twice?** Bronze and Silver get duplicate rows. Gold gets recomputed (no duplicates because of overwrite). This is the idempotency gap that DLT solves.
- **Where is the 999.9 C reading?** It should be in `silver_rejected`, not in Silver or Gold. If it shows up in Gold, your validation logic has a bug.

### After running

Check the rejection rate output. The sample data has one intentionally bad reading (sensor_0004 at 999.9 C). Your rejection rate should be small but nonzero — that is the signal that quality tracking is working.

Then look at the Gold table output. You should see per-sensor hourly aggregates with warning and critical counts. Sensor_0004 should show warnings (it runs hot, even after the 999.9 reading is rejected).
