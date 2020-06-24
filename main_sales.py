import csv
import pandas as pd

pd.read_csv('sales.csv')
# -------read all data into pandas dataframe, filter data and define month.-----------
with open('sales.csv', 'r') as csv_file:
    spreadsheet = csv.DictReader(csv_file)
    # converts CSV into pd dataframe that contains year, month, sales and expenditure
    df = pd.DataFrame(spreadsheet, columns=['year', 'month', 'sales', 'expenditure'])
    # turn sales column values from string into int
    df['sales'] = df['sales'].astype(float)
    df['expenditure'] = df['expenditure'].astype(float)
    # create a list with all the sales from each month
    sales_list = df['sales'].to_list()
    print(sales_list)
    # output total sales across all months
    total_sales = df['sales'].sum()
    print("total sales across all months was {}".format(total_sales))

    # --- extra functions
    # percentage changes
    df['% change sales'] = df['sales'].pct_change()
    df['% change expenditures'] = df['expenditure'].pct_change()

    print(df)
