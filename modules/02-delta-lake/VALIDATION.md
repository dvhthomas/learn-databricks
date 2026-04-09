# Module 2 Validation: Delta Lake

---

## Oral questions

**Must know cold:**

1. Explain what `_delta_log/` contains and why it exists. Don't say "it's a
   transaction log" — explain mechanically what's in the files and how a reader
   uses them.

2. A writer crashes halfway through writing a batch of sensor readings. What
   happens to the data? How does Delta handle this differently from raw Parquet?

3. What does "time travel" mean in Delta Lake? Give me a scenario where you'd
   actually use it in production.

4. I want to add a `location` column to my sensor readings table. I have new
   data with this column and old data without it. How does Delta handle this?
   What options do I have?

5. What's the difference between Delta Lake and Apache Iceberg? If a customer
   says "we're all-in on AWS," which format would you lean toward and why?

**Know the shape:**

6. What is Z-ordering and when would you use it? (One sentence.)

7. What is a MERGE operation and why is it useful for IoT data?

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
- [ ] Explain what the `--version` flag in `delta-rs` corresponds to in the log

---

## The interview question

Practice until fluent:

> "A customer says their data lake is a mess — files everywhere, no consistency,
> analysts can't trust the data. What do you recommend?"

Good answer: start with diagnosis (is it a format problem, an access problem, a
quality problem?), then propose Delta Lake for the storage layer, explain what
ACID gives them, mention schema enforcement as the "garbage in, garbage out" fix,
and tie it to the medallion architecture (Module 3) as the structural fix.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Log file contents explained correctly
- [ ] Time travel demonstrated
- [ ] Schema enforcement triggered and explained
- [ ] Interview question answer is fluent
- [ ] Module status updated to `done` in repo README
