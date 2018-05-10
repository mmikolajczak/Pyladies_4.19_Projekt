# Hello there :)
from data_loading import load_data
from helper_functions import create_date


DATA_PATH = './szwagropol_data/transactions.txt'
TRANSACTION_TIME_INDEX = 0
CUSTOMER_INDEX = 1
PRODUCT_NAME_INDEX = 2
CATEGORY_NAME_INDEX = 3
QUANTITY_INDEX = 4
UNIT_PRICE_INDEX = 5
TOTAL_VALUE = 6

columns, rows = load_data(DATA_PATH)
columns.append('total_transaction_values')
for row in rows:
    total = row[QUANTITY_INDEX] * row[UNIT_PRICE_INDEX]
    row.append(total)


def calculate_total_revenue(rows):
    total_revenue = 0
    for row in rows:
        total_revenue += row[TOTAL_VALUE]
    total_revenue = round(total_revenue, 2)
    return total_revenue


total_revenue = calculate_total_revenue(rows)
print(total_revenue)

second_april = rows[0][TRANSACTION_TIME_INDEX]
print(second_april)

year = 2018
month = 4
day = 2
second_april = create_date(year, month, day)


def filter_rows_by_data(rows, date):
    filtered_rows = []
    for row in rows:
        if row[TRANSACTION_TIME_INDEX] == date:
            filtered_rows.append(row)
    return filtered_rows


second_april_rows = filter_rows_by_data(rows, date=second_april)
print('Total revenue in 2nd april:',
      calculate_total_revenue(second_april_rows))


#for i in range(5):
#    print(rows[i])


class DataTable:
    pass
