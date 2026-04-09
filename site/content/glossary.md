---
title: Glossary
description: Definitions of key terms used throughout the curriculum. Lectures link here rather than redefining terms inline.
---

Terms are listed alphabetically. Each definition is one paragraph — enough to understand the term when you encounter it in a lecture, not a deep dive.

## ACID

A set of properties that guarantee reliable database transactions. **Atomicity:** a write either fully succeeds or fully fails — no partial results. **Consistency:** readers always see a valid state of the data. **Isolation:** concurrent operations don't interfere with each other. **Durability:** once committed, data survives crashes. Traditional databases provide ACID by default. Data lakes on raw files provide none of it. Delta Lake and Iceberg add ACID guarantees on top of cloud storage.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Delta Lake protocol spec](https://github.com/delta-io/delta/blob/master/PROTOCOL.md)

---

## Adaptive Query Execution (AQE)

A Spark optimization that dynamically adjusts the query plan *during* execution based on actual runtime statistics. AQE can split skewed partitions, coalesce too-small partitions after a shuffle, and switch join strategies (e.g., from sort-merge to broadcast) when it discovers one side of a join is smaller than expected. Enabled by default in Spark 3.0+ and all Databricks runtimes.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark performance tuning docs](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

---

## Apache Iceberg

An open table format created at Netflix (2017), now an Apache project. Like Delta Lake, it adds ACID transactions, schema evolution, and time travel to Parquet files. Iceberg stores metadata as Parquet files in a tree structure (vs. Delta's JSON log). Its key advantage is broad multi-engine support: native integration with Spark, Flink, Trino, Snowflake, Athena, and Dremio. Governed by the Apache Software Foundation with contributions from 30+ companies.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [iceberg.apache.org](https://iceberg.apache.org/)

---

## Apache Kafka

A distributed event streaming platform that stores ordered, immutable sequences of events (topics) durably on disk. Unlike in-memory caches like Redis, Kafka retains events for a configurable period (days to forever), allowing multiple consumers to read independently. For IoT pipelines, Kafka is the standard backbone for ingesting sensor data — it handles connectivity to SCADA systems through Kafka Connect.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [kafka.apache.org](https://kafka.apache.org/intro/)

---

## Apache Parquet

A columnar file format for storing structured data. Instead of storing rows together (like CSV), Parquet stores each column separately — so reading just the `temperature` column doesn't require reading `sensor_id`, `timestamp`, etc. This makes analytical queries (which typically read few columns but many rows) dramatically faster. Parquet also supports built-in compression, predicate pushdown, and schema metadata. It's the standard storage format for Delta Lake, Iceberg, and most modern data lakes.

Source: [parquet.apache.org](https://parquet.apache.org/) | [Format specification](https://github.com/apache/parquet-format)

---

## Auto Loader

A Databricks feature that continuously monitors cloud storage (S3, ADLS, GCS) for new files and automatically ingests them into Delta tables. Unlike Kafka-based streaming, Auto Loader is file-based — it detects new files as they land and processes them in near-real-time (seconds to minutes latency, not milliseconds). Useful for batch-oriented data sources that drop files on a schedule.

Module: [4 — Delta Live Tables]({{< ref "modules/04-delta-live-tables" >}}) | Source: [Databricks Auto Loader docs](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/index.html)

---

## Bronze / Silver / Gold

The three layers of the medallion architecture. **Bronze:** raw data as received — append-only, immutable, everything kept. **Silver:** cleaned and validated data — bad readings removed, types enforced, duplicates dropped. **Gold:** business-ready aggregates — pre-computed metrics that analysts and dashboards consume directly. The names are Databricks convention; dbt uses staging/intermediate/marts for the same concept.

Module: [3 — Medallion Architecture]({{< ref "modules/03-medallion-architecture" >}})

---

## CEII

Critical Energy Infrastructure Information — a category of sensitive information defined by FERC (Federal Energy Regulatory Commission) that includes details about power generation facilities, grid topology, and vulnerability assessments. Utilities must restrict access to CEII and prove compliance to NERC auditors. In the wind utility scenario, turbine locations, generation capacity, and grid interconnection details are CEII.

Source: [FERC CEII regulations](https://www.ferc.gov/enforcement-legal/ceii)

---

## Checkpoint (Delta Lake)

A Parquet file in the `_delta_log/` directory that snapshots the complete table state (all current file references, schema, etc.) at a specific version. Written every 10 commits by default. Readers find the latest checkpoint and replay only the log entries after it, instead of replaying from version 0. Keeps read performance constant regardless of table history length.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Delta Lake protocol spec](https://github.com/delta-io/delta/blob/master/PROTOCOL.md)

---

## CMS

Condition Monitoring System — uses accelerometers and other sensors on wind turbine components (bearings, gearboxes, generators) to capture high-frequency vibration data. Unlike SCADA's routine 10-minute polling, CMS captures short "bursts" at high sampling rates (typically 25 kHz) to detect mechanical wear patterns before they become catastrophic failures.

Source: [DOE wind turbine gearbox research](https://www.energy.gov/eere/wind/articles/zeroing-no-1-cause-wind-turbine-gearbox-failures)

---

## DAG

Directed Acyclic Graph — Spark's internal representation of your computation as a graph of steps. Each node is an operation (filter, join, aggregate); edges show data flow. "Directed" means data flows one way. "Acyclic" means no loops. Spark uses the DAG to optimize the entire computation before running anything — reordering operations, pruning unused columns, and choosing join strategies.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Zaharia et al., CACM 2016](https://dl.acm.org/doi/10.1145/2934664)

---

## DBU

Databricks Unit — an abstract unit of compute. Different workload types consume DBUs at different rates per hour, and the price per DBU varies by contract tier. A "Medium" SQL warehouse consumes 16 DBUs/hour; a small Jobs cluster consumes about 10 DBUs/hour. AWS Premium tier list prices: Jobs Compute $0.15/DBU, All-Purpose $0.40/DBU, SQL Serverless $0.70/DBU.

Module: [1 — Why Spark Exists (cost model)]({{< ref "modules/01-why-spark" >}}) | Source: [Mammoth Analytics pricing guide](https://mammoth.io/blog/databricks-pricing-2/)

---

## Delta Lake

An open-source storage layer that adds ACID transactions, schema enforcement, and time travel to Parquet files in cloud storage. Created by Databricks, now a Linux Foundation project. Delta Lake works by maintaining a transaction log (`_delta_log/`) that records every change to the table — readers consult the log to determine which Parquet files constitute the current table, rather than scanning the directory.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [delta.io](https://delta.io/)

---

## delta-rs

A native Rust implementation of Delta Lake with Python bindings (the `deltalake` PyPI package). Lets you read, write, and manage Delta tables from Python without Spark or Java. Uses Apache Arrow under the hood, so it's compatible with Pandas, DuckDB, and Polars. This is what the Module 2 exercises use.

Source: [github.com/delta-io/delta-rs](https://github.com/delta-io/delta-rs)

---

## DLT / Lakeflow Declarative Pipelines

Delta Live Tables — a Databricks framework for building batch and streaming data pipelines declaratively. Instead of writing imperative code (read this, transform that, write here), you declare what datasets you want and what quality rules they must satisfy. The engine handles execution order, retries, and data quality tracking. Renamed to "Lakeflow Spark Declarative Pipelines" in 2025; the `import dlt` API still works but is being replaced by `from pyspark import pipelines`.

Module: [4 — Delta Live Tables]({{< ref "modules/04-delta-live-tables" >}}) | Source: [Databricks docs](https://docs.databricks.com/aws/en/ldp/)

---

## Driver (Spark)

The single process that runs your main program in a Spark cluster. It accepts your code, plans the execution, and coordinates work across executors. The driver does NOT process your data — it manages the processes that do.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark cluster overview](https://spark.apache.org/docs/latest/cluster-overview.html)

---

## DuckDB

An embedded analytical database (like SQLite, but for analytics). Runs in a single process on a single machine, processes data in columnar format, and is optimized for analytical queries. Requires zero infrastructure. DuckDB 1.0 shipped in June 2024 with a stable storage format; version 1.4 LTS (October 2025) added encryption, MERGE, and Iceberg write support. Can process about 1 TB of Parquet data in approximately 30 seconds on a modern laptop.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [duckdb.org](https://duckdb.org/why_duckdb)

---

## Executor (Spark)

A worker process that runs on a machine in a Spark cluster. Each executor receives tasks from the driver, processes a portion of the data, and reports results back. A cluster typically has many executors (2 to hundreds). Executors read data from storage, apply transformations, and write results — they do the actual computation.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark cluster overview](https://spark.apache.org/docs/latest/cluster-overview.html)

---

## Lazy evaluation

Spark records transformations (filter, groupBy, join) but does NOT execute them immediately. Execution only happens when you call an *action* — an operation that returns a result (like `show()`, `count()`, `collect()`) or writes data. This lets Spark optimize the entire computation plan before running anything.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}})

---

## Liquid clustering

A Delta Lake feature that automatically reorganizes data layout based on clustering keys to optimize query performance. Unlike Z-ordering (which requires rewriting all data), liquid clustering adjusts incrementally. Databricks recommends it for all new Delta tables. Not compatible with Hive-style partitioning.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Databricks clustering docs](https://docs.databricks.com/aws/en/delta/clustering)

---

## Medallion architecture

A data organization pattern with three layers: Bronze (raw), Silver (cleaned), Gold (business-ready). Every Databricks customer conversation uses this vocabulary. The same idea exists in dbt as staging/intermediate/marts. The key insight: separate the "never lose data" concern (Bronze) from the "make data trustworthy" concern (Silver) from the "make data fast to query" concern (Gold).

Module: [3 — Medallion Architecture]({{< ref "modules/03-medallion-architecture" >}})

---

## MERGE

A SQL operation that combines INSERT, UPDATE, and DELETE in a single atomic transaction. You specify a matching condition (e.g., same turbine_id and timestamp), then define what to do when rows match (update) and when they don't (insert). In Delta Lake, the entire operation is one commit — readers never see a half-updated table.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Delta Lake update docs](https://docs.delta.io/latest/delta-update.html)

---

## MLflow

An open-source platform for managing the ML lifecycle: experiment tracking (which parameters, which metrics), model registry (which version is in production), and model serving. On Databricks, MLflow integrates with Unity Catalog for model governance. Created by Databricks, now a Linux Foundation project.

Module: [7 — MLflow and the AI Platform]({{< ref "modules/07-mlflow-and-ai" >}}) | Source: [mlflow.org](https://mlflow.org/)

---

## NERC CIP

North American Electric Reliability Corporation — Critical Infrastructure Protection standards. A set of cybersecurity and reliability regulations for the US/Canadian power grid. Wind utilities above a certain size must comply, including proving who has access to CEII data, maintaining audit trails, and meeting physical/cyber security requirements. Maximum penalty: $1.54M per violation per day as of 2025.

Source: [NERC CIP standards](https://www.nerc.com/standards/reliability-standards/cip)

---

## Object storage (S3 / ADLS / GCS)

Cloud storage services that store data as objects (files) in a flat namespace of "buckets." Virtually unlimited capacity, accessible from any machine with credentials, designed for 99.999999999% durability, and inexpensive for cold data (about $0.023/GB/month). The trade-off: individual file operations are slower than local disk (100ms+ latency per request). Delta Lake and Iceberg are designed to work on top of object storage.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [AWS S3 pricing](https://aws.amazon.com/s3/pricing/)

---

## Partition (Spark)

A chunk of your dataset that one executor task processes independently. If your data has 200 partitions and you have 10 executors, each executor processes roughly 20 partitions. Partitions are the fundamental unit of parallelism in Spark. Partition count is determined by file count (when reading) or configuration (after a shuffle).

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark cluster overview](https://spark.apache.org/docs/latest/cluster-overview.html)

---

## Photon

Databricks' native execution engine, written in C++, that replaces the JVM-based Spark engine for supported operations. Runs by default on SQL warehouses and serverless compute. Features vectorized shuffle (columnar format with SIMD instructions) for approximately 1.5x throughput on CPU-bound workloads like large joins and wide aggregations.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Databricks Photon docs](https://docs.databricks.com/aws/en/compute/photon)

---

## SCADA

Supervisory Control and Data Acquisition — the industrial control systems that monitor and control wind turbines (and other industrial equipment). A SCADA system collects sensor data (temperatures, pressures, speeds, voltages) at regular intervals (typically every 10 minutes for routine monitoring), displays it to operators, and triggers alerts. SCADA data is the primary data source for wind turbine analytics and predictive maintenance.

Source: [Pandit et al., "SCADA data for wind turbine condition monitoring: A review," 2023](https://journals.sagepub.com/doi/10.1177/0309524X221124031)

---

## Shuffle

The process of redistributing data across Spark executors so that rows with the same key end up on the same machine. Happens during groupBy, join, distinct, and sort operations. During a shuffle, every executor writes outgoing data to disk, then reads incoming data from other executors over the network. Shuffles are the primary cause of slow Spark jobs.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark shuffle docs](https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations)

---

## Spark Connect

A thin client architecture introduced in Spark 4.0 where your code sends requests to a remote Spark server over gRPC. The `pyspark-client` package is 1.5 MB with no JVM dependency — decoupling "where you write code" from "where Spark runs." Useful on Databricks where serverless compute handles the cluster.

Module: [1 — Why Spark Exists]({{< ref "modules/01-why-spark" >}}) | Source: [Spark 4.0 release notes](https://spark.apache.org/releases/spark-release-4-0-0.html)

---

## SQL Warehouse

A Databricks compute endpoint optimized for running SQL queries. Comes in Classic (self-managed VMs), Pro, and Serverless (Databricks-managed, starts in seconds, scales to zero) variants. SQL warehouses connect to BI tools via JDBC/ODBC and serve concurrent analyst queries against Delta tables. Powered by the Photon engine.

Module: [6 — Databricks SQL]({{< ref "modules/06-databricks-sql" >}})

---

## Transaction log (_delta_log/)

An ordered sequence of JSON files in the `_delta_log/` directory that records every change to a Delta table. Each file represents one committed transaction containing actions: files added, files removed, metadata changes. The log is append-only and is the source of truth for table state — readers consult the log, not the directory listing. See also: [Delta Lake](#delta-lake).

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Databricks transaction log deep dive](https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html)

---

## UniForm

Delta Lake Universal Format — a feature that automatically generates Iceberg metadata alongside Delta metadata, both pointing to the same Parquet data files. Write through Delta; read from any Iceberg-compatible engine (Snowflake, Trino, Flink) without conversion. The write path is Delta-only — UniForm is read-only for Iceberg clients.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Databricks UniForm GA blog](https://www.databricks.com/blog/delta-lake-universal-format-uniform-iceberg-compatibility-now-ga)

---

## Unity Catalog

Databricks' centralized metastore for managing access control, data lineage, and audit logging across all data assets. Uses a three-level namespace: catalog → schema → table. Required for NERC CIP compliance at the wind utility because it provides the access control and audit trails that regulators demand.

Module: [5 — Unity Catalog]({{< ref "modules/05-unity-catalog" >}})

---

## Z-ordering

A Delta Lake optimization that physically sorts data within files by one or more columns to improve query performance when filtering on those columns. Requires rewriting all data files (expensive). Being superseded by liquid clustering, which adjusts incrementally without full rewrites.

Module: [2 — Delta Lake]({{< ref "modules/02-delta-lake" >}}) | Source: [Databricks clustering docs](https://docs.databricks.com/aws/en/delta/clustering)
