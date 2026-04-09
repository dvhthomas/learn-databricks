---
title: "Knowledge Test: Medallion Architecture"
summary: "Validate your understanding of Bronze/Silver/Gold layers, data quality tracking, grain decisions, and how medallion compares to dbt and other patterns"
weight: 99
type: test
tags:
  - medallion
  - bronze-silver-gold
  - data-quality
  - dbt
---

## Oral questions

**Must know cold:**

1. Why is Bronze append-only and immutable? What specifically breaks if you modify a Bronze record after it has been written? Use the wind utility scenario.

2. What is the difference between Silver cleaning and Gold aggregating? Give a concrete SCADA example of a transformation that belongs in Silver and one that belongs in Gold.

3. A teammate proposes silently dropping all readings outside -50 to 100 C in the Silver transformation. What do you say, and what do you do instead?

4. Explain the medallion architecture to a non-technical stakeholder — the wind utility's CFO — in two sentences. No jargon.

5. How does the medallion architecture map to dbt's staging/intermediate/marts? What is the same and what is different?

6. An analyst's dashboard shows the wrong fleet capacity factor this morning. Walk through how the medallion architecture helps you diagnose where the problem entered.

**Know the shape:**

7. What does "data at the grain of the business" mean for a Gold table? How do you decide the right grain?

8. A Gold table is being re-aggregated by every analyst before they can use it. What does this tell you about the Gold design?

9. When is medallion architecture overkill? Describe a scenario where fewer layers would be the right choice.

## Code challenge

Run `modules/03-medallion-architecture/exercises/medallion.py`:

```sh
uv run python modules/03-medallion-architecture/exercises/medallion.py
```

You should be able to:

- [ ] Explain why the Bronze writer uses `mode="append"` and not `mode="overwrite"`
- [ ] Show the `silver_rejected` table and explain what is in it and why it exists
- [ ] Explain what happens if you run the script twice — does it produce duplicate data? In which layers?
- [ ] Describe what DLT (Module 4) would handle automatically that this script does not — name at least four things
- [ ] Modify the Gold aggregation to add a new metric (e.g., temperature range = max - min) and re-run

## The interview question

Practice until fluent:

> "Your wind utility's analysts spend most of their time fixing broken dashboards. The fleet capacity factor shows up differently in every meeting. How would you restructure the data pipeline?"

A good answer:
- **Diagnose** — the root cause is likely no separation between raw and refined data. Transformations live in dashboard queries. Each analyst writes their own cleaning logic. There is no single source of truth.
- **Propose** — medallion architecture. Bronze captures the immutable record. Silver applies standardized validation (so the cleaning logic is written once, not per-analyst). Gold pre-aggregates to the metrics the business actually needs.
- **Explain the mechanism** — Bronze immutability means you can always reprocess when something goes wrong. Silver quality tracking means you can measure and report data quality (not just hope for it). Gold pre-aggregation means dashboards read finished metrics instead of computing them on the fly.
- **Be honest about limits** — medallion does not fix bad source data. It does not fix poorly defined business metrics. It structures the pipeline so those problems are visible and diagnosable instead of hidden in personal spreadsheets.
