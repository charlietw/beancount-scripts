from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv
from urllib3.exceptions import ReadTimeoutError


def influx_client() -> InfluxDBClient:
    load_dotenv()
    token: str = os.environ["INFLUXDB_TOKEN"]
    host: str = os.environ["INFLUXDB_HOST"]
    org = "org"
    client = InfluxDBClient(url=host, token=token, org=org, debug=False, timeout=30_000)
    return client


def clear_bucket(measurement: str, bucket_name: str):
    """
    Removes all data in a given bucket
    """

    client: InfluxDBClient = influx_client()
    start = "2020-01-01T00:00:00Z"
    stop = "2026-01-01T00:00:00Z"
    attempts = 0
    while True:
        print("Emptying bucket...")
        try:
            client.delete_api().delete(
                start, stop, f'_measurement="{measurement}"', bucket=f"{bucket_name}", org="org"
            )
            break
        except ReadTimeoutError:
            print("Timeout. Trying again...")
        attempts += 1
        if attempts == 5:
            break

    client.close()


def write_to_influx(df, bucket, measurement, fields, tags):
    client: InfluxDBClient = influx_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for index, row in df.iterrows():
        p: Point = Point(measurement)
        for tag in tags:
            p.tag(tag['tag_name'], tag['tag_value'])
        for field in fields:
            p.field(field, row[field])
        p.time(row['date'])
        write_api.write(bucket=bucket, record=p)
    write_api.close()
    client.close()
