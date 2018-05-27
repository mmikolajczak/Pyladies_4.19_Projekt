# Hello there :)
import matplotlib.pyplot as plt
from data_loading import load_data
from helper_functions import create_date, create_dates_in_range
from helper_functions import sort_dict_by_values


def filter_rows(rows, column_index, value):
    filtered_rows = []
    for row in rows:
        if row[column_index] == value:
            filtered_rows.append(row)
    return filtered_rows


def calculate_total_revenue(rows):
    total_revenue = 0
    for row in rows:
        total_revenue += row[TOTAL_VALUE]
    total_revenue = round(total_revenue, 2)
    return total_revenue


def filter_rows_by_date(rows, date):
    filtered_rows = []
    for row in rows:
        if row[TRANSACTION_TIME_INDEX] == date:
            filtered_rows.append(row)
    return filtered_rows


class DataTable:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def filter_rows(self, column_index, value):
        filtered_rows = []
        for row in self.rows:
            if row[column_index] == value:
                filtered_rows.append(row)
        return filtered_rows

    def get_column(self, column_index):
        column_values = []
        for row in self.rows:
            column_values.append(row[column_index])
        return column_values

    def get_row(self, row_index):
        return self.rows[row_index]


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

dataset = DataTable(rows, columns)


# pierwsza funkcjonalność
second_april = create_date(2018, 4, 2)
sixth_april = create_date(2018, 4, 6)
dates_in_april_first_week = create_dates_in_range(second_april, sixth_april)

revenues = []
for date in dates_in_april_first_week:
    filtered_rows = dataset.filter_rows(TRANSACTION_TIME_INDEX, date)
    revenue = calculate_total_revenue(filtered_rows)
    revenues.append(revenue)


with open('raport.txt', 'w') as f:
    for i in range(len(revenues)):
        f.write(str(dates_in_april_first_week[i]) + " " +
                str(revenues[i]) + 'zł\n')


plt.bar([1, 2, 3, 4, 5], revenues)
plt.xticks(list(range(1, len(revenues) + 1)), dates_in_april_first_week)
plt.title('Utarg w pierwszym tygodniu kwietnia')
plt.show()

# trzecia na liście funkcjonalność

# przerobić na funkcje poniższy kod, tak aby można było wyspecyfikować
# po jakiej kolumnie filtrujemy
def unique_values(rows, column_index):
    unique_values = []
    for row in rows:
        if row[column_index] not in unique_values:
            unique_values.append(row[column_index])
    return unique_values

unique_products_names = unique_values(dataset.rows, PRODUCT_NAME_INDEX)

revenues_by_product = {}
for name in unique_products_names:
    filtered_rows = dataset.filter_rows(PRODUCT_NAME_INDEX, name)
    product_revenue = calculate_total_revenue(filtered_rows)
    revenues_by_product[name] = product_revenue

sorted_product_names = sort_dict_by_values(revenues_by_product)
print('Najlepiej sprzedające produkty:',sorted_product_names[-5:])

# funkcjonalnosc nr 2.
# chcemy otrzymać słownik w którym kluczem będzie kategoria a wartością
# utarg dla niej
# uzyskać uniklane kategorie (mamy do tego funkcje)
unique_categories_names = unique_values(dataset.rows, CATEGORY_NAME_INDEX)
# stworzyć słownik
categories_revenue_share = {}
total_revenue = calculate_total_revenue(dataset.rows)
# dla każdej unikalnej kategorii
for name in unique_categories_names:
    # filtrujemy po niej wiersze
    filtered_rows = dataset.filter_rows(CATEGORY_NAME_INDEX, name)
    # dla przefiltrowanych wierszy obliczamy utarg
    category_revenue = calculate_total_revenue(filtered_rows)
    # i przypisujemy go do naszego słownika
    categories_revenue_share[name] = round(category_revenue / total_revenue, 2)

# print(categories_revenue_share)
plt.pie(list(categories_revenue_share.values()),
        labels=list(categories_revenue_share.keys()), autopct='%.0f%%')
plt.title('Udział kategorii w utargu')
plt.show()


# bonus: czwarta funkcjonalność - wysyłanie emaili
from helper_functions import GmailEmailSender


class SpamSender(GmailEmailSender):

    def generate_message_content(self, product_name):
        ad_text = 'Super oferta, tylko, teraz, musisz kupic nasz {}!!!1!1!'.format(
            product_name)
        return ad_text


spam_sender = SpamSender('zbyszek.nowak.fejkmejl@gmail.com', 'Pyladies2018')
spam_sender.send_mail('zbyszek.nowak.fejkmejl@gmail.com', 'Kalafior Krzys')
print('done')

