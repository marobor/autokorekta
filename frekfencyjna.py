import re, csv, subprocess, os.path
from collections import Counter


# Odczyt tekstu z pliku
def read_text(file_name):
  try:
    with open(file_name, 'r', encoding='utf-8') as file:
      text = file.read()
    return text
  except FileNotFoundError:
    print('Plik nie został znaleziony.')
    return None

# Utworzenie listy frekfencyjnej
def lista_frekfencyjna(text):
  if text is None:
    return None

  # Usuwanie niechcianych znaków (interpunkcja i cyfry)
  # zmiana na małe litery
  text = re.sub(r'[\d\W_]+', ' ', text)
  text = text.lower()

  # dzielenie tekstu na słowa
  words = text.split()

  # zliczanie słów
  word_counter = Counter(words)

  # sortowanie wyników
  sorted_result = sorted(word_counter.items(), 
                         key=lambda x: x[1], 
                         reverse=True)
  
  return sorted_result

# Zapis listy w pliku CSV
def result_csv(word_list, csv_file_name):
  if word_list is None:
    return None

  with open(csv_file_name, 'w', newline='', 
            encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Position', 'Word', 'Counter'])
    position = 1
    for word, counter in word_list:
      writer.writerow([position, word, counter])
      position += 1


def freq(filename):
    source = filename
    result = 'lista.csv'
    
    path = './lista.csv'
    
    if not os.path.isfile(path):
        sample = read_text(source)
        list = lista_frekfencyjna(sample)
        result_csv(list, result)
    
    return result
