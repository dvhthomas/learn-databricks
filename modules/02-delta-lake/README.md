# Module 2: Delta Lake — ACID on Files

**Status:** planned  
**Databricks environment:** Community Edition (for Spark-based exercises)  
**Local code:** yes — `uv run python exercises/delta_writer.py`

## The question this module answers

Your sensor-analytics Parquet files work fine until they don't: a crashed writer
leaves a partial file, two writers corrupt each other, a schema change breaks every
downstream query. What do you do?

Delta Lake wraps Parquet files in a transaction log that gives you ACID guarantees,
schema enforcement, time travel, and upserts — without changing the file format
or requiring a server.

## Core concepts

### The transaction log is the whole idea

Delta Lake stores data as ordinary Parquet files. The difference is a `_delta_log/`
directory containing JSON files (and periodic Parquet checkpoints) that record
every operation:

```
sensors/
├── _delta_log/
│   ├── 00000000000000000000.json   ← "created table, added file A"
│   ├── 00000000000000000001.json   ← "added files B and C"
│   └── 00000000000000000002.json   ← "deleted bad readings, added corrected file D"
├── part-00000-abc.parquet
└── part-00001-def.parquet
```

Reading a Delta table means: read the log to know which files are current,
then read those files. The log is the source of truth — not the files themselves.

### What ACID means here in practice

- **Atomicity:** a write either fully succeeds or fully fails. No partial files that
  look valid but aren't.
- **Consistency:** schema is enforced at write time. A malformed reading is rejected
  before it lands.
- **Isolation:** readers always see a consistent snapshot. A write in progress doesn't
  affect concurrent reads.
- **Durability:** committed data survives crashes. The log entry is the proof.

### Time travel

Every write creates a new version. You can query any previous state:

```sql
-- What did the data look like at version 3?
SELECT * FROM sensors VERSION AS OF 3

-- What did it look like yesterday?
SELECT * FROM sensors TIMESTAMP AS OF '2024-11-17'
```

Useful for debugging ("what changed between these two runs?"), compliance ("show
me the data as of this date"), and recovery ("oops, undo that bad write").

### Schema enforcement vs. schema evolution

By default, Delta rejects writes that don't match the current schema:

```python
# Fails if "humidity" column doesn't exist in the table schema
df_with_humidity.write.format("delta").save("/data/sensors")

# Succeeds — merges the new column into the schema
df_with_humidity.write.format("delta").option("mergeSchema", "true").save("/data/sensors")
```

This is what makes Silver tables trustworthy. Schema surprises get caught at write
time, not silently corrupted into the table.

### MERGE (upserts)

```sql
MERGE INTO sensors AS target
USING new_readings AS source
ON target.sensor_id = source.sensor_id
   AND target.timestamp = source.timestamp
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

This handles late-arriving data (common in IoT) and corrections without rewriting
the whole table.

## Delta vs. Apache Iceberg

Iceberg does the same job. The technical differences matter less than the ecosystem:

| | Delta Lake | Apache Iceberg |
|---|---|---|
| Primary backer | Databricks | Apache (Netflix, Apple, AWS) |
| Snowflake native? | Limited | Yes |
| AWS Glue native? | Supported | Native |
| Partition evolution | V2 improved | First-class |
| Who uses it | Databricks shops | Snowflake, AWS, cloud-native |

Choosing Delta vs. Iceberg is often a vendor bet, not a purely technical decision.
Knowing both exist and why customers choose each is more useful than deep technical
mastery of either format.

## Reading

- **The log format:** [Delta Protocol spec](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) — read the intro and the log entry format section only
- **Original paper:** [Delta Lake VLDB paper](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf) — intro + architecture sections
- **Databricks docs:** [What is Delta Lake?](https://docs.databricks.com/en/delta/index.html)
- **Neutral comparison:** [Delta vs. Iceberg vs. Hudi](https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison)

## Hands-on exercise

See [`exercises/`](exercises/) — runs locally with `uv run`.

The exercise adds a Delta writer to your sensor data alongside the existing
Parquet approach. You'll inspect the log, test time travel, trigger schema
enforcement, and observe what happens with concurrent writes.

## What to write on your blog

> *"I opened `_delta_log/00000000000000000000.json` so you don't have to."*

Show the actual log file contents and explain each field. Most people treat Delta
Lake as a black box. Showing you understand the mechanism is what separates
"I've read about it" from "I've worked with it."
