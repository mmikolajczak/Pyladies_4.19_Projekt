# Hello there :)
DATA_PATH = './szwagropol_data/transactions.txt'

with open(DATA_PATH, encoding='utf-8') as f:
    rows = []
    for line in f:
        current_row = line.strip().split(';')
        rows.append(current_row)

for i in range(5):
    print(rows[i])

