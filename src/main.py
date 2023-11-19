from src import functions, connector
import pandas as pd


if __name__ == "__main__":
    measurement_name: str = "finance"
    bucket_name: str = "python"
    assets = [
        "Assets:BankAccounts:Monzo",
        "Assets:BankAccounts:HSBC",
        "Assets:BankAccounts:MarcusSavings",
        "Assets:BankAccounts:CryptoCard",
        "Assets:Investments:MoneyboxLISA",
        "Assets:Investments:StocksSharesISA",
        "Assets:Investments:Crypto",
        "Assets:Property:6CommonRoad",
        "Liabilities:StudentLoan",
        "Liabilities:Amex"
    ]
    df: pd.DataFrame = functions.balance_query_to_df(["Assets:Investments:MoneyboxLISA"])

    connector.clear_bucket(measurement_name, bucket_name)
    # Upload savings rate data
    savings_rate_df: pd.DataFrame = functions.calculate_savings_rate()
    expenses_fields = ['relevant_expenses', 'saving_rate']
    expenses_tags = [
        {
            'tag_name': 'expenses',
            'tag_value': 'savings_rate'
        }
        ]
    print("Uploading savings rate data...")
    connector.write_to_influx(savings_rate_df, bucket_name, measurement_name, expenses_fields, expenses_tags)
    # Upload balance data
    for asset in assets:
        print("Uploading {0} data...".format(asset))
        df: pd.DataFrame = functions.balance_query_to_df([asset])
        balance_fields = ['balance']
        balance_tags = [
            {
                'tag_name': 'account',
                'tag_value': asset
            }
            ]
        connector.write_to_influx(df, bucket_name, measurement_name, balance_fields, balance_tags)

   # connector.write_to_influx(savings_rate_df, bucket_name, measurement_name)
