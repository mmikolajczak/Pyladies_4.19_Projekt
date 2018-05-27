"""
Moduł zawierający różne gotowe do zaimportowania i wykorzystania funkcje pomocnicze,
które prawdopodobnie przydzadzą się w trakcie realizacji projeku.
"""
import datetime
import smtplib


def parse_date_from_string(time_string):
    """
    Tworzy obiekt typu date z łańcucha znaków, zawierającego datę i czas w formacie takim
    jaki znajduje się w danych SZWAGROPOLU.
    Przykład użycia:
    >>> a = parse_date_from_string('2018-04-02 08:25:11')
    >>> print(a)
    output: 2018-04-02
    """
    return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S').date()


def create_date(year, month, day):
    """
    Tworzy obiekt typu date, na podstawie przekazanego roku, miesiąca i dnia.
    Przykład wykorzystania:
    >>> a = create_date(2018, 1, 1)
    >>> print(a)
    output: 2018-01-01
    """
    return datetime.date(year, month, day)


def sort_dict_by_values(dict_):
    """
    Zwraca listę kluczy słownika. Klucze w wyniku są posortowane wg. wartości jakie odpowiały im w słowniku.
    Przykład użycia:
    >>> workers_salaries = {'Nowak': 3100, 'Kowalski': 10000, 'Brzęczyszczykiewicz': 3050}
    >>> lst = sort_dict_by_value(workers_salaries)
    >>> print(lst)
    output: ['Brzęczyszczykiewicz', 'Nowak', 'Kowalski']
    """
    return sorted(dict_, key=dict_.get)


def create_dates_in_range(start_date, end_date):
    """
    Tworzy listę następujących po sobie dat (obiekty typu date), zaczynając od start_date (włącznie)
    do end_date (również włącznie).
    Przykład użycia:
    >>> start_date = create_date(2018, 1, 1)
    >>> end_date = create_date(2018, 1, 10)
    >>> dates = create_dates_in_range(start_date, end_date)
    >>> for date in dates:
    >>>     print(date, end=', ')
    output: 2018-01-01, 2018-01-02, 2018-01-03, 2018-01-04, 2018-01-05, 2018-01-06, (nowa linia dodana manualnie)
     2018-01-07, 2018-01-08, 2018-01-09, 2018-01-10,
    """
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):
        dates.append(start_date + datetime.timedelta(days=i))
    return dates


class GmailEmailSender:
    """Klasa, której obiekty służą do wysyłania wiadomości z poczty Gmail."""

    def __init__(self, gmail_username, gmail_password):
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

    def generate_message_content(self, *args, **kwargs):
        """
        Metoda abstrakcyjna, którą należy zaimplementować w klasie dziedziczącej.
        Na podstawie przekazanych argumentów powinna generować string, będący treścią wiadomości.
        """
        raise NotImplemented()

    def send_mail(self, receiver_address, *args, **kwargs):
        try:
            self.initialize_smtp()
            email_content = self.generate_message_content(*args, **kwargs)
            self.server.sendmail(self.gmail_username, receiver_address, email_content.encode('utf-8'))
            self.terminate_smtp()
        except Exception:
            raise RuntimeError('Error during sending mail.')

    def initialize_smtp(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.gmail_username, self.gmail_password)

    def terminate_smtp(self):
        self.server.close()


