---
title: "Module 5: Unity Catalog"
summary: "NERC auditors ask who has access to grid operations data. You can't answer. How do you govern data across teams, clouds, and compliance requirements?"
status: in-progress
weight: 5
tags:
  - unity-catalog
  - governance
  - access-control
  - lineage
  - nerc-cip
  - ceii
prerequisites:
  - 1
  - 2
last_refreshed: "2026-04-08"
---

Your wind utility's data platform is working. Delta tables are reliable, the medallion layers are clean, DLT pipelines run automatically. Then a NERC CIP audit arrives and asks three questions:

1. **Who has access to CEII (Critical Energy Infrastructure Information)?** Grid topology, generation capacity, and vulnerability data are regulated. You need to prove that only authorized personnel can see them.
2. **What is the lineage of your compliance reports?** When the quarterly capacity report says your fleet produced 1.2 TWh, what data went into that number? Can you trace it back to the raw SCADA readings?
3. **What changed and when?** If an analyst modified a Gold table on March 15, who approved it and what was the previous state?

You can't answer any of these with file permissions and tribal knowledge. You need a governance layer.

**Unity Catalog is Databricks' answer — a centralized metastore that manages access control, data lineage, and audit logging across all your data assets.** It uses a three-level namespace (catalog → schema → table) that maps naturally to organizational boundaries: one catalog per environment (dev/prod) or per business unit, schemas for functional areas, tables for specific datasets.

Most enterprise Databricks deals now hinge on Unity Catalog, not Spark. The conversation is rarely "can Spark run our queries" — it's "can we govern our data across teams, clouds, and compliance requirements." This module teaches you what that conversation looks like.

A large portion of existing Databricks customers are mid-migration from Hive Metastore to Unity Catalog. Understanding the pain of that migration — and how to minimize it — is practical consulting knowledge.

## Prerequisites

Complete [Module 2: Delta Lake]({{< ref "02-delta-lake" >}}). You need to understand Delta's storage model to see how Unity Catalog governs it.

## Exercises

Exercises live in [`modules/05-unity-catalog/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/05-unity-catalog/exercises). You'll set up a namespace, configure access controls, and trace lineage through a pipeline.
