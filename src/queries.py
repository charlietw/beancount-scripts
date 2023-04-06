import subprocess
import pandas as pd
from io import StringIO
from src import functions


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
    query_result_df['sum_position'] = functions.fix_currency_column(query_result_df['sum_position'])
    query_result_df = functions.convert_to_datetime(query_result_df)
    max_date: str = query_result_df["date"].max()
    return functions.pad_dates(query_result_df, "2020-01-01", max_date)


def bean_query(query) -> str:
    """
    Queries beancount and returns the result as a string
    """
    args: list[str] = [
        "bean-query",
        "-f",
        "csv",
        "/Users/charlie.wren/Documents/projects/personal/ledger/budget.beancount",
        query,
    ]
    proc = subprocess.run(args, capture_output=True, check=True)
    return proc.stdout.decode("utf-8")


def income_query() -> pd.DataFrame:
    df_income: pd.DataFrame = account_query_to_df(['Income:*'])
    df_income['sum_position'] = df_income['sum_position'] * -1 # need to reverse the income
    df_income = df_income.rename(columns={"sum_position": "income"})
    return df_income
    

def expenses_query() -> pd.Series:
    df_expenses: pd.DataFrame = account_query_to_df(['Expenses:*'])
    df_expenses = df_expenses.rename(columns={"sum_position": "all_expenses"})
    return functions.group_by_month(df_expenses, "all_expenses")


def employment_expenses_query() -> pd.Series:
    df_employment_expenses: pd.DataFrame = account_query_to_df(['Expenses:Employment:*'])
    df_employment_expenses = df_employment_expenses.rename(columns={"sum_position": "employment_expenses"})
    return functions.group_by_month(df_employment_expenses, "employment_expenses")


def savings_rate_query() -> pd.DataFrame:
    """
    Gets and merges all the relevant dataframes for savings rate
    """
    df_income: DataFrame = income_query()
    df_expenses = expenses_query()
    df_employment_expenses = employment_expenses_query()
    total_dataframe: DataFrame = pd.merge(df_income, df_expenses, on=['date'])
    total_dataframe = pd.merge(total_dataframe, df_employment_expenses, on=['date'])
    return total_dataframe

print(savings_rate_query())