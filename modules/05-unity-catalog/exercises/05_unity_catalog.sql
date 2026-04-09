-- Module 5: Unity Catalog hands-on exercise
-- Run these statements in order in a Databricks SQL editor.
-- Requires a workspace with Unity Catalog enabled (free trial).
--
-- Work through each section. The TODOs are where you fill in the logic.
-- The COMMENTs explain what you should observe at each step.

-- ===========================================================================
-- Section 1: Explore what already exists
-- ===========================================================================

-- See all catalogs in the metastore
SHOW CATALOGS;

-- See the current catalog and schema context
SELECT current_catalog(), current_schema();


-- ===========================================================================
-- Section 2: Create your own catalog and schema
-- ===========================================================================

-- TODO: Create a catalog called `learning`
-- CREATE CATALOG ...;

-- TODO: Set it as your default catalog
-- USE CATALOG ...;

-- TODO: Create a schema called `sensors`
-- CREATE SCHEMA ...;

-- TODO: Set it as your default schema
-- USE SCHEMA ...;

-- Verify
SELECT current_catalog(), current_schema();
-- Expected: learning, sensors


-- ===========================================================================
-- Section 3: Create a managed table
-- ===========================================================================

-- Create a managed Gold table from scratch (no external data needed)
-- TODO: Create a Delta table `gold_hourly_stats` with these columns:
--   sensor_id STRING, hour TIMESTAMP, avg_temp_c DOUBLE,
--   max_temp_c DOUBLE, reading_count BIGINT

-- CREATE TABLE learning.sensors.gold_hourly_stats (
--   ...
-- ) USING DELTA
-- COMMENT 'Hourly temperature statistics per sensor';


-- Insert some sample rows
-- TODO: Insert 5-10 sample rows. Mix sensor_0001 through sensor_0003.
-- INSERT INTO learning.sensors.gold_hourly_stats VALUES (...);


-- Verify
SELECT * FROM learning.sensors.gold_hourly_stats;


-- ===========================================================================
-- Section 4: Access control
-- ===========================================================================

-- COMMENT: The table exists but access is controlled by Unity Catalog.
-- By default, only the table owner can read it.

-- Describe the current grants on the table
SHOW GRANTS ON TABLE learning.sensors.gold_hourly_stats;

-- TODO: Grant SELECT to the `account users` group (all users in the account)
-- GRANT SELECT ON TABLE learning.sensors.gold_hourly_stats TO `account users`;

-- Verify the grant was applied
SHOW GRANTS ON TABLE learning.sensors.gold_hourly_stats;

-- TODO: Revoke the grant
-- REVOKE SELECT ON TABLE learning.sensors.gold_hourly_stats FROM `account users`;


-- ===========================================================================
-- Section 5: Table metadata and discoverability
-- ===========================================================================

-- Add a description to a column
-- TODO: Add a comment to the avg_temp_c column
-- ALTER TABLE learning.sensors.gold_hourly_stats
--   ALTER COLUMN avg_temp_c COMMENT 'Average temperature in degrees Celsius for the hour';

-- Add tags to the table
-- TODO: Tag the table to indicate it's a Gold-quality table
-- ALTER TABLE learning.sensors.gold_hourly_stats
--   SET TAGS ('quality' = 'gold', 'owner' = 'sensor-team', 'sla' = '99.9');

-- View table details including tags and comments
DESCRIBE TABLE EXTENDED learning.sensors.gold_hourly_stats;


-- ===========================================================================
-- Section 6: Lineage
-- ===========================================================================

-- Run a query that reads from the table — this creates a lineage event
SELECT sensor_id, AVG(avg_temp_c) as overall_avg
FROM learning.sensors.gold_hourly_stats
GROUP BY sensor_id;

-- COMMENT: After running the query above, go to the Databricks UI:
--   Catalog Explorer > learning > sensors > gold_hourly_stats > Lineage tab
-- You should see this query recorded as a downstream consumer of the table.


-- ===========================================================================
-- Section 7: Audit logs via system tables
-- ===========================================================================

-- Unity Catalog audit logs are queryable as Delta tables in the `system` catalog
-- TODO: Query the audit log for your own recent activity
-- Hint: system.access.audit contains all access events

SELECT
    event_time,
    user_identity.email AS user,
    action_name,
    request_params
FROM system.access.audit
WHERE user_identity.email = current_user()
  AND event_time > DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY event_time DESC
LIMIT 20;

-- COMMENT: You should see your own SELECT and ALTER statements from this session.
-- This is the audit trail that compliance teams require.


-- ===========================================================================
-- Section 8: Reflection
-- ===========================================================================

-- Answer these in comments before your validation session:

-- 1. What is the difference between GRANT on a TABLE vs. GRANT on a SCHEMA?
--    When would you use each?

-- 2. You query system.access.audit and see a user queried a table containing PII
--    that they shouldn't have access to. What do you do? What in UC prevents this
--    from happening in the future?

-- 3. What's the difference between the `learning` catalog you created and the
--    `main` catalog that exists by default?

-- 4. A new data engineer joins the team. What's the minimum set of grants they
--    need to start working with the sensors schema?
