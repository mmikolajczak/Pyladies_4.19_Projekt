# Hello there :)
import matplotlib.pyplot as plt  # importujemy moduł do generacji wykresów/wizualizacji. nie jest on dostarczony w "czsytym"
                                 # Pythonie i musieliśmy go wcześniej doinstalować (wskazówki jak to zrobić znajdują się w prezentacji).
                                 # dodatkowo, aby skrócić nazwę którą posługujemy się przy wywoływaniu modułu używamy "as"
                                 # i nadajemy jej alias.
from data_loading import load_data  # importujemy wykorzystwane do ładowania danych/tworzenia dat funkcje z lokalnych modułów
from helper_functions import create_date, create_dates_in_range
from helper_functions import sort_dict_by_values


DATA_PATH = './szwagropol_data/transactions.txt' # zmienna, pod którą przechowywana jest ścieżka z danymi. Zapisanie nazwy zmiennej
                                                  # w całości wielkimi literami jest konwencją (ogólnie stosowaną), do oznaczania
                                                  # stałych (zmiennych, których wartość nie powinna się w trakcie wykonywania
                                                  # programu zmieniać)
TRANSACTION_TIME_INDEX = 0
CUSTOMER_INDEX = 1
PRODUCT_NAME_INDEX = 2
CATEGORY_NAME_INDEX = 3
QUANTITY_INDEX = 4
UNIT_PRICE_INDEX = 5
TOTAL_VALUE = 6  # zmienne (stałe), przy pomocy których zapisujemy pod którym indeksem znajdują się konkretne informacje
                 # przechowywane w wierszach  danych - zwiększając przy tym czytelność kodu

columns, rows = load_data(DATA_PATH)  # wczytujemy listę kolumn i listę wierszy z pliku - przy pomocy wcześniej
                                      # stworzonej, i zaimportowanej funkcji load_data

columns.append('total_transaction_values')  # dodajemy dodatkową kolumnę, która będzie zawierać łączną wartość danego wiersza.
                                            # początkowo w wierszu zawarta jest liczba sztuk kupionego produktu i cena/sztukę,
                                            # zapisując sobie wynik mnożenia tych wartości w dodatkowej kolumnie unikniemy
                                            # wymnażania tych wartości wielokrotnie

for row in rows:                                         # dla każdego z wczytanych wierszy
    total = row[QUANTITY_INDEX] * row[UNIT_PRICE_INDEX]  # wylicz całkowitą wartość danej transakcji, mnożąc liczbę sztuk * cenna/sztukę...
    row.append(total)                                    # ... i dodaj obliczony wynik na końcu wiersza
                                                         # (w zasadzie dobrym pomysłem mogłoby być przeniesienie tego framentu
                                                         # do funkcji wczytującej dane)


def calculate_total_revenue(rows):  # funkcja do obliczania wartości całkowitego utargu w przekazanych wierszach z transakcjami
    total_revenue = 0               # inicjalizuemy zmienną, która będzie zawierała całkowity utarg
    for row in rows:                # iterujemy po każdym z przekazanych wierszy
        total_revenue += row[TOTAL_VALUE]  # dodajemy do zmiennej pomocniczej, w której trzymamy całkowity utarg
                                           # wartość zamówienia po którym aktualnie iterujemy
    total_revenue = round(total_revenue, 2) # zaokrąglamy wynik do dwóch miejsc po przecinku (głównie ze względów wizualnych)
    return total_revenue                    # zwracamy obliczony utarg całkowity


def filter_rows_by_date(rows, date):  # funkcja, służąca do filtrowania wierszy tak, aby uzyskać tylko te z przekazanego
                                      # w drugim argumencie dnia (obiektu typu date)
    filtered_rows = []                # inicjalizujemy pustą listę na wiersze które spełnią warunki filtracji
    for row in rows:                  # dla każdego wiersza z przekazanych w argumencie
        if row[TRANSACTION_TIME_INDEX] == date:  # jeśli spełniony jest warunek filtracji (data w wierszu jest zgodna z przekazaną)...
            filtered_rows.append(row)            # ... to dodaj aktualny wiersz do listy na wiersze przefiltrowane
    return filtered_rows              # zwracamy wynik - przefiltrowane wiersze


def filter_rows(rows, column_index, value):  # ulepszona wersja powyższej fukcji - którą rozszerzyliśmy tak, aby móc
                                             # filtrować po każdej z możliwych kolumn przy pomocy tylko jednej funkcji.
                                             # kolumne po ktorej filtrujemy okreslamy jednym z parametrów.

    filtered_rows = []                       # funkcja działa identycznie jak wcześniejsza...
    for row in rows:
        if row[column_index] == value:       # ... zmieniło się tylko to porównanie - nie używamy już stałego indeksu
                                             # kolumny, a ten przekazany w paramterze.
            filtered_rows.append(row)
    return filtered_rows


# tu przechodzimy do czynów (mamy już dane i parę przydatnych funckji) - realizujemy pierwszą funkcjonalność czyli
# liczymy utarg poszczególnych dni w przedziale (a potem generujemy/prezentujemy wyniki)

# (testy przeprowadzamy na pierwszym tygodniu kwietnia)
second_april = create_date(2018, 4, 2)  # tworzymy obiekt date, przy pomocy jednej z funkcji pomocniczych (wcześniej zaimportowana)
sixth_april = create_date(2018, 4, 6)
dates_in_april_first_week = create_dates_in_range(second_april, sixth_april)  # tworzymy listę dat w danym przedziale,
                                                                              # znowu korzystając z pomocniczej funkcji

# mamy już listę poszczególnych dni w danym przedziale -  teraz musimy policzyć same utargi
revenues = []  # tworzymy pustą listę na obliczone utargi
for date in dates_in_april_first_week:  # dla każdej daty w naszej otrzymanej liście dni
    filtered_rows = filter_rows_by_date(rows, date)  # filtrujemy wiersze, tak aby otrzymać tylko te z dnia,
                                                     # po którym aktualnie iterujemy
    revenue = calculate_total_revenue(filtered_rows) # obliczamy utarg w rekordach będących wynikiem filtracji
    revenues.append(revenue) # i dodajemy utarg wynikowy z danego dnia do listy wyników


# pierwsza wersja przedstawienia wyników użytkownikowi, przy pomocy raportu w pliku tekstowym
# w postaci data(spacja)utarg(zł), a każdy kolejny wynik jest w osobnej linii
with open('raport.txt', 'w') as f:  # otwieramy plik w trybie do zapisu (w). dzieki temu ze korzystamy z with nie musimy
                                    # "ręcznie" zamykać pliku
    for i in range(len(revenues)):  # dla kolejnych i w przedziale od 0 do liczby elementów w liście z utargami - 1
        f.write(str(dates_in_april_first_week[i]) + " " +  # zapisz obecny wynik (dzień/utarg) w opisanym wyżej formacie do pliku
                str(revenues[i]) + 'zł\n')


# niestety, prezesowi nie spodobała się pierwsza forma wyniku - wygenerujemy mu więc wynik w ładniejszej, graficznej formie
plt.bar([1, 2, 3, 4, 5], revenues)  # generujemy wykres słupkowy, pierwszy parametr to lista współrzędnych poszczególnych
                                    # słupków, a drugi parametr to lista ich wysokości (obie muszą mieć tą samą liczbę elementów)
plt.xticks(list(range(1, len(revenues) + 1)), dates_in_april_first_week)  # ustawiamy podpisy dla poszczególnych słupków, pierwszym parametrem
                                                                   # jest ponownie lista współrzędnych (ale generujemy ją
                                                                   # innym, bardziej uniwersalnym sposobem), drugim argumentem
                                                                   # są same podpisy
plt.title('Utarg w pierwszym tygodniu kwietnia')  # ustawiamy tytuł wykresu
plt.show()  # wywołujemy show, aby wyświetlić przygotowany wykres

# voila - pierwsza funkcjonalność gotowa - teraz zajmiemy się następną (trzecią na lisćie) - wygenerowaniem 5 najlepiej
# sprzedających się produktów


# w tym celu potrzebna nam będzie najpierw lista z unikalnymi nazwami produktow

unique_products_names = []  # stwórzmy więc na wspomniane unikalmne nazwy nową listę
for row in rows:  # iterujemy po wszystkich transakcjach
    if row[PRODUCT_NAME_INDEX] not in unique_products_names: # jezeli na liscie unikalnych nazw nie ma nazwy produktu z
                                                             #  wiersza po ktorym aktualnie iterujemy...
        unique_products_names.append(row[PRODUCT_NAME_INDEX]) #...to dodajemy go na wspomnianą liste


# następnym krokiem jest swtorzenie słownika, w którym kluczem jest nazwa produktu a wartoscia calłkowity utarg
revenues_by_product = {}
for name in unique_products_names:  # iterujemy po unikalnych nazwach produktów
    filtered_rows = filter_rows(rows, PRODUCT_NAME_INDEX, name)  # filtrujemy wiersze tak zeby otrzymac tylko te, ktorych
                                                                 # nazwa produktu jest taka jak ta po ktorej aktualnie iterujemy

    product_revenue = calculate_total_revenue(filtered_rows)     # dla przefiltrowanych wierszy (tylko te z aktualnym produktem)
                                                                 #  liczymy utarg
    revenues_by_product[name] = product_revenue  # umieszczamy obliczony utarg (i nazwe produktu) w slowniku


sorted_product_names = sort_dict_by_values(revenues_by_product)  # następnie korzytamy z kolejnej funkcji pomocniczej,
                                                                 # aby uzyskać klucze słownika posortowane według wartości
                                                                 # uwaga: jak widać w przykładzie w module z którego importujemy
                                                                 # funkcję, wynik jest posortowany rosnąco, od najmniejszej
                                                                 # do największej wartości

print(sorted_product_names[-5:])  # wypisujemy wynik - ostatnie 5 wartości z posortowanej listy


class DataTable:  # deklaracja klasy (chwilowo pustej, tylko dla przypomnienia składni)
    pass  # pass - słowo kluczowe, które dosłownie "nic" nie robi - natomiast w tym przypadku zapobiega błędom wynikającym
          # z braku wymaganego wcięcia
