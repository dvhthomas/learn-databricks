# Module 2 Validation: Delta Lake

---

## Oral questions

**Must know cold:**

1. Explain what `_delta_log/` contains and why it exists. Don't say "it's
   a transaction log" — explain mechanically what's in the files and how
   a reader uses them.

2. A SCADA pipeline crashes halfway through writing a batch of turbine
   readings. What happens to the data? How does Delta handle this
   differently from raw Parquet?

3. What does "time travel" mean in Delta Lake? Give a scenario at the
   wind utility where you'd actually use it in production.

4. A turbine firmware update adds a `blade_ice_detection` column. What
   happens when the pipeline writes this to your Delta table? What
   should you do?

5. What's the difference between Delta Lake and Apache Iceberg? If a
   customer says "we're standardizing on Iceberg," what do you say?

6. Explain what MERGE does. Use the sensor recalibration example.

**Know the shape:**

7. What is Z-ordering and when would you use it? What's replacing it?

8. What is UniForm and what problem does it solve?

---

## Code challenge

Run `exercises/delta_writer.py` locally:

```sh
uv run python modules/02-delta-lake/exercises/delta_writer.py
```

You should be able to:

- [ ] Explain what each section of the script does before running it
- [ ] Open `data/delta/sensors/_delta_log/00000000000000000000.json` and explain
      what you see (what do `add`, `commitInfo`, `metaData` mean?)
- [ ] Run the time travel query and explain how Delta knew what data to return
- [ ] Trigger the schema enforcement error and explain why it happened
- [ ] Explain what the log looks like after schema evolution with `merge`

---

## The interview question

Practice until fluent:

> "A customer says their data lake is a mess — files everywhere, no consistency,
> analysts can't trust the data. The quarterly report doesn't add up. What do
> you recommend?"

Good answer: start with diagnosis (format, access, or quality problem?),
propose Delta Lake for the storage layer, explain what ACID gives them,
mention schema enforcement as the "garbage in" fix, time travel for
auditability, and tie it to medallion architecture (Module 3) as the
structural fix and Unity Catalog (Module 5) for governance.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Log file contents explained correctly
- [ ] Time travel demonstrated and explained
- [ ] Schema enforcement triggered and explained
- [ ] Interview question answer is fluent
- [ ] Module status updated to `done` in `_index.md` front matter
