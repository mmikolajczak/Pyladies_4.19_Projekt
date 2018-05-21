# kod odpowiadający za wczytywanie danych, przeniesiony do osobnego modułu i funkcji (w celu większego uporządkowania kodu/projektu)
from helper_functions import parse_date_from_string  # import funkcji pomocniczej do konwersji łańcucha znaków
                                                     # na obiekt klasy date


def load_data(path):  # funkcja którą ładujemy dane i konwertujemy ją na odpowiednie typy z postaci stringowej
    with open(path, encoding='utf-8') as f:  # otwieramy plik (with zapewnia nam jego automatyczne zamknięcie)
        rows = []  # inicjalizujemy listę, w której będziemy przechowywać wczytane wiersze
        columns = f.readline().strip().split(';')  # wczytujemy kolumny z pliku z danymi (pozbywamy się białych znaków
                                                   # przy pomocy strip(), a następnie rozdzielamy wartości według średnika - split(';')
        for line in f:  # iterujemy po pozostałych liniach pliku
            current_row = line.strip().split(';')  # potępujemy analogicznie jak w przypadku kolumn
            current_row[0] = parse_date_from_string(current_row[0])  # używamy zaimportowanej funkcji, aby przekonwertować
                                                                     # pierwszy element w wierszu (czas transakcji) na datę
            current_row[-2] = int(current_row[-2])  # przedostatni wiersz (ilość sztuk produktu) konwertujemy na liczbę całkowitą
            try:
                current_row[-1] = float(current_row[-1])  # konwertujemy ostatnią wartość wiersza (cena/sztukę) na wartość zmiennoprzecinkową
            except ValueError:  # przy pomocy try/except zabezpieczamy się przed ewentualnym wystąpieniem ceny która
                                # nie jest liczbą (np. napis FOR FREE, pojawia się w niektórych rekordach) i błędem konwersji
                continue  # jeśli taki błąd wystąpi, przerwyamy iterację dla obecnej linii, i przechodzimy do następnej...
            rows.append(current_row)  # ...w innym przypadku (pomyślna konwersja), dodajemy przygotowany wiersz do naszej listy
    return columns, rows  # po zakończeniu pętli, zwracamy wczytane kolumny oraz przygotowane wiersze

