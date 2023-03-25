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
        data={
            "date": pd.to_datetime(["2020-01-01", "2020-02-01", "2020-03-01"]),
            "month": [1, 2, 3],
            "year": [2020, 2020, 2020],
        }
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
    assert list(df.columns.values) == ['sum_position', 'account', 'date']
