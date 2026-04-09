---
title: "Knowledge Test: Delta Live Tables"
summary: "Validate your understanding of declarative pipelines, data quality expectations, the DLT execution model, and how DLT compares to Airflow and dbt"
weight: 99
type: test
tags:
  - dlt
  - declarative-pipelines
  - data-quality
  - expectations
  - validation
---

## Oral questions

**Must know cold:**

1. What is the difference between a DLT pipeline and a set of Spark scripts that do the same transformations? Do not just say "declarative vs. imperative" -- explain specifically what DLT handles that you would otherwise write yourself (dependency resolution, incremental state, quality metrics, failure isolation).

2. Explain the three `@dlt.expect` variants. For each one, give a specific wind utility SCADA example of when you would use it. Why would you choose `expect_or_drop` for a temperature of 999.9 but `expect_or_fail` for a timestamp in the year 2030?

3. What is the difference between `dlt.read_stream()` and `dlt.read()`? In the Bronze-Silver-Gold pipeline, which table uses which and why? What would go wrong if Gold used `read_stream` instead of `read`?

4. A customer asks: "Should we use DLT or dbt for our transformations?" What questions do you ask before answering? Give at least three questions and explain why each one matters for the recommendation.

5. Where does Airflow fit in a Databricks architecture that uses DLT? Are they competing or complementary? Draw the picture: what does Airflow trigger, and what does DLT handle within that trigger?

6. Your wind utility's SCADA pipeline breaks at 3am because a weather station sent malformed JSON. Walk through what happens with a hand-coded pipeline vs. a DLT pipeline. Specifically: does Gold consume stale data? Can you tell the compliance team what was affected? How long does recovery take?

**Know the shape:**

7. What is Enhanced Autoscaling in DLT? How does it differ from standard Databricks cluster autoscaling? (Two sentences.)

8. What happened to the "Delta Live Tables" name? What are the three names this product now has, and what is the significance of the open-source contribution to Apache Spark?

9. What does it mean that DLT expectations can now be stored in Unity Catalog tables? Why would a data quality team care about this? (Two sentences.)

## Code challenge

Upload `modules/04-delta-live-tables/exercises/04_dlt_pipeline.py` to Databricks and run it as a DLT pipeline.

You should be able to:

- [ ] Fill in all `# TODO` markers in the notebook before running
- [ ] Create a DLT pipeline in the Databricks UI and attach the notebook
- [ ] Run the pipeline and have it complete successfully (all three tables populated)
- [ ] Find the data quality dashboard and identify how many rows were dropped by `valid_temperature`
- [ ] Explain the lineage graph shown in the pipeline UI -- why does Gold depend on Silver?
- [ ] Introduce a reading with `value=999.9` in a new batch and confirm it appears in the quality metrics
- [ ] Add an `@dlt.expect_or_fail` expectation with a future timestamp and watch the pipeline halt
- [ ] Compare line counts: how many lines of code did you delete vs. Module 3's imperative version?

## The interview question

Practice until fluent:

> "Your wind utility's SCADA pipeline breaks at 3am. How does Databricks help you detect the failure, understand the impact, and recover automatically?"

A strong answer covers:

1. **Detection:** DLT pipelines track every step's success or failure. Databricks Workflows or alerts can notify on failure immediately -- not hours later when an analyst notices bad numbers.

2. **Impact assessment:** DLT's dependency graph shows exactly which downstream tables are affected. The quality dashboard shows how many rows were impacted. Unity Catalog lineage (Module 5) extends this to dashboards and reports that consumed the data.

3. **Recovery:** DLT handles incremental state. Re-running the pipeline processes only the data that was not yet committed. There is no manual "figure out where we left off" step. For `expect_or_fail` scenarios, the pipeline halts cleanly with a specific error -- no partial state to clean up.

4. **Prevention:** Quality expectations catch data problems before they propagate. The 3am failure might have been prevented entirely if `expect_or_fail` had caught the malformed JSON at Bronze, before Silver even attempted to process it.

The key insight: the value is not just that DLT detects the failure -- it is that DLT prevents the downstream cascade. Gold never sees stale Silver data because DLT understands the dependency graph. That is the structural difference from running independent cron jobs.
