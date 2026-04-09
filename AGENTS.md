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
If an explanation is getting abstract, pull it back to sensor-analytics.
"How would this change the way your Parquet writer works?" is always a valid anchor.

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

### Module 1: Why Spark Exists
**What to emphasize:** The driver/executor model and the shuffle are the two concepts
that come up constantly in real Databricks conversations. Make sure the learner can explain
both with a concrete example (not just "shuffle moves data between nodes").

**Common misconception to address:** Spark is not always better than single-node tools.
The honest answer is that DuckDB beats Spark for datasets under ~1TB on a single machine.
Understanding *when* to use distributed compute is more valuable than being a Spark
evangelist.

**Must know cold:**
- What a shuffle is and why it's expensive
- The difference between a transformation and an action in Spark
- Why Spark uses lazy evaluation (and what that means for debugging)
- Why Databricks exists on top of Spark (what problems does it solve?)

**Interview question to practice:**
> "Walk me through what happens when a Spark job runs a groupBy on a 1TB dataset
> across 10 executors."

---

### Module 2: Delta Lake
**What to emphasize:** Read the actual `_delta_log/` JSON file together. This is the
single most grounding exercise in the whole curriculum — it turns an abstract concept
into something concrete. Don't skip it.

**Must know cold:**
- What ACID means in this context (not just the acronym — what does "atomicity" mean
  when writing Parquet files?)
- How time travel works mechanically (the log, not magic)
- The difference between Delta and Iceberg at a level beyond "both are open formats"
- Why schema enforcement matters for production pipelines

**Know the shape:**
- Z-ordering and data skipping
- Liquid clustering (newer, replacing Z-ordering)
- Delta Sharing protocol

**Interview question to practice:**
> "A customer says their data lake is a mess — files everywhere, no consistency,
> analysts can't trust the data. What would you recommend and why?"

---

### Module 3: Medallion Architecture
**What to emphasize:** This is vocabulary more than technology. Every Databricks
customer conversation uses Bronze/Silver/Gold. The learner should be able to map any
customer's data problem onto this pattern immediately.

**Common mistake to address:** Gold doesn't mean "small." Gold means "business-ready."
A Gold table can be enormous — it's about the grain and trustworthiness, not the size.

**Must know cold:**
- Why Bronze is immutable and append-only (what breaks if it isn't?)
- The difference between Silver cleaning and Gold aggregating
- How to explain medallion to a non-technical stakeholder in two sentences
- How it maps to dbt's staging/intermediate/marts (same idea, different execution)

**Interview question to practice:**
> "A customer's data team is spending all their time fixing broken dashboards.
> How would you restructure their data pipeline?"

---

### Module 4: Delta Live Tables
**What to emphasize:** The shift from imperative (you write the orchestration)
to declarative (you describe the outcome, the platform handles the rest) is the
core concept. Everything else follows from that.

**The thing most people miss:** DLT's data quality tracking (`@dlt.expect`) is
often *more valuable* to enterprise buyers than the pipeline automation itself.
Being able to say "our Silver table has a 99.7% validity rate this month, and
here's the trend" is what compliance teams want.

**Must know cold:**
- What `@dlt.expect_or_drop` vs. `@dlt.expect_or_fail` vs. `@dlt.expect` each do
- The difference between `dlt.read()` and `dlt.read_stream()` and when to use each
- Why you'd use DLT instead of writing plain Spark transformation code
- When you'd use Airflow/Workflows *with* DLT rather than instead of it

**Know the shape:**
- Enhanced autoscaling in DLT
- DLT with Unity Catalog (lineage through pipelines)

**Interview question to practice:**
> "A customer wants to know when their data pipeline breaks and why. How does
> Databricks help them answer that?"

---

### Module 5: Unity Catalog
**What to emphasize:** Most enterprise Databricks deals now hinge on Unity Catalog.
The conversation is almost never "can Spark run our queries" — it's "can we govern
our data across teams, clouds, and compliance requirements." UC is the answer.

**The migration story matters:** A large portion of existing Databricks customers
are mid-migration from Hive Metastore to Unity Catalog. Understanding the pain of
that migration (and how to minimize it) is practical consulting knowledge.

**Must know cold:**
- The three-level namespace (metastore → catalog → schema → table) and what each level is for
- The difference between Unity Catalog and the legacy Hive Metastore
- What data lineage means and why a data engineering manager cares about it
- Column-level vs. row-level security: when does each apply?

**Know the shape:**
- Delta Sharing through Unity Catalog
- External tables vs. managed tables in UC
- System tables (audit logs, lineage data as queryable tables)

**Interview question to practice:**
> "A healthcare customer says they can't adopt Databricks because they can't prove
> who has access to PHI. How do you respond?"

---

### Module 6: Databricks SQL
**What to emphasize:** DBSQL is where the learner will have the most customer conversations
because it's where SQL analysts live — and SQL analysts are the ones complaining to
their managers that the platform is slow or confusing. Understanding DBSQL from an
analyst's perspective (not an engineer's) is key.

**The Snowflake comparison is unavoidable:** Every DBSQL conversation eventually
becomes "so how does this compare to Snowflake?" the learner needs a nuanced, honest answer —
not a Databricks sales pitch. Snowflake is genuinely better at some things.

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
> "A customer's CFO asks why they should pay for Databricks SQL when they already
> have Snowflake. What do you say?"

---

### Module 7: MLflow and the AI Platform
**What to emphasize:** The learner doesn't need to be a data scientist. They need to
understand the ML *workflow* well enough to advise on it, spot problems, and
connect it to the governance story (which they already understand from Unity Catalog).

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
- Feature Store (what it is, why ML teams need it)
- Vector Search (for RAG applications)
- Model Serving endpoints
- LLM fine-tuning on Databricks

**Interview question to practice:**
> "A customer's data science team says their models keep producing different results
> and they don't know why. What's the root cause and how does Databricks help?"

---

## Final assessment

When all 7 modules are complete, run this assessment before the learner moves on:

### The whiteboard test
Ask the learner to draw the Databricks architecture from memory:
- Where does data land? (object storage + Delta)
- How does it get there? (ingestion: Auto Loader, DLT, Spark)
- How is it structured? (medallion: Bronze/Silver/Gold)
- Who governs it? (Unity Catalog)
- Who queries it? (DBSQL for analysts, notebooks for engineers, Model Serving for apps)
- How is ML tracked? (MLflow)

If the learner can draw this in 3 minutes with reasonable accuracy, they're ready.

### The customer scenario test
Present this scenario without preparation:

> "A retail company has 5 years of transaction data in S3 as CSV files. They have a
> data engineering team of 4, a data science team of 2, and 20 SQL analysts. They're
> currently using Redshift for analytics and a custom Python pipeline for data prep.
> They want to 'modernize their data platform.' What do you recommend and why?"

A good answer covers: migration approach (don't rip and replace), Delta Lake for
storage, medallion for structure, Unity Catalog for governance, DBSQL for the analysts
(their biggest pain), and an honest discussion of whether they need Spark or whether
simpler tools would serve them. It should also mention what *not* to do — over-engineering
is a common failure mode.

### The "why not Snowflake?" test
Ask: "This customer is also evaluating Snowflake. Make the case for Databricks,
then steelman the case for Snowflake."

The learner should be able to do both without prompting.
