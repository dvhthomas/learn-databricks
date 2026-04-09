# Module 6 Validation: Databricks SQL

---

## Oral questions

**Must know cold:**

1. What is a SQL warehouse? How does it differ from a Spark cluster?
   Why would an analyst use one instead of a notebook?

2. What is Photon and what does it change about how queries execute?
   Explain it without using the words "vectorized" or "columnar" — use an analogy.

3. A customer's CFO asks why they should pay for Databricks SQL when they already
   have Snowflake. Make the case for Databricks. Now steelman Snowflake's position.

4. What is the difference between Z-ordering and Liquid clustering? Which would
   you recommend for a new table today and why?

5. An analyst complains that their DBSQL dashboard is slow. Walk me through the
   first three things you'd check.

**Know the shape:**

6. What is result caching in DBSQL? What's the catch — when does it not help?

7. How does a BI tool like Tableau connect to Databricks SQL? What does the
   analyst need to set up?

8. What is Delta Sharing? How is it different from just granting SELECT on a table?

---

## Code challenge

Complete `exercises/06_dbsql_queries.sql` in the Databricks SQL editor.

You should be able to:

- [ ] Run all three queries and explain what each one shows
- [ ] Build a dashboard with at least two visualizations
- [ ] Enable auto-refresh and explain when this is and isn't appropriate
- [ ] Identify the SQL warehouse type (serverless vs. pro/classic) and explain
      when you'd choose each
- [ ] Run `query_dbsql.py` locally and get results (optional but recommended)

---

## The interview question

Practice until fluent:

> "We have 50 SQL analysts who currently use Snowflake. We're adopting Databricks
> for our data engineering team. Should we migrate the analysts to DBSQL or keep
> them on Snowflake?"

Good answer: this is a "it depends" with a clear framework. Keep them on Snowflake
if: they're productive, you don't have a strong reason to consolidate, the BI tool
integrations are working. Migrate to DBSQL if: you want a single governance layer
(Unity Catalog across both), your analysts are already querying tables produced by
the Databricks pipelines (latency from Snowflake sync becomes a problem), or you
want to reduce vendor count. The wrong answer is a blanket recommendation either way.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Dashboard built in DBSQL with auto-refresh
- [ ] Snowflake comparison articulated fluently in both directions
- [ ] Flask dashboard vs. DBSQL trade-offs documented
- [ ] Module status updated to `done` in repo README
