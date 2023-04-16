from src import functions
from typing import Literal
from pandas import DataFrame, Series
import pandas as pd
import pytest
from typing import Any


@pytest.fixture
def expenses_df() -> DataFrame:
    """
    Create a mock expenses dataframe which would be output by Beancount
    """
    data: dict[str, Any] = {
        "month": [1, 3, 5],
        "year": [2020, 2021, 2022],
        "sum_position": ["200.00 GBP", "15.10 GBP", "120.12 GBP"],
        "account": [
            "Expenses:Account:Sub",
            "Expenses:Account:OtherSub",
            "Expenses:Account:FinalSub",
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def expenses_datetime_df(expenses_df: DataFrame) -> DataFrame:
    """
    Create a mock dataframe with dates converted to datetime and currency col fixed
    """
    expenses_df["sum_position"] = functions.fix_currency_column(
        expenses_df["sum_position"]
    )
    return functions.convert_to_datetime(expenses_df)


@pytest.fixture
def dates_df() -> DataFrame:
    """
    Create a mock dataframe containing a set of dates for merging
    """
    return functions.create_month_year_dataframe("2020-01-01", "2022-12-01")


@pytest.fixture
def expenses_datetime_df_merged(expenses_datetime_df: DataFrame) -> DataFrame:
    """
    Create a mock dataframe with dates converted to datetime merged with the date df
    """
    return functions.pad_dates(expenses_datetime_df, "2020-01-01", "2022-12-01")


def test_fix_currency_column(expenses_df: DataFrame) -> None:
    """
    Asserts that we can remove the currency symbol as expected
    """
    expected_values: Series = Series([200.00, 15.10, 120.12])
    actual_values: Series = functions.fix_currency_column(expenses_df["sum_position"])

    assert actual_values.equals(expected_values) == True


def test_create_month_year_dataframe() -> None:
    """
    Tests the creation of a dataframe consisting of all months in a given range
    """
    expected: DataFrame = pd.DataFrame(
        data={"date": pd.to_datetime(["2020-01-01", "2020-02-01", "2020-03-01"])}
    )
    actual: DataFrame = functions.create_month_year_dataframe(
        "2020-01-01", "2020-03-01"
    )
    assert expected.equals(actual) == True


def test_convert_to_datetime(expenses_df: DataFrame) -> None:
    """
    Tests conversion to datetime
    """
    date: Series = pd.Series(pd.to_datetime(["2020-01-01", "2021-03-01", "2022-05-01"]))
    df: DataFrame = functions.convert_to_datetime(expenses_df)
    assert date.equals(df["date"]) == True
    assert list(df.columns.values) == ["sum_position", "account", "date"]


def test_pad_dates(expenses_datetime_df: DataFrame) -> None:
    """
    Pads dates and asserts that the resulting length is 36
    """
    expenses_datetime_df = functions.pad_dates(
        expenses_datetime_df, "2020-01-01", "2022-12-01"
    )
    expected: int = 36
    actual: int = len(expenses_datetime_df)
    assert expected == actual


def test_fill_data_zero(expenses_datetime_df_merged: DataFrame) -> None:
    """
    We know that there are three actual values in the test data, and we know how many
    rows there are in total, so we can assert that the correct number are filled
    """
    expenses_datetime_df_merged["sum_position"] = functions.fill_data_zero(
        expenses_datetime_df_merged["sum_position"]
    )
    zeroes: Series[bool] = expenses_datetime_df_merged["sum_position"] == 0
    assert zeroes.sum() == 33
