# coding = utf-8
import frekfencyjna
import edycyjna
import re
import marshal
import csv


def words_to_dict(words):
    words = words.split() 
    rDict = {i:i.lower().replace(',', '') for i in words}
    return rDict


def text_to_list(fileName):
    try:
        with open(fileName, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace(',', '').lower().split()
        return text
    except FileNotFoundError:
        print('Plik nie został znaleziony.')
        return None


def inspect(word):
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
    to_correct = words_to_dict(words)
    dictionary = text_to_list('test.txt')
    freq = frekfencyjna.freq(korpus)
    error = []
    group = {}
    print(to_correct)
    
    for key, value in to_correct.items():
        if value not in dictionary:
            print(value, 'nie ma w słowniku')
            upper, inter = inspect(key)
            for word in dictionary:
                distance = edycyjna.lev(word, value)
                # print(word, value, distance)
                if word not in group.items() and len(group) < 7:
                    try:
                        if distance < max(group.values()):
                            group.update({word: distance})
                    except ValueError:
                        if len(group) == 0:
                            group.update({word: distance})
                elif word not in group.items() and distance < max(group.values()):
                    temp = max(group, key=group.get)
                    group.pop(temp)
                    group.update({word: distance})

            print(group, len(group))

# x = "ala, żółw kot pies papuga goląb Sfkgnadn, ala"
x = "ala, żółw kot pies papuga goląb ala"
correct(x, 'wiki.txt')
