import frekfencyjna
import edycyjna
import re
import marshal
import csv

# TODO: Edycja odległości edycyjnej tak, żeby wyraz ze słownika nigdy nie był zmieniany
# TODO: Wyświetlanie pełnego zdania po poprawkach
# TODO: Cache'owanie wyników dla błędnych wyrazów


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


def compare(mistake_dict, f_dict):
    """
    Porównanie i sortowanie słownika proponowanych słów z listą frekwencyjną.
    :param mistake_dict: Słownik z proponowanymi słowami.
    :param f_list: Lista frekwencyjna.
    :return: Posortowana lista z proponowanymi słowami.
    """
    sorted_mistake_dict = {}
    # przygotowanie słownika posortowanego według pozycji na liście frekwencyjnej
    mistake_list = [word for word in mistake_dict.keys()]
    sorted_mistake_list = sorted(mistake_list, key=lambda x: f_dict.get(x, len(f_dict) + 1))
    # Własna inwencja twórcza może być głupie (chcę uwzględnić wynik Levenshteina i pozycję na liście frekwencyjnej)
    for index, key in enumerate(sorted_mistake_list, start=1):
        value = mistake_dict[key] + index
        sorted_mistake_dict[key] = value

    sorted_mistake_dict = dict(sorted(sorted_mistake_dict.items(), key=lambda x: x[1]))

    return sorted_mistake_dict


def frequency_list(korpus):
    """
    Zmienia korpus na listę słów posortowaną według częstości występowania.
    :param korpus: Nazwa pliku tekstowego.
    :return: Słownik słowo: pozycja w słowniku.
    """
    f_words = {}
    # Tworzę listę frekwencyjną na podstawie tekstu
    csv_file = frekfencyjna.freq(korpus)
    # Odczytanie słów z pliku CSV
    with open(csv_file, 'r', encoding="utf8") as file:
        reader = csv.reader(file)
        # Pominięcie nagłówków, jeśli istnieją
        next(reader, None)
        # Dodanie słów do listy
        i = 1
        for row in reader:
            word = row[1]
            f_words.update({word: i})
            i += 1

    return f_words


def user_input(candidates_dict, upper, inter):
    """
    Wyświetla listę możliwych korekcji i zrwaca wybrane przez użytkownika słowo.
    :param candidates_dict: Słownik proponowanych słów.
    :return: Wybrane przez użytkownika słowo.
    """
    correction = ''
    first_5_keys = list(candidates_dict.keys())[:5]
    print(' Czy chodziło Ci o jedno z poniższych słów?\n', first_5_keys, '\n',
          'Wybierz słowo z listy wpisując cyfrę od 1 do 5. Jeśli nie ma odpowiedniego słowa wpisz 0')
    x = input()

    while x not in '012345':
        print(first_5_keys, '\n',
              'Wybierz słowo z listy wpisując cyfrę od 1 do 5. Jeśli nie ma odpowiedniego słowa wpisz 0')
        x = input()

    if x == '0':
        m2 = input('Jeśli chcesz wpisać poprawne słowo wpisz 1\n')
        if m2 == '1':
            correction = input()
            print(' Wprowadziłeś słowo: ', correction, '\n\n\n')
    else:
        correction = first_5_keys[int(x) - 1]
        print(' Wybrałeś słowo: ', correction, '\n\n\n')

    if upper:
        correction = correction.capitalize()

    if inter:
        correction = correction + inter

    return correction


def correct(words, korpus):
    """
    Funkcja, która przeprowadza półautomatyczną korektę słów.
    :param words: Zdanie do korekty.
    :param korpus: Nazwa pliku, na podstawie którego będzie tworzona lista frekwencyjna.
    :return: Zwraca poprawne zdanie
    """

    # tworzę słownik z parami "słowo oryginalne": "słowo oryginalne, które będzie zmieniane w razie potrzeby"
    to_correct = words_to_dict(words)
    # Listę z pliku, w którym znajduje się lista odmienionych słów (źródło: sjp)
    dictionary = text_to_list('odm.txt')

    freq = frequency_list(korpus)

    # Słownik słów, które mogą zastąpić wyraz z błędem. Wartość to koszt zamiany z odległości Levenshteina.
    group = {}
    # print(to_correct)

    for key, value in to_correct.items():

        if value not in dictionary:
            print('Słowa', value, 'nie ma w słowniku')
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

            print(group, len(group))
            candidates = compare(group, freq)
            # print(candidates)
            correction = user_input(candidates, upper, inter)

            # print(correction)
            if correction != '':
                to_correct[key] = correction
            # print(to_correct)
        group = {}

    correct_sentence = ' '.join(to_correct.values())
    return correct_sentence


x = "Mialen puroblem, ktory wymagau szypkiego rosfionsania"
# x = "ala, żółw kot pies papuga goląb ala"
print(correct(x, 'wiki.txt'))
