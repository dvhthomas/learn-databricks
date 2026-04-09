-- Module 6: Databricks SQL hands-on exercise
-- Run in the Databricks SQL editor against your learning.sensors.gold_hourly_stats table.
-- After writing the queries, add them to a Dashboard (SQL > Dashboards > New).

-- ===========================================================================
-- Query 1: Current sensor status
-- "What is each sensor's latest reading?"
-- This is the real-time view your Flask dashboard showed.
-- ===========================================================================

-- TODO: For each sensor, show the most recent hour's average temperature.
-- Include a status column: 'normal' (<35°C), 'warning' (35-40°C), 'critical' (>40°C)
-- Hint: use a subquery or window function to get the latest hour per sensor.

SELECT
    sensor_id,
    -- TODO: latest hour
    -- TODO: avg_temp_c from that hour
    -- TODO: CASE expression for status
    CASE
        WHEN avg_temp_c > 40 THEN 'critical'
        WHEN avg_temp_c > 35 THEN 'warning'
        ELSE 'normal'
    END AS status
FROM learning.sensors.gold_hourly_stats
-- TODO: filter to latest hour per sensor
ORDER BY avg_temp_c DESC;


-- ===========================================================================
-- Query 2: Alert trend over time
-- "How many sensors were in warning or critical state each hour?"
-- This is the time-series chart your Flask dashboard showed.
-- ===========================================================================

-- TODO: For each hour, count sensors in each status bucket.
-- Produce columns: hour, normal_count, warning_count, critical_count

SELECT
    hour,
    -- TODO: count sensors in each status
    COUNT(*) AS total_sensors
FROM learning.sensors.gold_hourly_stats
GROUP BY hour
ORDER BY hour;


-- ===========================================================================
-- Query 3: Sensor reliability
-- "Which sensors have the most data quality issues?"
-- ===========================================================================

-- TODO: For each sensor, show:
--   - total_hours: how many hours they've reported
--   - avg_reading_count: average readings per hour (should be consistent)
--   - hours_with_warnings: hours where avg_temp_c > 35
--   - warning_rate: hours_with_warnings / total_hours

SELECT
    sensor_id,
    -- TODO: fill in the aggregations
    COUNT(*) AS total_hours
FROM learning.sensors.gold_hourly_stats
GROUP BY sensor_id
ORDER BY total_hours DESC;


-- ===========================================================================
-- Dashboard instructions
-- ===========================================================================
-- After the queries run:
-- 1. SQL > Dashboards > New Dashboard > name it "Sensor Analytics"
-- 2. Add Query 1 as a Table visualization
-- 3. Add Query 2 as a Line chart (x=hour, y=warning_count + critical_count)
-- 4. Add Query 3 as a Bar chart (x=sensor_id, y=warning_rate)
-- 5. Set the dashboard to auto-refresh every 60 seconds
-- 6. Share the dashboard URL -- notice it's governed by Unity Catalog permissions


-- ===========================================================================
-- Optimization: add liquid clustering to your Gold table
-- ===========================================================================

-- Your Gold table was created without optimization hints.
-- Add liquid clustering on the columns most commonly used in WHERE clauses.

-- TODO: Enable liquid clustering on gold_hourly_stats
-- ALTER TABLE learning.sensors.gold_hourly_stats
--   CLUSTER BY (sensor_id, hour);

-- Run an OPTIMIZE to apply the clustering immediately
-- (normally this runs automatically in the background)
-- OPTIMIZE learning.sensors.gold_hourly_stats;

-- Check if query performance improved — run Query 1 before and after
-- and compare the query execution time in the Query History tab.


-- ===========================================================================
-- Reflection
-- ===========================================================================
-- Answer these in comments before your validation session:

-- 1. How long did it take to build this dashboard vs. the Flask dashboard?
--    What did you give up? What did you gain?

-- 2. An analyst says the dashboard is slow. What would you check first?

-- 3. Your manager asks why the company needs both Snowflake and DBSQL.
--    What's your answer?
