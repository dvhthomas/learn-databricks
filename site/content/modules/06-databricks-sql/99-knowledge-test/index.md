---
title: "Knowledge Test: Databricks SQL"
summary: "Validate your understanding of SQL warehouses, Photon, the Databricks vs. Snowflake comparison, BI tool connectivity, and query optimization"
weight: 99
type: test
tags:
  - databricks-sql
  - sql-warehouse
  - photon
  - snowflake
  - liquid-clustering
---

## Oral questions

**Must know cold:**

1. What is a SQL warehouse and how does it differ from an all-purpose Spark cluster? Give three specific reasons why an analyst should use a SQL warehouse instead of a notebook attached to a cluster.

2. Explain what Photon does without using the words "vectorized" or "columnar." Use an analogy that a non-technical stakeholder would understand -- then explain the actual mechanism (SIMD, batch processing, native C++ execution) for a technical audience.

3. A customer's CFO asks why they should pay for Databricks SQL when they already have Snowflake for their retail division. Make the case for Databricks. Now steelman Snowflake's position -- give at least three areas where Snowflake is genuinely better.

4. What is the difference between Z-ordering and Liquid clustering? Which would you recommend for a new Delta table today and why? When might Z-ordering still be appropriate?

5. An analyst complains that their DBSQL dashboard is slow. Walk through the first three things you would check, in order, and what you would do for each finding.

6. Explain the three SQL warehouse types (Classic, Pro, Serverless). When would you choose each? Why does Databricks recommend Serverless for most workloads?

**Know the shape:**

7. What is result caching in DBSQL? Describe the caching layers (result cache, disk cache, predictive I/O). What is the catch -- when does caching not help?

8. How does a BI tool like Tableau connect to Databricks SQL? What does the analyst need to configure? What is Partner Connect and why does it matter for adoption?

9. What is Delta Sharing? How is it different from just granting SELECT on a table? When would you use it instead of giving someone a Snowflake account?

## Code challenge

Complete `modules/06-databricks-sql/exercises/06_dbsql_queries.sql` in the Databricks SQL editor.

You should be able to:

- [ ] Run all three queries and explain what each one shows
- [ ] Build a dashboard with at least two visualizations (table + chart)
- [ ] Enable auto-refresh and explain when this is and is not appropriate (hint: result caching, compute cost)
- [ ] Identify your SQL warehouse type (serverless vs. pro vs. classic) and explain when you would choose each
- [ ] Add Liquid clustering to the Gold table and demonstrate the performance difference using Query History
- [ ] Run `query_dbsql.py` locally and get results (optional but recommended)

## The interview question

Practice until fluent:

> "We have 50 SQL analysts who currently use Snowflake. We are adopting Databricks for our data engineering team. Should we migrate the analysts to DBSQL or keep them on Snowflake?"

A good answer has a framework, not a blanket recommendation:

**Keep them on Snowflake if:** they are productive, their BI tool integrations work, their query patterns are well-served by Snowflake's optimizer, and you do not have a strong reason to consolidate. Migrating productive analysts is expensive and risky.

**Migrate to DBSQL if:** (a) analysts primarily query tables produced by Databricks pipelines and the Snowflake sync adds latency or cost, (b) you want a single governance layer (Unity Catalog) across both engineering and analytics instead of maintaining two access control systems, (c) you want to reduce vendor count and total licensing cost.

**The wrong answer:** a blanket recommendation in either direction without understanding the specific workload patterns, analyst productivity, and organizational priorities. Both platforms are strong. The question is which architecture best serves this customer.
