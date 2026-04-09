# Sample Data

Exercises use sensor data from the
[sensor-analytics](https://github.com/dvhthomas/sensor-analytics) project.

## Generating data

```sh
# In your sensor-analytics directory:
docker compose up -d
# Let it run for a few minutes, then:
cp -r data/hourly/ /path/to/learn-databricks/data/hourly/
docker compose down
```

## What the data looks like

Each Parquet file contains sensor readings with this schema:

```
sensor_id: string       e.g. "sensor_0001"
value:     float64      temperature reading
units:     string       "degrees_c"
timestamp: timestamp    when the reading was taken
```

Files are partitioned by hour: `hourly/20241118_10.parquet`

## Committed sample

`data/sample.json` contains 100 readings for exercises that don't need a full
Parquet file. Use this if you don't want to run sensor-analytics first.
