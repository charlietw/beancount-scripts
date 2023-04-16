from src import functions, connector
import pandas as pd


if __name__ == "__main__":
    measurement_name: str = "savings_rate"
    bucket_name: str = "python"
    df: pd.DataFrame = functions.calculate_savings_rate()
    connector.clear_bucket(measurement_name, bucket_name)
    connector.write_to_influx(df, bucket_name, measurement_name)
