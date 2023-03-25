import pandas as pd
from pandas import DataFrame


# def convert_datetime_fill_dates(filename, expenses_column_name) -> DataFrame:
#     # Load the dataset into a pandas DataFrame
#     df = pd.read_csv(filename)

#     # Create a new DataFrame with all possible month-year combinations
#     min_date = "2020-01-01"
#     max_date = df["date"].max()
#     all_months: DataFrame = create_month_year_dataframe(min_date, max_date)

#     # Merge the original DataFrame with the new DataFrame
#     df = pd.merge(all_months, df, on=["month", "year"], how="left")

#     # # Use forward-fill to fill in missing values
#     # df['last_balance'].fillna(method='ffill', inplace=True)
#     # df['last_balance'].fillna("0", inplace=True)

#     df: DataFrame = df.drop(columns=["month", "year", "date_y"])

#     # Remove GBP
#     df = remove_currency_symbol(df, "sum_position")


#     df = df.rename(columns={"date_x": "date", "sum_position": expenses_column_name})
#     return df


# def calculate_savings_rate(
#         exclude_holidays: bool) -> None:
#     # Get income
#     df_income = convert_datetime_fill_dates('income.csv', "income")
#     # Make income a positive number rather than negative
#     df_income['income'] = df_income['income'] * -1

#     # Get expenses
#     df_expenses = convert_datetime_fill_dates('expenses.csv', "all_expenses")

#     # Remove whitespace from account
#     df_expenses['account'] = df_expenses['account'].str.replace(' ', '')

#     # Filter out holidays if requested
#     if exclude_holidays:
#         df_expenses = df_expenses[(df_expenses['account'].str.startswith("Expenses:Holidays:") == False)]

#     # Get employment expenses
#     df_employment_expenses = convert_datetime_fill_dates('expenses_employment.csv', "employment_expenses")

#     # Group by date i.e. remove the 'account'
#     df_expenses = df_expenses.groupby(df_expenses['date'])['all_expenses'].sum()
#     df_employment_expenses = df_employment_expenses.groupby(df_employment_expenses['date'])['employment_expenses'].sum()

#     # Merge the dataframes together
#     total_dataframe = pd.merge(df_income, df_expenses, on=['date'])
#     total_dataframe = pd.merge(total_dataframe, df_employment_expenses, on=['date'])

#     # Only count relevant expenses
#     total_dataframe['income_after_tax'] = total_dataframe['income'] - total_dataframe['employment_expenses']
#     total_dataframe['relevant_expenses'] = total_dataframe['all_expenses'] - total_dataframe['employment_expenses']

#     # Calculate savings amount
#     total_dataframe['saving_amount'] = total_dataframe['income_after_tax'] - total_dataframe['relevant_expenses']
#     total_dataframe['saving_rate'] = total_dataframe['saving_amount'] / total_dataframe['income_after_tax']

#     # Calculate savings amount gross
#     total_dataframe['saving_amount_gross'] = total_dataframe['income'] - (total_dataframe['all_expenses'])
#     total_dataframe['saving_rate_gross'] = total_dataframe['saving_amount_gross'] / total_dataframe['income']


#     # Export to CSV
#     total_dataframe.to_csv('savings_rate.csv', index=False)

#     # Get averages
#     total_dataframe_average = total_dataframe.mean()
#     print(total_dataframe_average)

# calculate_savings_rate(exclude_holidays = True)
