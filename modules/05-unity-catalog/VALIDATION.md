# Module 5 Validation: Unity Catalog

---

## Oral questions

**Must know cold:**

1. Explain the three-level Unity Catalog namespace. What is a metastore, a catalog,
   and a schema? Give a concrete example of how a company with three teams (data
   engineering, analytics, ML) might structure theirs.

2. What is the difference between Unity Catalog and the legacy Hive Metastore?
   Name two specific things UC gives you that Hive Metastore doesn't.

3. A healthcare customer says they can't adopt Databricks because they can't prove
   who has access to patient data. Walk me through how you'd use Unity Catalog
   to address that concern.

4. What is data lineage in Unity Catalog? Give a scenario where a data engineer
   would use it on a Monday morning after a weekend incident.

5. What's the difference between a managed table and an external table?
   When would a regulated enterprise prefer external tables?

**Know the shape:**

6. What are system tables in Unity Catalog? Name one thing you can query from them.

7. A customer is migrating from Hive Metastore to Unity Catalog. What's the biggest
   category of pain they're likely to hit? (Permissions, storage credentials, compute
   policies — pick one and explain.)

8. What is Delta Sharing and how does it relate to Unity Catalog?

---

## Code challenge

Complete `exercises/05_unity_catalog.sql` in a Databricks SQL editor.

You should be able to:

- [ ] Create a catalog and schema successfully
- [ ] Register your Gold table from Module 4 in Unity Catalog
- [ ] Show that reading the table fails before a GRANT is issued
- [ ] Issue a GRANT and verify reading works
- [ ] Query the lineage for the Gold table after running a query against it
- [ ] Find at least one audit log entry for your own queries in the system tables

---

## The interview question

Practice until fluent:

> "A Fortune 500 retailer is evaluating Databricks. Their legal team says any
> solution must demonstrate column-level access control on customer PII and
> provide a 90-day audit trail of all data access. Can Databricks do this?"

Good answer: yes, via Unity Catalog. Column-level security through column masks
or dynamic views, row-level security through row filters. Audit trail via system
tables (`system.access.audit`) which retain access logs queryable as Delta tables.
Tie it to the migration caveat: if they have existing Databricks, there's a UC
migration involved — understand the timeline.

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] Code challenge complete — GRANT demonstrated, lineage visible, audit log queried
- [ ] Can explain the Hive Metastore migration story at a high level
- [ ] Module status updated to `done` in repo README
