"""
Module 6 (optional): Query Databricks SQL from local Python.

This shows how a downstream application would consume DBSQL programmatically —
useful for understanding how BI tools and custom apps connect.

Setup:
1. In your Databricks workspace: SQL > SQL Warehouses > your warehouse > Connection details
2. Copy the Server hostname and HTTP path
3. Create a .env file (never commit this):

    DATABRICKS_HOST=<your-workspace>.azuredatabricks.net
    DATABRICKS_TOKEN=<your-personal-access-token>
    DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>

Then run:
    uv run python modules/06-databricks-sql/exercises/query_dbsql.py
"""

import os
from pathlib import Path

from databricks import sql
from rich.console import Console
from rich.table import Table

console = Console()


def get_connection_params() -> dict:
    """
    Load connection parameters from environment variables.
    Never hardcode credentials — always use environment or a secrets manager.
    """
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH")

    if not all([host, token, http_path]):
        raise EnvironmentError(
            "Missing Databricks connection config. "
            "Set DATABRICKS_HOST, DATABRICKS_TOKEN, and DATABRICKS_HTTP_PATH."
        )

    return {"server_hostname": host, "http_path": http_path, "access_token": token}


def run_query(cursor, sql_text: str) -> list[dict]:
    """Execute a query and return results as a list of dicts."""
    cursor.execute(sql_text)
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def display_results(title: str, rows: list[dict]) -> None:
    """Display query results as a rich table."""
    if not rows:
        console.print(f"[yellow]{title}: no results[/yellow]")
        return

    table = Table(title=title, show_header=True, header_style="bold")
    for col in rows[0].keys():
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(v) if v is not None else "" for v in row.values()])
    console.print(table)


def main() -> None:
    params = get_connection_params()
    console.print(f"Connecting to {params['server_hostname']}...")

    with sql.connect(**params) as connection:
        with connection.cursor() as cursor:

            # TODO: Run the current sensor status query from 06_dbsql_queries.sql
            # and display the results using display_results()

            # Query 1: current sensor status
            status_rows = run_query(cursor, """
                SELECT
                    sensor_id,
                    MAX(hour) AS latest_hour,
                    AVG(avg_temp_c) AS avg_temp_c,
                    -- TODO: add the status CASE expression
                    'normal' AS status
                FROM learning.sensors.gold_hourly_stats
                GROUP BY sensor_id
                ORDER BY avg_temp_c DESC
            """)
            display_results("Current Sensor Status", status_rows)

            # TODO: Run query 2 (alert trend) and display it
            # trend_rows = run_query(cursor, "...")
            # display_results("Alert Trend", trend_rows)

            console.print("\n[bold]Query complete.[/bold]")
            console.print(
                "Notice: this is the same data your DBSQL dashboard shows, "
                "consumed programmatically. This is how a custom app or BI tool "
                "connects to Databricks SQL."
            )


if __name__ == "__main__":
    main()
