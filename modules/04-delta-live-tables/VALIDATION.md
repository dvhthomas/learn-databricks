# Module 4 Validation: Delta Live Tables

---

## Oral questions

**Must know cold:**

1. What is the difference between a DLT pipeline and a Spark script that does
   the same transformations? What does DLT handle that you'd otherwise write yourself?

2. Explain the three `@dlt.expect` variants. When would you use each one?
   Give a sensor-analytics example for each.

3. What is the difference between `dlt.read_stream()` and `dlt.read()`?
   In the Bronze → Silver → Gold pipeline, which uses which and why?

4. A customer asks: "Should we use DLT or dbt for our transformations?"
   What questions do you ask before answering?

5. Where does Airflow fit in a Databricks architecture that uses DLT?
   Are they competing or complementary?

**Know the shape:**

6. What does DLT's data quality dashboard show that you couldn't easily get from
   raw Spark code?

7. What is Enhanced Autoscaling in DLT? (One sentence — know it exists and why.)

---

## Code challenge

Upload `exercises/04_dlt_pipeline.py` to Databricks and run it as a DLT pipeline.

You should be able to:

- [ ] Create a DLT pipeline in the Databricks UI and attach the notebook
- [ ] Run the pipeline and have it complete successfully
- [ ] Find the data quality dashboard and identify which rows were rejected
- [ ] Introduce a reading with value=999 and confirm it's tracked in quality metrics
- [ ] Explain the lineage graph shown in the pipeline UI

---

## The interview question

Practice until fluent:

> "A customer wants to know when their data pipeline breaks and why. They're
> currently running a set of Python scripts on a schedule with no monitoring.
> How does Databricks help?"

Good answer: DLT handles retries and tracks failures automatically, quality
expectations produce auditable metrics, the pipeline lineage graph shows what
depends on what, Databricks alerts can notify on pipeline failures. The key insight:
the customer doesn't just want to know *that* it broke — they want to know *where*
in the pipeline and *why*, which is what DLT's observability gives you.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] DLT pipeline running in Databricks
- [ ] Quality metrics demonstrated with a deliberately bad reading
- [ ] Module 3 and Module 4 code compared side-by-side
- [ ] Module status updated to `done` in repo README
