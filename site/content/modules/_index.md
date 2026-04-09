---
title: Modules
---

## What this is

A self-directed curriculum for building practical, working knowledge of the Databricks platform and the data engineering ecosystem around it. The goal is **industry-ready knowledge** — enough to have a fluent technical conversation with a Databricks engineer, advise a customer on platform choices with genuine authority, and demonstrate hands-on familiarity.

This is not a tutorial collection. Each module teaches through a concrete scenario, produces working code, and validates understanding through oral questions and exercises.

## How accurate is this?

This curriculum was built with AI assistance (Claude) and grounded in published sources — official documentation, peer-reviewed papers, industry reports, and vendor pricing guides. Sources are cited inline throughout the lectures.

That said: **the wind utility scenario is fictional.** The data volumes, costs, and risk numbers are modeled from real industry data (SCADA polling intervals from published research, gearbox failure rates from EPRI, NERC penalty amounts from public enforcement actions), but the specific utility, its turbine fleet, and its teams don't exist. The cost model is an informed estimate, not a quote.

Treat this like a well-researched case study, not a consulting engagement. The goal is to give you the right mental models and enough real numbers to reason credibly — not to produce a deployment-ready architecture document.

## The scenario

You built [sensor-analytics](https://github.com/dvhthomas/sensor-analytics) — a working data pipeline with TCP collectors, Redis queues, a Parquet writer, and DuckDB for analysis. It processes 50 simulated sensors on one machine. It works.

Now imagine that system is real. You're running 500 wind turbines across 3 regions for an electric utility. Each turbine has 50+ SCADA sensors reporting every 10 minutes. Field engineers need real-time alerts. Analysts need historical trends. Data scientists need training data for predictive maintenance models. A compliance team needs audit trails for NERC (North American Electric Reliability Corporation) regulators.

**What breaks, what do you replace, and in what order?**

## The modules

Each module answers one piece of that question — starting with the compute layer and building outward to storage, structure, automation, governance, analytics, and ML. The modules build on each other: you can't understand Delta Live Tables without understanding the medallion architecture, and you can't understand the medallion architecture without understanding Delta Lake.
