from pandas import Series, DataFrame, DatetimeIndex
import pandas as pd
import subprocess
from io import StringIO
from dotenv import load_dotenv
import os


def fix_currency_column(series: Series) -> Series:
    """
    Take a Series, remove GBP, strip out trailing whitespace, turn into number
    """
    return pd.to_numeric(series.str.replace("GBP", "").str.rstrip())


def create_month_year_dataframe(min_date: str, max_date: str) -> DataFrame:
    """
    Create a new DataFrame with all possible month-year combinations
    between two dates
    """
    all_dates: DatetimeIndex = pd.date_range(start=min_date, end=max_date, freq="MS")
    all_months: DataFrame = pd.DataFrame(data={"date": all_dates})
    return all_months


def convert_to_datetime(df: DataFrame) -> DataFrame:
    """
    Take a dataframe with 'month' and 'year' columns and return a datetime,
    dropping the month and year
    """
    df["date"] = pd.to_datetime(df["month"].astype(str) + " " + df["year"].astype(str))
    return df.drop(columns=["month", "year"])


def pad_dates(df: DataFrame, min_date: str, max_date: str) -> DataFrame:
    """
    Add extra rows for dates when there is no data
    """
    dates_df: DataFrame = create_month_year_dataframe(min_date, max_date)
    return pd.merge(dates_df, df, on=["date"], how="left")


def fill_data_zero(series: Series) -> Series:
    """
    Add zero balance in when there is none for that specific row
    """
    # df['sum_position'].fillna(method='ffill', inplace=True)
    return series.fillna(0)


def group_by_month(df: DataFrame, column_name: str) -> Series:
    """
    Takes a dataframe with 'sum_position' and groups it by date, i.e. removes the account
    """
    return df.groupby(df["date"])[column_name].sum()


def construct_account_query(accounts: list[str]) -> str:
    """
    Takes 'accounts' and constructs the string required for bean-query
    """
    query = "SELECT MONTH(date) AS month, YEAR(date) as year, sum(position), account "
    for i, account in enumerate(accounts):
        if i == 0:  # First account has to be WHERE
            query += f"WHERE account ~ '{account}' "
        else:  # Rest have to be OR
            query += f"OR account ~ '{account}' "
    query += "GROUP BY year, month, account"
    return query


def account_query_to_df(accounts: list[str]) -> pd.DataFrame:
    """
    Takes 'accounts' and returns a DataFrame containing the result
    of calling 'bean-query', padding dates
    """
    query: str = construct_account_query(accounts)
    query_result: str = bean_query(query)
    query_result_df: pd.DataFrame = pd.read_csv(StringIO(query_result))
    query_result_df["sum_position"] = fix_currency_column(
        query_result_df["sum_position"]
    )
    query_result_df = convert_to_datetime(query_result_df)
    max_date: str = query_result_df["date"].max()
    return pad_dates(query_result_df, "2020-01-01", max_date)


def bean_query(query) -> str:
    """
    Queries beancount and returns the result as a string
    """
    load_dotenv()
    filepath = os.environ["BEANCOUNT_FILE"]
    args: list[str] = [
        "bean-query",
        "-f",
        "csv",
        filepath,
        query,
    ]
    proc = subprocess.run(args, capture_output=True, check=True)
    return proc.stdout.decode("utf-8")


def income_query() -> pd.Series:
    df_income: pd.DataFrame = account_query_to_df(["Income:*"])
    df_income["sum_position"] = (
        df_income["sum_position"] * -1
    )  # need to reverse the income
    df_income = df_income.rename(columns={"sum_position": "income"})
    return group_by_month(df_income, "income")


def expenses_query() -> pd.Series:
    df_expenses: pd.DataFrame = account_query_to_df(["Expenses:*"])
    df_expenses = df_expenses.rename(columns={"sum_position": "all_expenses"})
    return group_by_month(df_expenses, "all_expenses")


def employment_expenses_query() -> pd.Series:
    df_employment_expenses: pd.DataFrame = account_query_to_df(
        ["Expenses:Employment:*"]
    )
    df_employment_expenses = df_employment_expenses.rename(
        columns={"sum_position": "employment_expenses"}
    )
    return group_by_month(df_employment_expenses, "employment_expenses")


def savings_rate_query() -> pd.DataFrame:
    """
    Gets and merges all the relevant dataframes for savings rate
    """
    df_income: DataFrame = income_query()
    df_expenses = expenses_query()
    df_employment_expenses = employment_expenses_query()
    total_dataframe: DataFrame = pd.merge(df_income, df_expenses, on=["date"])
    total_dataframe = pd.merge(total_dataframe, df_employment_expenses, on=["date"])
    return total_dataframe


def calculate_savings_rate() -> DataFrame:
    # Merge the dataframes together
    total_dataframe: DataFrame = savings_rate_query()

    # Only count relevant expenses
    total_dataframe["income_after_tax"] = (
        total_dataframe["income"] - total_dataframe["employment_expenses"]
    )
    total_dataframe["relevant_expenses"] = (
        total_dataframe["all_expenses"] - total_dataframe["employment_expenses"]
    )

    # Calculate savings amount
    total_dataframe["saving_amount"] = (
        total_dataframe["income_after_tax"] - total_dataframe["relevant_expenses"]
    )
    total_dataframe["saving_rate"] = (
        total_dataframe["saving_amount"] / total_dataframe["income_after_tax"]
    )

    # Calculate savings amount gross
    total_dataframe["saving_amount_gross"] = total_dataframe["income"] - (
        total_dataframe["all_expenses"]
    )
    total_dataframe["saving_rate_gross"] = (
        total_dataframe["saving_amount_gross"] / total_dataframe["income"]
    )

    return total_dataframe


def savings_rate_average() -> Series:
    total_dataframe: DataFrame = calculate_savings_rate()
    return total_dataframe.mean()
