# Module 3 Validation: Medallion Architecture

---

## Oral questions

**Must know cold:**

1. Why is Bronze append-only and immutable? What breaks if you modify Bronze?

2. A data analyst tells you their dashboard shows the wrong numbers today. Walk
   me through how the medallion architecture helps you diagnose this.

3. What's the difference between Silver cleaning and Gold aggregating? Give
   a sensor-analytics example of a transformation that belongs in each layer.

4. A teammate wants to silently drop all readings outside -50–100°C in Silver.
   What do you say, and what do you do instead?

5. How does the medallion architecture map to what dbt does? What's the same
   and what's different?

**Know the shape:**

6. What does "data at the grain of the business" mean for a Gold table?

7. A Gold table is being re-aggregated by every analyst before they can use it.
   What does this tell you about the Gold design?

---

## Code challenge

Run `exercises/medallion.py` locally:

```sh
uv run python modules/03-medallion-architecture/exercises/medallion.py
```

You should be able to:

- [ ] Explain why the Bronze writer uses `mode="append"` not `mode="overwrite"`
- [ ] Show the `silver_rejected` table and explain what's in it
- [ ] Explain what happens if you run the script twice — does it produce duplicate data?
- [ ] Describe what DLT would handle automatically that this script doesn't

---

## The interview question

Practice until fluent:

> "A retail company's data team spends most of their time fixing broken dashboards.
> How would you restructure their data pipeline?"

Good answer: diagnose the problem (likely no separation between raw and refined data,
no quality tracking, transformations buried in dashboard queries), propose the medallion
pattern, explain Bronze's immutability as the recovery mechanism, Silver's quality
tracking as the trust mechanism, Gold's pre-aggregation as the performance mechanism.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Code challenge complete and explained
- [ ] Can explain why this exercise is the manual version of what DLT does
- [ ] Module status updated to `done` in repo README
