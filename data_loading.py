from helper_functions import parse_date_from_string


def load_data(path):
    with open(path, encoding='utf-8') as f:
        rows = []
        columns = f.readline().strip().split(';')
        for line in f:
            current_row = line.strip().split(';')
            current_row[0] = parse_date_from_string(current_row[0])
            current_row[-2] = int(current_row[-2])
            try:
                current_row[-1] = float(current_row[-1])
            except ValueError:
                continue
            rows.append(current_row)
    return columns, rows

