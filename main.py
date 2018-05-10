# Hello there :)
from data_loading import load_data  # importujemy wykorzystwane funkcje do ładowania danych/tworzenia dat z odpowiednich modułów
from helper_functions import create_date


DATA_PATH = './szwagropol_data/transactions.txt'  # zmienna, pod którą przechowywana jest ścieżka z danymi. Zapisanie nazwy zmiennej
                                                  # w całości wielkimi literami jest konwencją (ogólnie stosowaną), do oznaczania
                                                  # stałych (zmiennych, których wartość nie powinna się w trakcie wykonywania
                                                  # programu zmieniać)
TRANSACTION_TIME_INDEX = 0
CUSTOMER_INDEX = 1
PRODUCT_NAME_INDEX = 2
CATEGORY_NAME_INDEX = 3
QUANTITY_INDEX = 4
UNIT_PRICE_INDEX = 5
TOTAL_VALUE_INDEX = 6  # zmienne (stałe), przy pomocy których zapisujemy pod którym indeksem znajdują się konkretne informacje
                       # przechowywane w wierszach  danych - zwiększając przy tym czytelność kodu

columns, rows = load_data(DATA_PATH)  # wczytujemy listę kolumn i listę wierszy z pliku - przy pomocy wcześniej
                                      # stworzonej, i zaimportowanej funkcji load_data
columns.append('total_transaction_values')  # dodajemy dodatkową kolumnę, która będzie zawierać łączną wartość danego wiersza.
                                            # początkowo w wierszu zawarta jest liczba sztuk kupionego produktu i cena/sztukę,
                                            # zapisując sobie wynik mnożenia tych wartości w dodatkowej kolumnie unikniemy
                                            # wymnażania tych wartości wielokrotnie
for row in rows:  # dla każdego z wczytanych wierszy
    total = row[QUANTITY_INDEX] * row[UNIT_PRICE_INDEX]  # wylicz całkowitą wartość danej transakcji, mnożąc liczbę sztuk * cenna/sztukę...
    row.append(total)  # ... i dodaj obliczony wynik na końcu wiersza


def calculate_total_revenue(rows):  # funkcja do obliczania wartości całkowitego utargu w przekazanych wierszach z transakcjami
    total_revenue = 0  # inicjalizuemy zmienną, która będzie zawierała całkowity utarg
    for row in rows:  # iterujemy po każdym z przekazanych wierszy
        total_revenue += row[TOTAL_VALUE_INDEX]  # dodajemy do zmiennej pomocniczej, w której trzymamy całkowity utarg
                                                 # wartość zamówienia po którym aktualnie iterujemy
    total_revenue = round(total_revenue, 2)  # zaokrąglamy wynik do dwóch miejsc po przecinku (głównie ze względów wizualnych)
    return total_revenue  # zwracamy obliczony utarg całkowity


total_revenue = calculate_total_revenue(rows)  # przykład użycia naszej funkcji do obliczania utargu - wykonujemy ją na
                                               # świeżo wczytanych wierszach (czyli wszystkich danych z pliku)
print(total_revenue)


year = 2018
month = 4
day = 2
second_april = create_date(year, month, day)  # tworzymy obiekt date, przy pomocy jednej z funkcji pomocniczych (wcześniej zaimportowana)


def filter_rows_by_date(rows, date):  # funkcja, służąca do filtrowania wierszy tak, aby uzyskać tylko te z przekazanego
                                      # w drugim argumencie dnia (obiektu typu date)
    filtered_rows = []  # inicjalizujemy pustą listę na wiersze które spełnią warunki filtracji
    for row in rows:  # dla każdego wiersza z przekazanych w argumencie
        if row[TRANSACTION_TIME_INDEX] == date:  # jeśli spełniony jest warunek filtracji (data w wierszu jest zgodna z przekazaną)...
            filtered_rows.append(row)  # ... to dodaj aktualny wiersz do listy na wiersze przefiltrowane
    return filtered_rows  # zwracamy wynik - przefiltrowane wiersze


second_april_rows = filter_rows_by_date(rows, date=second_april)  # przykładowe wywołanie funkcji filtrującej - tworzymy
                                                                  # nową zmienną, w której są tylko transakcje z drugiego lutego
print('Total revenue in 2nd april:',
      calculate_total_revenue(second_april_rows))  # tym razem obliczamy utarg tylko dla transakcji wcześniej przefiltrowanych - z
                                                   # drugiego kwietnia. warto zwrócić uwagę, że dzięki zamknięciu tej funkcjonalności
                                                   # wystarczy nam do tego napisanie tylko jednej linii - nie musimy ponownie
                                                   # pisać 5 linii i całej sumującej pętli


#for i in range(5):  # wyświetlanie pierwszych pięciu wierszy z wczytanych danych - w ten sposób sprawdzaliśmy poprawność
#    print(rows[i])  # naszych działań


class DataTable:  # deklaracja klasy (chwilowo pustej, tylko dla przypomnienia składni)
    pass  # pass - słowo kluczowe, które dosłownie "nic" nie robi - natomiast w tym przypadku zapobiega błędom wynikającym
          # z braku wymaganego wcięcia
