# Module 1 Validation: Why Spark Exists

Work through these with your AI agent. Don't look at notes — the goal is to
test what actually stuck, not what you can look up.

---

## Oral questions

Answer these out loud (or in chat). Aim for 2–3 sentences per answer — enough
to show you understand it, not a lecture.

**Must know cold:**

1. What is a shuffle in Spark, and why is it expensive? Give a concrete example
   using sensor data.

2. I have 500GB of sensor data and I want the average temperature per sensor per
   hour. Walk me through what Spark does when I run `groupBy("sensor_id").agg(avg("value"))`.
   Where does the shuffle happen?

3. What's the difference between a Spark transformation and an action? Why does
   this distinction matter when debugging a slow job?

4. Why does Databricks exist? If Apache Spark is open source and free, what are
   customers paying for?

5. I'm a data engineer at a company with 50GB of data growing by 1GB/month. Should
   I use Spark or DuckDB? Justify your answer.

**Know the shape:**

6. What is Photon and how does it relate to Spark? (One sentence is fine.)

7. What's the difference between Spark's DataFrame API and the RDD API? Which
   should you use today?

---

## Code challenge

Upload `exercises/01_spark_vs_duckdb.ipynb` to Databricks Community Edition and
run it. You should be able to:

- [ ] Explain what each cell is doing before running it
- [ ] Find the shuffle stage in the Spark UI after running the `groupBy`
- [ ] Identify which operation triggered execution (the action)
- [ ] Explain why the DuckDB version is faster for this dataset

---

## The interview question

Practice this answer until it's fluent (under 90 seconds):

> "Walk me through what happens when a Spark job runs a groupBy on a 1TB dataset
> across 10 executors."

A good answer covers: data is partitioned across executors → transformations are
lazy → the `groupBy` triggers a shuffle → data is repartitioned by key → aggregation
runs locally on each executor → results are collected.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Code challenge complete and explained
- [ ] Interview question answer is fluent and under 90 seconds
- [ ] Module status updated to `done` in repo README
