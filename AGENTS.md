# Agent Instructions: learn-databricks

## Purpose and context

The learner is building deep, practical knowledge of the data-platform industry:
Databricks, Snowflake, dbt Labs, and similar. The goal is
**industry-ready knowledge** — credible, practical, and demonstrable — not academic
understanding.

The target is being able to:
1. Have a fluent technical conversation with a Databricks engineer or architect
2. Advise a customer on platform choices and trade-offs with genuine authority
3. Demonstrate hands-on familiarity: "I've built with this, here's what I found"
4. Understand the competitive landscape well enough to discuss it without notes

**This is not a tutorial repo.** Each module produces working code and tested
understanding, not just reading notes.

---

## How to use this repo as an agent

When the learner asks you to work on a module:

1. **Read** `modules/NN-name/README.md` for the conceptual content
2. **Read** `modules/NN-name/VALIDATION.md` for the success criteria
3. **Check** `modules/NN-name/exercises/` for starter code with `# TODO` markers
4. **Work through** the exercises with the learner, filling in TODOs together
5. **Run validation** at the end using the protocol in VALIDATION.md

When the learner says "validate module N" or "am I done with module N":
- Work through every item in VALIDATION.md's **Oral Questions** section
- Ask the questions one at a time, wait for the learner's answer, give honest feedback
- Run or review the **Code Challenges** together
- Only mark the module done if the learner can answer the Oral Questions without
  significant prompting AND the code challenges run correctly

---

## General agent principles for this project

### Keep it practical
If an explanation is getting abstract, pull it back to the wind utility scenario.
"How would this affect the SCADA pipeline for 500 turbines?" is always a valid anchor.
sensor-analytics is the starting point; the wind utility is where it has to work for real.

### Contrast is how understanding deepens
Every concept has a contrast (DuckDB vs. Spark, Delta vs. Iceberg, DLT vs. Airflow,
Databricks vs. Snowflake). Always surface these. Job interviewers at Databricks
will ask "why not Snowflake?" — the learner needs fluent answers.

### Be honest about what matters for the role
Not everything needs deep mastery. Flag when something is:
- **Must know cold** — will definitely come up in interviews and customer conversations
- **Know the shape** — understand the concept, know where to look for details
- **Aware of** — know it exists and roughly what it does

These are called out per-module in VALIDATION.md.

### Run code, don't just describe it
Whenever possible, write and run actual code. Seeing Delta Lake's `_delta_log/`
directory after writing data is worth more than reading three paragraphs about it.

### Populate exercises when asked
If the learner asks you to "set up module N" or "populate the exercises for module N",
fill in the `# TODO` sections in the exercise files with working, idiomatic code.
Use `uv` for dependency management, never `pip`. Code should follow the preferences
in this repo: readable over clever, clear state management, limited side effects.

---

## Module-by-module agent guide

All modules use a **wind utility scenario** as the through-line: a regional operator
with 500 turbines across 3 states, 50+ SCADA sensors per turbine, 15 analysts,
a data science team, and NERC CIP compliance requirements. The starting point is
[sensor-analytics](https://github.com/dvhthomas/sensor-analytics) — a toy pipeline
that works on one machine — and each module addresses what breaks as you scale it
to production.

### Module 1: Why Spark Exists
**What to emphasize:** The full production infrastructure landscape — not just Spark.
Start from sensor-analytics and walk through what breaks first: Redis loses data
(→ Kafka), local Parquet can't be shared (→ object storage + Delta), no governance
(→ Unity Catalog), no concurrent access (→ DBSQL). Spark is one component in this
picture, not the whole story.

The driver/executor model and the shuffle are the two Spark-specific concepts that
come up constantly. Make sure the learner can explain both with a concrete wind
utility example.

**Common misconception to address:** The wind utility's SCADA data (a few GB/day)
doesn't need Spark for volume. What drives platform adoption is governance, concurrent
access, streaming + batch, and ML lifecycle — not data size.

**Must know cold:**
- What breaks when sensor-analytics scales to 500 turbines (and which component fixes each problem)
- What a shuffle is and why it's expensive (use the SCADA + weather join example)
- The difference between a transformation and an action in Spark
- Why Databricks exists on top of Spark (governance, collaboration, managed infrastructure)
- When DuckDB is genuinely better than Spark (and when it's not enough)

**Know the shape:**
- What Kafka does and why it replaces Redis for production IoT
- What Spark Connect is (Spark 4.0, thin client, no JVM)
- What Photon's vectorized shuffle does

**Interview question to practice:**
> "Walk me through what happens when a Spark job runs a groupBy on a 1TB dataset
> across 10 executors."

---

### Module 2: Delta Lake
**What to emphasize:** Read the actual `_delta_log/` JSON file together. This is the
single most grounding exercise in the whole curriculum — it turns an abstract concept
into something concrete. Don't skip it.

**Wind utility anchor:** Two pipelines (SCADA ingestion and weather backfill) write to
the same directory. A writer crashes mid-batch. An analyst queries during a write. What
happens with raw Parquet vs. Delta? Make it concrete with the turbine data.

**Must know cold:**
- What ACID means in this context (not just the acronym — what does "atomicity" mean
  when writing turbine telemetry files?)
- How time travel works mechanically (the log, not magic)
- The difference between Delta and Iceberg (especially relevant since Databricks
  acquired Tabular in 2024 and is working on UniForm interoperability)
- Why schema enforcement matters when a SCADA sensor starts sending new fields

**Know the shape:**
- Z-ordering and data skipping
- Liquid clustering (newer, replacing Z-ordering)
- Delta Sharing protocol

**Interview question to practice:**
> "Your wind utility's data lake is a mess — files everywhere, no consistency,
> the compliance team can't trust the quarterly report. What do you recommend?"

---

### Module 3: Medallion Architecture
**What to emphasize:** This is vocabulary more than technology. Every Databricks
customer conversation uses Bronze/Silver/Gold. The learner should be able to map any
customer's data problem onto this pattern immediately.

**Wind utility anchor:** Field engineers want raw 10-minute SCADA readings. Analysts
want hourly aggregates with outliers removed. Compliance wants an immutable record of
everything — even the bad readings. How do you serve all three from one copy of the data?

**Common mistake to address:** Gold doesn't mean "small." Gold means "business-ready."
A Gold table with all 500 turbines' monthly capacity factors is still huge — it's about
the grain and trustworthiness, not the size.

**Must know cold:**
- Why Bronze is immutable and append-only (what breaks if you modify turbine readings after the fact?)
- The difference between Silver cleaning and Gold aggregating (use the SCADA → temperature averages example)
- How to explain medallion to a non-technical stakeholder in two sentences
- How it maps to dbt's staging/intermediate/marts (same idea, different execution)

**Interview question to practice:**
> "Your wind utility's analysts spend most of their time fixing broken dashboards.
> How would you restructure the data pipeline?"

---

### Module 4: Delta Live Tables (Lakeflow Declarative Pipelines)
**What to emphasize:** The shift from imperative (you write the orchestration)
to declarative (you describe the outcome, the platform handles the rest) is the
core concept. Everything else follows from that.

**Wind utility anchor:** The medallion pipeline from Module 3 breaks at 3am because
a weather station sent malformed JSON. Nobody knows which step failed, what data was
affected, or whether Silver is now inconsistent. DLT fixes this by making the pipeline
declarative and tracking data quality automatically.

**Naming transition:** DLT was rebranded to Lakeflow Spark Declarative Pipelines in 2025.
The `import dlt` API still works but is being replaced by `from pyspark import pipelines`.
Teach the concepts (which are stable) and flag the API transition.

**The thing most people miss:** Data quality tracking (`@dlt.expect`) is often *more
valuable* to enterprise buyers than the pipeline automation. Telling a NERC auditor
"our Silver turbine data has a 99.7% validity rate this month" is what compliance wants.

**Must know cold:**
- What `@dlt.expect_or_drop` vs. `@dlt.expect_or_fail` vs. `@dlt.expect` each do
- The difference between `dlt.read()` and `dlt.read_stream()` and when to use each
- Why you'd use DLT instead of writing plain Spark transformation code
- When you'd use Airflow/Workflows *with* DLT rather than instead of it

**Know the shape:**
- The DLT → Lakeflow Declarative Pipelines rename and API migration
- Enhanced autoscaling in DLT
- DLT with Unity Catalog (lineage through pipelines)

**Interview question to practice:**
> "Your wind utility's SCADA pipeline breaks at 3am. How does Databricks help you
> detect the failure, understand the impact, and recover automatically?"

---

### Module 5: Unity Catalog
**What to emphasize:** Most enterprise Databricks deals now hinge on Unity Catalog.
The conversation is almost never "can Spark run our queries" — it's "can we govern
our data across teams, clouds, and compliance requirements." UC is the answer.

**Wind utility anchor:** NERC CIP auditors ask three questions: (1) Who has access
to CEII data? (2) What is the lineage of your compliance reports? (3) What changed
and when? sensor-analytics can't answer any of these. Unity Catalog can.

**The migration story matters:** A large portion of existing Databricks customers
are mid-migration from Hive Metastore to Unity Catalog. Understanding the pain of
that migration (and how to minimize it) is practical consulting knowledge.

**Must know cold:**
- The three-level namespace (catalog → schema → table) and what each level is for
- The difference between Unity Catalog and the legacy Hive Metastore
- What data lineage means and why a NERC compliance officer cares about it
- Column-level vs. row-level security: when does each apply? (e.g., hiding specific
  turbine locations that are CEII while allowing access to aggregated fleet data)

**Know the shape:**
- Delta Sharing through Unity Catalog
- External tables vs. managed tables in UC
- System tables (audit logs, lineage data as queryable tables)

**Interview question to practice:**
> "A wind utility says they can't adopt Databricks because NERC requires them to
> prove who has access to CEII. How do you respond?"

---

### Module 6: Databricks SQL
**What to emphasize:** DBSQL is where the learner will have the most customer conversations
because it's where SQL analysts live — and SQL analysts are the ones complaining to
their managers that the platform is slow or confusing. Understanding DBSQL from an
analyst's perspective (not an engineer's) is key.

**Wind utility anchor:** 15 analysts each have their own CSV extracts. The fleet
capacity factor shows up differently in every meeting. The CFO is losing confidence
in the data. DBSQL gives everyone governed access to the same Gold tables.

**The Snowflake comparison is unavoidable:** Every DBSQL conversation eventually
becomes "so how does this compare to Snowflake?" The learner needs a nuanced, honest
answer — not a Databricks sales pitch. Snowflake is genuinely better at some things
(mature SQL interface, simpler concurrency scaling, deeper SQL tool ecosystem).

**Must know cold:**
- What a SQL warehouse is and how it differs from a Spark cluster
- Why Photon exists and what it changes (vectorized execution, not just "faster")
- The honest Databricks vs. Snowflake comparison for SQL analytics workloads
- What "serverless" means in this context (vs. "pro" or "classic" warehouses)

**Know the shape:**
- Query history and performance monitoring in DBSQL
- Result caching
- BI tool connectivity (JDBC/ODBC, Partner Connect)

**Interview question to practice:**
> "Your wind utility's CFO asks why they should pay for Databricks SQL when they
> already have Snowflake for their retail division. What do you say?"

---

### Module 7: MLflow and the AI Platform
**What to emphasize:** The learner doesn't need to be a data scientist. They need to
understand the ML *workflow* well enough to advise on it, spot problems, and
connect it to the governance story (which they already understand from Unity Catalog).

**Wind utility anchor:** The vibration model predicted bearing failure in the notebook
(94% recall). In production it missed 3 failures and flagged 200 false alarms. The team
can't explain what changed — which model version is running, what training data it used,
whether input distributions shifted. MLflow solves this.

**The AI pivot framing:** Databricks is repositioning from "data platform" to
"AI platform." The thesis is: your AI needs your data; your data is governed in
Databricks; therefore Databricks is where your AI should live. Understanding this
argument — and its weaknesses — is important for senior roles.

**Must know cold:**
- What MLflow tracks and why that matters for reproducibility
- The model lifecycle: experiment → registered model → staging → production
- Why the Databricks AI platform pitch is coherent (and where it's weaker)
- The Mosaic AI vs. Snowflake Cortex comparison at a high level

**Know the shape:**
- Feature Store (what it is, why ML teams need it for predictive maintenance)
- Vector Search (for RAG applications)
- Model Serving endpoints
- LLM fine-tuning on Databricks

**Interview question to practice:**
> "Your wind utility's vibration model keeps producing different results in production
> vs. the notebook. What's the root cause and how does Databricks help?"

---

## Final assessment

When all 7 modules are complete, run this assessment before the learner moves on:

### The whiteboard test
Ask the learner to draw the wind utility's full data platform from memory:
- Where does data come from? (SCADA → Kafka/Event Hubs)
- Where does it land? (object storage + Delta Lake)
- How does it get there? (Auto Loader, Structured Streaming, DLT pipelines)
- How is it structured? (medallion: Bronze/Silver/Gold)
- Who governs it? (Unity Catalog — CEII access, lineage, audit)
- Who queries it? (DBSQL for analysts, notebooks for engineers, Model Serving for alerts)
- How is ML tracked? (MLflow — vibration model lifecycle)

If the learner can draw this in 3 minutes with reasonable accuracy, they're ready.

### The customer scenario test
Present this scenario without preparation:

> "A solar farm operator has 3 years of inverter telemetry in S3 as CSV files. They
> have a data engineering team of 3, a data science team of 2, and 12 SQL analysts.
> They're currently using Redshift for analytics and cron jobs running Python scripts
> for data prep. They want to 'modernize their data platform.' What do you recommend?"

A good answer covers: migration approach (don't rip and replace), Delta Lake for
storage, medallion for structure, Unity Catalog for governance, DBSQL for the analysts
(their biggest pain), and an honest discussion of whether they need Spark or whether
DuckDB + dbt would serve them at their scale. It should mention what *not* to do —
over-engineering a 3-person team with a full Databricks deployment when simpler tools
would work is a common failure mode.

### The "why not Snowflake?" test
Ask: "This customer is also evaluating Snowflake. Make the case for Databricks,
then steelman the case for Snowflake."

The learner should be able to do both without prompting.
