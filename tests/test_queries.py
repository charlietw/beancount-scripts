from src import functions


def test_construct_account_query() -> None:
    expected: str = "SELECT MONTH(date) AS month, YEAR(date) as year, sum(position), account WHERE account ~ 'Expenses:*' GROUP BY year, month, account"
    accounts: list[str] = ["Expenses:*"]
    actual: str = functions.construct_account_query(accounts)
    assert expected.strip() == actual.strip()


def test_construct_multiple_account_query() -> None:
    expected: str = "SELECT MONTH(date) AS month, YEAR(date) as year, sum(position), account WHERE account ~ 'Expenses:*' OR account ~ 'SomethingElse:*' GROUP BY year, month, account"
    accounts: list[str] = ["Expenses:*", "SomethingElse:*"]
    actual: str = functions.construct_account_query(accounts)
    assert expected.strip() == actual.strip()
