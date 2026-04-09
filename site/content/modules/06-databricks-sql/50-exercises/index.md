---
title: "Exercises: Databricks SQL"
summary: "Build a dashboard in the DBSQL editor, optimize query performance with Liquid clustering, and query Databricks SQL programmatically from local Python"
weight: 50
type: exercise
---

## DBSQL queries and dashboard (SQL, Databricks workspace)

This exercise runs in the Databricks SQL editor. You will write queries against your Gold table, build a dashboard, and optimize query performance -- replacing the Flask dashboard from sensor-analytics without writing a single line of application code.

The exercise file has `# TODO` markers -- fill them in before running.

```sh
# Open in the Databricks SQL editor (copy-paste or upload):
modules/06-databricks-sql/exercises/06_dbsql_queries.sql
```

### What you will do

1. **Query 1: Current sensor status** -- for each sensor, show the latest hour's average temperature and a status classification (normal/warning/critical). This is the real-time view your Flask dashboard showed.
2. **Query 2: Alert trend over time** -- for each hour, count sensors in each status bucket. This is the time-series chart.
3. **Query 3: Sensor reliability** -- for each sensor, show reporting hours, average reading count, warning hours, and warning rate.
4. **Build a dashboard** -- add all three queries as visualizations (table, line chart, bar chart), set auto-refresh to 60 seconds, and share the URL.
5. **Add Liquid clustering** -- enable clustering on the Gold table and compare query performance before and after using the Query History tab.

### After running

Answer the reflection questions in the exercise file:
- How long did it take to build this dashboard vs. the Flask dashboard? What did you give up? What did you gain?
- An analyst says the dashboard is slow. What would you check first?
- Your manager asks why the company needs both Snowflake and DBSQL. What is your answer?

## Python connector (optional, local)

This exercise runs locally against your Databricks workspace. It shows how a downstream application or custom tool connects to DBSQL programmatically -- the same connection that BI tools use under the hood, exposed as a Python API.

### Setup

1. In your Databricks workspace: SQL > SQL Warehouses > your warehouse > Connection details
2. Copy the Server hostname and HTTP path
3. Create a `.env` file (never commit this):

```sh
DATABRICKS_HOST=<your-workspace>.cloud.databricks.com
DATABRICKS_TOKEN=<your-personal-access-token>
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>
```

4. Run with uv:

```sh
uv run python modules/06-databricks-sql/exercises/query_dbsql.py
```

### What you will do

1. **Connect** to your SQL warehouse from local Python using the `databricks-sql-connector`
2. **Run** the sensor status query and see results in the terminal
3. **Complete the TODOs** to add the alert trend query and the status CASE expression
4. **Observe** that this returns the same data as the DBSQL dashboard -- same table, same governance, different interface

### Key learning

The Python connector demonstrates that DBSQL is not just a web UI -- it is a SQL endpoint that any application can query. This is how a custom alerting service, a data quality monitor, or a CI/CD pipeline validation step would consume data from your Gold tables.
