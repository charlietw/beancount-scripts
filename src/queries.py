import subprocess
import pandas as pd
from io import StringIO

def construct_account_query(accounts) -> str:
    query = "SELECT MONTH(date) AS month, YEAR(date) as year, sum(position), account "
    for i, account in enumerate(accounts):
        if i == 0: # First account has to be WHERE
            query += f"WHERE account ~ '{account}' "
        else: # Rest have to be OR
            query += f"OR account ~ '{account}' "
    query += "GROUP BY year, month, account"
    return query


def account_query(accounts) -> pd.DataFrame:
    query: str = construct_account_query(accounts)
    query_result: str = bean_query(query)
    return pd.read_csv(StringIO(query_result))


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
    return proc.stdout.decode('utf-8')



