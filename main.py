# Hello there :)
import matplotlib.pyplot as plt  # importujemy moduł do generacji wykresów/wizualizacji. nie jest on dostarczony w "czsytym"
                                 # Pythonie i musieliśmy go wcześniej doinstalować (wskazówki jak to zrobić znajdują się w prezentacji).
                                 # dodatkowo, aby skrócić nazwę którą posługujemy się przy wywoływaniu modułu używamy "as"
                                 # i nadajemy jej alias.
from data_loading import load_data  # importujemy wykorzystwane do ładowania danych/tworzenia dat funkcje z lokalnych modułów
from helper_functions import create_date, create_dates_in_range
from helper_functions import sort_dict_by_values


def calculate_total_revenue(rows):           # funkcja do obliczania wartości całkowitego utargu w przekazanych wierszach z transakcjami
    total_revenue = 0                        # inicjalizuemy zmienną, która będzie zawierała całkowity utarg
    for row in rows:                         # iterujemy po każdym z przekazanych wierszy
        total_revenue += row[TOTAL_VALUE]    # dodajemy do zmiennej pomocniczej, w której trzymamy całkowity utarg
                                             # wartość zamówienia po którym aktualnie iterujemy
    total_revenue = round(total_revenue, 2)  # zaokrąglamy wynik do dwóch miejsc po przecinku (głównie ze względów wizualnych)
    return total_revenue                     # zwracamy obliczony utarg całkowity


def unique_values(rows, column_index):               # funkcja służąca do otrzymywania unikalnych wartości z kolumny o podanym indeksie
    unique_values = []                               # tworzymy nową listę na unikalne wartości
    for row in rows:                                 # dla każdego z przekazanych wierszy
        if row[column_index] not in unique_values:   # jeśli wartość o określonym indeksie z wiersza nie znajduje się aktualnie
                                                     # w liście z unikalnymi wartościami...
            unique_values.append(row[column_index])  # ...dodajemy tą wartość do listy z unikalnymi wartościami
    return unique_values                             # zwracamy wynik


class DataTable:  # klasa do reprezentacji/przechowywania/przetwarzania wczytanych danych. zawiera w sobie

    def __init__(self, rows, columns):  # metody init, która jest automatycznie wykonywana przy tworzeniu obiektu. w naszym
                                        # przypadku ma ona dwa argumenty (columny i wiersze), i specjalny argument self,
                                        # który reprezentuje instancje (obiekt) klasy na którym działamy.
        self.rows = rows
        self.columns = columns  # przypisujemy do obiektu klasy (self), przekazane argumenty

    def filter_rows(self, column_index, value):  # metoda, która służy do filtrowania wierszy w reprezentowanych danych tak,
                                                 # aby uzyskać tylko, których wartość wiersza w kolumnie z przekazanym indeksem (column_index)
                                                 # jest równa przekazanej wartości (value). wynikowe wiersze zwracamy.
        filtered_rows = []                       # inicjalizujemy pustą listę na wiersze które spełnią warunki filtracji
        for row in self.rows:                    # dla każdego wiersza z przechowywanych w obecnym obiekcie
            if row[column_index] == value:       # jeśli spełniony jest warunek filtracji (wartość w wierszu jest zgodna z przekazaną)...
                filtered_rows.append(row)        # ... to dodaj aktualny wiersz do listy na wiersze spełniające warunek filtracji
        return filtered_rows                     # zwracamy wynik - przefiltrowane wiersze

    def get_column(self, column_index):              # metoda, zwracająca kolumnę (listę wartości które się w niej znajdują) o podanym indeksie
        column_values = []                           # tworzymy listę na wartości z kolumny
        for row in self.rows:                        # dla każdego z wierszy przechowywanych w obiekcie
            column_values.append(row[column_index])  # dodajemy do listy wartość z wiersza o indeksie żądanej kolumny
        return column_values                         # zwracamy listę wartości znajdujących się w kolumnie

    def get_row(self, row_index):    # metoda zwracająca wiersz o podanym w argumencie indeksie
        return self.rows[row_index]  # po prostu zwracacamy wartość z listy wierszy przechowywanych w obiekcie

# warto zwrócić uwagę na to, że nasza klasa jest obecnie dosyć prosta (była głównie powtórką z tematyki klas, a na zajęciach
# mamy trochę ograniczony czas) i w obecnej formie skupia jedynie w sobie wcześniej zdefiniowane funkcje (do filtracji czy
# uzyskiwania określonej kolumny). można by dodać do niej sporo nowych fukcjonalności (jak np. filtracja w miejscu, tak aby
# nie zwracać listy wierszy, tylko zmodyfikować te w obiekcie, filtrować po więcej niż pojedynczej wartości (np. ich liście),
# czy umożliwić odwoływanie się do kolumny wg. jej nazwy a nie liczbowego indeksu) i zabezpieczyć ją przed potencjalnymi błędami
# (np. obecnie, gdy podamy zły indeks kolumny to cały program zakończy się błędem, a moglibyśmy zamiast tego zwracać pustą wartość - None).
# pomysłów może być oczywiście więcej - natomiast potencjalna realizacja pozostawiona jest czytelnikowi.


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
TOTAL_VALUE = 6  # zmienne (stałe), przy pomocy których zapisujemy pod którym indeksem znajdują się konkretne informacje
                 # przechowywane w wierszach  danych - zwiększając przy tym czytelność kodu

columns, rows = load_data(DATA_PATH)  # wczytujemy listę kolumn i listę wierszy z pliku - przy pomocy wcześniej
                                      # stworzonej, i zaimportowanej funkcji load_data
columns.append('total_transaction_values')  # dodajemy dodatkową kolumnę, która będzie zawierać łączną wartość danego wiersza.
                                            # początkowo w wierszu zawarta jest liczba sztuk kupionego produktu i cena/sztukę,
                                            # zapisując sobie wynik mnożenia tych wartości w dodatkowej kolumnie unikniemy
                                            # wymnażana tych wartości wielokrotnie

for row in rows:                                         # dla każdego z wczytanych wierszy
    total = row[QUANTITY_INDEX] * row[UNIT_PRICE_INDEX]  # wylicz całkowitą wartość danej transakcji, mnożąc liczbę sztuk * cenna/sztukę...
    row.append(total)                                    # ... i dodaj obliczony wynik na końcu wiersza
                                                         # (w zasadzie dobrym pomysłem mogłoby być przeniesienie tego framentu
                                                         # do funkcji wczytującej dane)

dataset = DataTable(rows, columns)


# pierwsza funkcjonalność z listy klienta - zestawienie całkowitej sprzedaży z poszczególnych dni w danym okresie czasowym
# testy przeprowadzamy "na sztywno", na pierwszym tygodniu kwietnia
second_april = create_date(2018, 4, 2)  # tworzymy obiekt date, przy pomocy jednej z funkcji pomocniczych (wcześniej zaimportowana)
sixth_april = create_date(2018, 4, 6)
dates_in_april_first_week = create_dates_in_range(second_april, sixth_april)  # tworzymy listę dat w danym przedziale,
                                                                              # ponownie korzystając z pomocniczej funkcji

# mamy już listę poszczególnych dni w danym przedziale -  teraz musimy policzyć same wartości utargów w tych dniach
revenues = []                           # tworzymy pustą listę na obliczone utargi
for date in dates_in_april_first_week:  # dla każdej daty w naszej otrzymanej liście dni
    filtered_rows = dataset.filter_rows(TRANSACTION_TIME_INDEX, date)  # filtrujemy wiersze, tak aby otrzymać tylko te z dnia,
                                                                       # po którym aktualnie iterujemy
    revenue = calculate_total_revenue(filtered_rows)  # obliczamy utarg w rekordach będących wynikiem filtracji
    revenues.append(revenue)                          # i dodajemy utarg wynikowy z danego dnia do listy wyników


# pierwsza wersja przedstawienia wyników użytkownikowi, przy pomocy raportu w pliku tekstowym i
# w postaci data(spacja)utarg(zł), gdzie każdy kolejny wynik jest w osobnej linii.
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
plt.show()                                        # wywołujemy show, aby wyświetlić przygotowany wykres


# trzecia na liście klienta funkcjonalność - wygenerowanie pięciu najlepiej sprzedających się produktów.
# w tym celu potrzebna nam będzie najpierw lista z unikalnymi nazwami produktow
unique_products_names = unique_values(dataset.rows, PRODUCT_NAME_INDEX)   # tworzymy ją za pomocą zdefiniowanej wcześniej funkcji

# naszym następnym krokiem jest swtorzenie słownika, w którym kluczem jest nazwa produktu a wartoscia calłkowity utarg
revenues_by_product = {}
for name in unique_products_names:                                 # iterujemy po unikalnych nazwach produktów
    filtered_rows = dataset.filter_rows(PRODUCT_NAME_INDEX, name)  # filtrujemy wiersze tak zeby otrzymac tylko te, ktorych
                                                                   # nazwa produktu jest taka jak ta po ktorej aktualnie iterujemy
    product_revenue = calculate_total_revenue(filtered_rows)       # dla przefiltrowanych wierszy (tylko te z aktualnym produktem)
                                                                   #  liczymy utarg
    revenues_by_product[name] = product_revenue                    # umieszczamy obliczony utarg (i nazwe produktu) w slowniku

sorted_product_names = sort_dict_by_values(revenues_by_product)  # następnie korzytamy z kolejnej funkcji pomocniczej,
                                                                 # aby uzyskać klucze słownika posortowane według wartości
                                                                 # uwaga: jak widać w przykładzie w module z którego importujemy
                                                                 # funkcję, wynik jest posortowany rosnąco, od najmniejszej
                                                                 # do największej wartości
print('Najlepiej sprzedające produkty:', sorted_product_names[-5:])  # wypisujemy wynik - ostatnie 5 wartości z posortowanej (rosnąco) listy

# ostatnia z funkcjonalności z wymagań klienta - obliczenie procentowego udziału poszczególnych kategorii w całkowitym utargu.
# chcemy więc otrzymać słownik w którym kluczem będzie kategoria a wartością jej udział w całkowitym utargu
unique_categories_names = unique_values(dataset.rows, CATEGORY_NAME_INDEX)  # zaczynamy od uzyskania wszystkich uniklanych kategorii

categories_revenue_share = {}  # zaczynamy od stworzenia pustego słownika
total_revenue = calculate_total_revenue(dataset.rows)  # utarg z kategorii musimy porównać do całkowitego aby uzyskać procentowy
                                                       # udział - obliczamy więc go na przyszłość

for name in unique_categories_names:                                             # dla każdej unikalnej kategorii
    filtered_rows = dataset.filter_rows(CATEGORY_NAME_INDEX, name)               # filtrujemy po niej wiersze
    category_revenue = calculate_total_revenue(filtered_rows)                    # dla przefiltrowanych wierszy obliczamy utarg
    categories_revenue_share[name] = round(category_revenue / total_revenue, 2)  # i przypisujemy do naszego słownika jego udział w
                                                                                 #  całkowitym utargu, wcześniej zaokrąglony

# print(categories_revenue_share)  # analogicznie jak wcześniej, tekstowa forma nie spodobała się prezesowi - prosi on ponownie o kolorki i grafiki.
plt.pie(list(categories_revenue_share.values()),
        labels=list(categories_revenue_share.keys()), autopct='%.0f%%')   # generujemy wykres kołowy, przy pomocy pie.
                                                                          # w argumentach podajemy listę "udziałów" poszczególnych
                                                                          # wycinków koła, ich etykiety (parametr labels)
                                                                          # i sposób formatowania opisu (parametr autopct,
                                                                          # dzięki niemu mamy "procenty" na wykresie).
                                                                          # labels i pierwszy przekazany argument muszą
                                                                          # być listami - stąd konwersja przy pomocy list().
plt.title('Udział kategorii w utargu')  # ustawiamy tytuł wykresu
plt.show()                              # wywołujemy show, aby wyświetlić przygotowany wykres


# bonus: czwarta funkcjonalność - wysyłanie emaili z ofertą produktu do klientów.
from helper_functions import GmailEmailSender  # importujemy z innego modułu gotową klasę, którą wykorzystamy do tego celu.
                                               # z jej analizy/przeczytania opisu wynika, że należy ją wykorzystać do stworzenia
                                               # klasy potomnej, w której należy nadpisać metodę abstrakcyjną (generate_message_content),
                                               # która z przyjętych argumentów powinna generować tekst wiadomości (string)
                                               # i zwracać go.


class SpamSender(GmailEmailSender):  # tworzymy klasę, która dziedziczy po zaimportowanej

    def generate_message_content(self, product_name):                                # nadpisujemy wspomnianą metodę abstrakcyjną
        ad_text = 'Super oferta, tylko, teraz, musisz kupić nasz {}!!!1!1!'.format(  # tworzymy string z treścią wiadomości
            product_name)
        return ad_text                                                               # i zwracamy go


spam_sender = SpamSender('zbyszek.nowak.fejkmejl@gmail.com', 'Pyladies2018')  # tworzymy obiekt naszej klasy do wysyłania poczty
spam_sender.send_mail('mkm0796@gmail.com', 'Kalafior Krzyś')   # i wywołujemy metodę, która wyśle wiadomość
print('Done - email sent.')  # jeśli wszystko pójdzie w porządku - zobaczymy wydrukowane potwierdzenie
                             # (na zajęciach był mały problem z polskimi znakami - teraz już jest on rozwiązany)
