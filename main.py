# coding = utf-8
import frekfencyjna
import edycyjna
import re
import marshal
import csv


def words_to_dict(words):
    """
    Zamienia string na słownik w formacie SŁOWO: słowo bez przecinków.
    :param words: Zdanie początkowe.
    :return: Słownik.
    """
    words = words.split() 
    rDict = {i:i.lower().replace(',', '') for i in words}
    return rDict


def text_to_list(file_name):
    """
    Funkcja zamienia tekst zapisany w pliku .txt na listę słów bez przecinków i pisanych od małej litery.
    :param file_name: Nazwa pliku.
    :return: Listę słów.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace(',', '').lower().split()
        return text
    except FileNotFoundError:
        print('Plik nie został znaleziony.')
        return None


def inspect(word):
    """
    Funkcja, która sprawdza, czy oryginalne słowo zaczyna się wielką literą, lub kończy się znakiem interpunkcyjnym.
    :param word: Oryginalne słowo.
    :return: Słowo zaczynające się wielką literą lub znak interpunkcyjny, którym się kończy.
    """
    upper = False
    inter = False
    if word[0].isupper():
        upper = True
    if word[-1] in '!.,?-':
        inter = word[-1]

    return upper, inter


def create_korpus(text):

    return text


def correct(words, korpus):
    """
    Funkcja, która przeprowadza półautomatyczną korektę słów
    :param words: Zdanie do korekty.
    :param korpus: Nazwa pliku, na podstawie którego będzie tworzona lista frekwencyjna.
    :return: Zwraca poprawne zdanie
    """

    # tworzę słownik z parami "słowo oryginalne": "słowo oryginalne, które będzie zmieniane w razie potrzeby"
    to_correct = words_to_dict(words)
    # Listę z pliku, w którym znajduje się lista odmienionych słów (źródło: sjp)
    dictionary = text_to_list('test.txt')
    # Tworzę listę frekwencyjną na podstawie tekstu
    freq = frekfencyjna.freq(korpus)

    # Będę przechowywał słowa z błędami
    error = []
    # Słownik słów, które mogą zastąpić wyraz z błędem. Wartość to koszt zamiany z odległości Levenshteina.
    group = {}
    print(to_correct)

    for key, value in to_correct.items():

        if value not in dictionary:
            print(value, 'nie ma w słowniku')

            # Czy słowo zaczyna się od dużej? Czy kończy się znakiem interpunkcyjnym?
            upper, inter = inspect(key)

            # Tworzę listę kandydatów
            for word in dictionary:

                # obliczam odległość Levenshteina
                distance = edycyjna.lev(word, value)
                # print(word, value, distance)

                # Lista kandydatów ma mieć 20 pozycji (teraz testuje na mniejszej - 7 pozycji)
                if len(group) < 7:
                    try:
                        # Dodaję parę, jeśli odległość jest mniejsza od największej odległości zapisanej w słowniku.
                        if distance < max(group.values()):
                            group.update({word: distance})
                    except ValueError:
                        # jeśli nic nie ma w słowniku to dodaję pierwszą parę
                        if len(group) == 0:
                            group.update({word: distance})
                # Jeśli słownik jest pełny, to sprawdzam, czy odległość jest mniejsza od
                # największej odległości zapisanej w słowniku.
                elif distance < max(group.values()):
                    temp = max(group, key=group.get)
                    group.pop(temp)
                    group.update({word: distance})

            # TODO: Sortowanie listy kandydatów według częstości występowania na liście frekwencyjnej
            # TODO: Przygotowanie listy 5 kandydatów do wyboru przez użytkownika
            # TODO: Obsługa wyboru propozycji wyrazu przez użytkownika
            # TODO: Dodanie wielkiej litery i interpunkcji PO WYBORZE UŻYTKOWNIKA (jeśli były)
            # TODO: Edycja odległości edycyjnej tak, żeby wyraz ze słownika nigdy nie był zmieniany
            # TODO: Wyświetlanie pełnego zdania po poprawkach
            # TODO: Cache'owanie wyników dla błędnych wyrazów

            print(group, len(group))

# x = "ala, żółw kot pies papuga goląb Sfkgnadn, ala"
x = "ala, żółw kot pies papuga goląb ala"
correct(x, 'wiki.txt')
