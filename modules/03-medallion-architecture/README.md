# Module 3: Medallion Architecture

**Status:** planned  
**Databricks environment:** Community Edition  
**Local code:** yes — `uv run python exercises/medallion.py`

## The question this module answers

You have raw sensor readings landing in Delta Lake. How do you structure them so
that data engineers, analysts, and ML engineers can all work from the same data
without stepping on each other — and so that when something goes wrong, you can
trace and fix it?

## Core concepts

### Bronze → Silver → Gold

```
Bronze   Raw, immutable, append-only. Exactly what arrived. Never modified.
  ↓
Silver   Cleaned, validated, typed, deduplicated. Trustworthy. Stable schema.
  ↓
Gold     Business-ready aggregates. Optimized for reads. Named for the business.
```

**Bronze is sacred.** If you can always reprocess from Bronze, you can fix any
downstream mistake. The moment you modify Bronze, you lose your audit trail.

**Silver is where quality happens.** Bad readings are flagged (not silently dropped),
schema is enforced, units are normalized, late arrivals are handled.

**Gold answers business questions.** Hourly stats, daily summaries, anomaly counts.
If analysts are re-aggregating Gold themselves, Gold is too fine-grained.

### Why three layers?

**Recoverability:** a bug in Silver can be fixed and reprocessed from Bronze.
**Trust:** Silver has a stable, documented schema — downstream teams can depend on it.
**Performance:** Gold is pre-aggregated for the queries that actually run.
**Debuggability:** when a dashboard shows wrong numbers, you can trace back through
Silver to Bronze to find where the problem entered.

### Data quality tracking

Bad data shouldn't be silently dropped — it should be counted and visible. A
production Silver table should be able to answer: "what percentage of our readings
were valid this month, and what were the top failure reasons?"

```python
# Track rejections explicitly
rejected = silver_input.filter(~is_valid)
rejected.write.format("delta").mode("append").save("data/delta/silver_rejected")
```

### Mapping to dbt

If you've seen dbt, this is the same pattern:

| Medallion | dbt |
|---|---|
| Bronze | sources (raw, declared not transformed) |
| Silver | staging + intermediate models |
| Gold | marts |

dbt implements it in SQL on a warehouse. Medallion implements it in Spark/Python
on a lakehouse. Same concept, different execution. Both are valid — knowing both
makes you credible to customers who've already invested in dbt.

## Reading

- [Databricks: Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [dbt project structure guide](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) — read alongside for contrast
- [Building Data Quality into Your Lakehouse](https://www.databricks.com/blog/2022/02/10/building-data-quality-into-your-lakehouse-with-delta-lake.html)

## Hands-on exercise

See [`exercises/`](exercises/) — runs locally with `uv run`.

Restructure your sensor data into three explicit Delta tables.
You write Bronze, Silver, and Gold as separate Python scripts — the manual way —
so you feel exactly what DLT (Module 4) does for you automatically.

## What to write on your blog

Show the same pipeline implemented in medallion (Python + Delta) and in dbt SQL.
The side-by-side makes the trade-offs concrete. Both work — the post is about
how to choose.
