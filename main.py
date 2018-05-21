# Hello there :)
from data_loading import load_data
from helper_functions import create_date, create_dates_in_range


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


#total_revenue = calculate_total_revenue(rows)
#print(total_revenue)

#second_april = rows[0][TRANSACTION_TIME_INDEX]
#print(second_april)




def filter_rows_by_date(rows, date):
    filtered_rows = []
    for row in rows:
        if row[TRANSACTION_TIME_INDEX] == date:
            filtered_rows.append(row)
    return filtered_rows


#second_april_rows = filter_rows_by_date(rows, date=second_april)
#print('Total revenue in 2nd april:',
#      calculate_total_revenue(second_april_rows))


year = 2018
month = 4
day = 2
second_april = create_date(year, month, day)
sixth_april = create_date(2018, 4, 6)
dates_in_april_first_week = create_dates_in_range(second_april, sixth_april)

# print(dates_in_april_first_week)


revenues = []
for date in dates_in_april_first_week:
    filtered_rows = filter_rows_by_date(rows, date)
    revenue = calculate_total_revenue(filtered_rows)
    revenues.append(revenue)


with open('raport.txt', 'w') as f:
    for i in range(len(revenues)):
        f.write(str(dates_in_april_first_week[i]) + " " +
                str(revenues[i]) + '\n')


#import matplotlib.pyplot as plt


#plt.bar([1, 2, 3, 4, 5], revenues)
#plt.xticks([1, 2, 3, 4, 5], dates_in_april_first_week)
#plt.title('Utarg w pierwszym tygodniu kwietnia')
#plt.show()


def filter_rows(rows, column_index, value):
    filtered_rows = []
    for row in rows:
        if row[column_index] == value:
            filtered_rows.append(row)
    return filtered_rows

# tworzymy liste z unikalnymi nazwami produktow
unique_products_names = []
# iterujemy po naszych wierszach
for row in rows:
    # jezeli na liscie nie ma produktu z wiersza po ktorym aktualnie iterujemy
    if row[PRODUCT_NAME_INDEX] not in unique_products_names:
        # ...to dodajemy go na ta liste
        unique_products_names.append(row[PRODUCT_NAME_INDEX])


# tworzymy słownik, w którym kluczem jest nazwa produkty a wartosci
# calłkowity utarg
revenues_by_product = {}
# iterujemy po unikalnych nazwach produktów
for name in unique_products_names:
# filtrujemy wiersze tak zeby otrzymac tylko te, ktorych nazwa produktu jest
# taka jak ta po ktorej aktualnie iterujemy
    filtered_rows = filter_rows(rows, PRODUCT_NAME_INDEX, name)
    # dla tych wierszy liczymy utarg
    product_revenue = calculate_total_revenue(filtered_rows)
    # umieszczamy obliczony utarg (i nazwe produktu) w slowniku
    revenues_by_product[name] = product_revenue

#print(revenues_by_product)

from helper_functions import sort_dict_by_values
sorted_product_names = sort_dict_by_values(revenues_by_product)
print(sorted_product_names[-5:])






class DataTable:
    pass
