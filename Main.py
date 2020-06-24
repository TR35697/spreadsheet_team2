import csv
import pandas as pd
import matplotlib.pyplot as plt

pd.read_csv('nyc-rolling-sales.csv')
# -------read all data into pandas dataframe, filter data and define month.-----------
with open('nyc-rolling-sales.csv', 'r') as csv_file:
    spreadsheet = csv.DictReader(csv_file)
    # converts CSV into pd dataframe that only contains borough, sale date and price
    df = pd.DataFrame(spreadsheet, columns=['BOROUGH', 'SALE DATE', 'SALE PRICE'])
    # Replace ' -  ' by '0'
    df.replace(to_replace=' -  ', value='0', inplace=True)
    # delete time from date
    df['SALE DATE'] = df['SALE DATE'].str.split(" ").str[0]
    # print(df)
    # add new month column
    df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])
    # sort data frame by date
    df = df.sort_values(by='SALE DATE', ascending=True)
    df['SALE PRICE'] = df['SALE PRICE'].astype(float)
    # filter all prices to delete values of sales price under 100, boolean indexing (basically if statements with
    # pandas)
    df = df[(df['SALE PRICE'] > 100)]

    # --------------Initial Output------------------
    # sum all prices
    price_sum = df['SALE PRICE'].sum()
    print('sum of all sale prices: {}'.format(str(price_sum)))
    # create a list with all the sales
    sales_list = df['SALE PRICE'].to_list()
    print(sales_list)


# ---------------------Define Functions-----------------------

def user_input_specific_month():
    question = input('Do you want to see sales for a specific month? yes/ no ')
    if question == 'yes':
        month_int = int(input('For which month do you want to see sales? 1-12 '))
        month_df = df[df["SALE DATE"].dt.month == month_int]
        print(month_df)
    else:
        print('ok')


def perform_analysis():
    # Resample dataframe to monthly values and save as new dataframe
    # we need sale price, total sold and average house price
    # on='SALE DATE' means we use SALE DATE as an index
    results_count = df.resample('M', on='SALE DATE').count()['SALE PRICE']
    results_avg = df.resample('M', on='SALE DATE').mean()['SALE PRICE']
    results_sum = df.resample('M', on='SALE DATE').sum()['SALE PRICE']
    # add columns together into result data frame
    res = pd.concat(
        [results_count.rename("total sold"), results_avg.rename("average price"), results_sum.rename("total sales")],
        axis=1)

    # add percentage changes
    res['% change houses sold'] = res['total sold'].pct_change()
    res['% change avg price'] = res['average price'].pct_change()
    res['% change total sales'] = res['total sales'].pct_change()
    # remove day in date and change date to string that way
    res['month'] = res.index.strftime(date_format="%Y-%m")
    return res


def write_to_csv(summary_df):
    summary_df.to_csv(path_or_buf="sum.csv")
    with open('sum.csv', 'a') as csv_file:
        # write summary information under table
        if highest_total_sales_row['month'] != highest_average_price_row['month'] and highest_average_price_row[
            'month'] != highest_sold_row['month'] and highest_total_sales_row['month'] != \
                highest_average_price_row['month']:
            information = [[" ", " "], [" ", "The month with the highest total sales is {}".format(
                highest_total_sales_row['month'])],
                           [" ", "The month with the highest average price is {}".format(
                               highest_average_price_row['month'])],
                           [" ",
                            "The month with the highest number of houses sold is {}".format(highest_sold_row['month'])]]
        elif highest_total_sales_row['month'] == highest_average_price_row['month'] and highest_total_sales_row[
            'month'] == highest_sold_row['month']:
            information = [[" ", " "],
                           [" ", "{} has the highest total sales, highest average price, and highest number "
                                 "of houses sold.".format(highest_total_sales_row['month'])]]
        elif highest_total_sales_row['month'] == highest_average_price_row['month']:
            information = [[" ", " "], [" ", "{} has the highest total sales and the highest average price.\
             ".format(highest_total_sales_row['month'])], [" ",
                                                           "The month with the highest number of houses sold is {}".format(
                                                               highest_sold_row['month'])]]
        elif highest_total_sales_row['month'] == highest_sold_row['month']:
            information = [[" ", " "],
                           [" ", "{} has the highest total sales and highest number "
                                 "of houses sold.".format(highest_total_sales_row['month'])],
                           [" ",
                            "The month with the highest average price is {}".format(
                                highest_average_price_row['month'])],
                           ]
        elif highest_sold_row['month'] == highest_average_price_row['month']:
            information = [[" ", " "],
                           [" ", "{} has the highest average price and highest number \
                                              of houses sold.".format(highest_sold_row['month'])],
                           [" ",
                            "The month with the highest total sales is {}".format(highest_total_sales_row['month'])]
                           ]
        writer = csv.writer(csv_file)
        writer.writerows(information)


def user_input_graph():
    graph = input('Would you like to see the data presented in a graph? (Yes/No) ')
    if graph == 'Yes':
        print('Here you go!')
    # line plot for multiple columns
    # had to include reset_index() because we made sale date an index when joining the data frames
    ax = plt.gca()
    summary_df.reset_index().plot(kind='line', x='SALE DATE', y='% change houses sold', ax=ax)
    summary_df.reset_index().plot(kind='line', x='SALE DATE', y='% change avg price', color='red', ax=ax)
    summary_df.reset_index().plot(kind='line', x='SALE DATE', y='% change total sales', color='black', ax=ax)
    if graph == 'Yes':
        plt.show()
    # make this an else statement?
    else:
        print('Okay.')


user_input_specific_month()
summary_df = perform_analysis()
print(summary_df)

highest_sold_row = summary_df.loc[summary_df['total sold'].idxmax()]
highest_total_sales_row = summary_df.loc[summary_df['total sales'].idxmax()]
highest_average_price_row = summary_df.loc[summary_df['average price'].idxmax()]

write_to_csv(summary_df)
user_input_graph()
