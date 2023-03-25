from pandas import Series, DataFrame, DatetimeIndex
import pandas as pd


def fix_currency_column(series: Series) -> Series:
    """
    Take a Series, remove GBP, strip out trailing whitespace, turn into number
    """
    return pd.to_numeric(series.str.replace("GBP", "").str.rstrip())


def create_month_year_dataframe(min_date, max_date) -> DataFrame:
    """
    Create a new DataFrame with all possible month-year combinations
    between two dates
    """
    all_dates: DatetimeIndex = pd.date_range(start=min_date, end=max_date, freq="MS")
    all_months: DataFrame = pd.DataFrame(
        data={"date": all_dates, "month": all_dates.month, "year": all_dates.year}
    )
    return all_months


def convert_to_datetime(df: DataFrame) -> DataFrame:
    """
    Take a dataframe with 'month' and 'year' columns and return a datetime,
    dropping the month and year
    """
    df["date"] = pd.to_datetime(df["month"].astype(str) + " " + df["year"].astype(str))
    return df.drop(columns=['month', 'year'])
