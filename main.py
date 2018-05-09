# Hello there :)
from data_loading import load_data


DATA_PATH = './szwagropol_data/transactions.txt'

columns, rows = load_data(DATA_PATH)


for i in range(5):
    print(rows[i])


class DataTable:
    pass
