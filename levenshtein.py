from pprint import pprint


def ortografy(word1, word2, position1, position2, p):
    s1 = word1[position1]
    try:
        s2 = word2[position2] + word2[position2 + 1]
    except IndexError:
        return False

    # if p:
    #   print(list(word1), list(word2))
    #   print(s1, s2)
    #   print(word1, ': ', len(word1), word2, ':', len(word2))
    #   print(position1, position2 + 1, '\n')
    # else:
    #   print(list(word1), list(word2))
    #   print(s1, s2)
    #   print(word1, ': ', len(word1), word2, ':', len(word2))
    #   print(position1, position2 + 1, '\n')

    if position2 + 1 > position1:
        try:
            if ((s1 == 'ż' and s2 == 'rz')
                    or (s1 == 'h' and s2 == 'ch')
                    or (s1 == 'ź' and s2 == 'zi')
                    or (s1 == 'ś' and s2 == 'si')
                    or (s1 == 'ć' and s2 == 'ci')
                    or (s1 == 'ń' and s2 == 'ni')):
                return s2
        except:
            pass
    return False


# oblicza odległość Levenshteina
def modlevenshtein(word1, word2):
    result = 0
    diakrytyki = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
                  'ń': 'n', 'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z'}

    newWord1 = list(word1)
    newWord2 = list(word2)

    # szukam dłuższego wyrazu
    longerWordLen = len(word2) if len(word2) > len(word1) else len(word1)

    for position in range(longerWordLen):
        try:
            l1 = word1[position]
            l2 = word2[position]
        except IndexError:
            break

        # szukam czeskiego błędu
        if ((len(word1) > position + 1 and len(word2) > position + 1)
                and (word1[position] == word2[position + 1])
                and (word2[position] == word1[position + 1])):
            result += 0.5
            newWord2[position:position + 2] = word1[position:position + 2]

        # szukam literówki
        elif (word1[position] in diakrytyki
              and diakrytyki[word1[position]] == word2[position]):
            newWord2[position] = word1[position]
            result += 0.2

        elif (word2[position] in diakrytyki
              and diakrytyki[word2[position]] == word1[position]):
            newWord1[position] = word2[position]
            result += 0.2

        # szukam błędu ortograficznego
        elif (word1[position] == 'u'
              and word2[position] == 'ó') or (word2[position] == 'u'
                                              and word1[position] == 'ó'):
            result += 0.5
            newWord1[position] = word2[position]

        elif ortografy(word1, word2, position, position, True):
            result += 0.5
            newWord1[position] = word2[position]
            newWord1.insert(position + 1, word2[position + 1])

        elif ortografy(word2, word1, position, position, False):
            result += 0.5
            newWord2[position] = word1[position]
            newWord2.insert(position + 1, word1[position + 1])

    word1 = ''.join(newWord1)
    word2 = ''.join(newWord2)
    print(word1, word2)

    m, n = len(word1), len(word2)
    d = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j

    for j in range(1, n + 1):

        for i in range(1, m + 1):

            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1

            d[i][j] = min(d[i - 1][j] + 1,
                          d[i][j - 1] + 1,
                          d[i - 1][j - 1] + cost)
            # pprint(d)
            result = result + d[m][n]

    # d = table(word1, word2, d)
    # pprint(d)
    # print('\nOdległość Levenshteina: %s \n'%(d[m+1][n+1]))

    # zwraca wynik dla tablicy, która zawiera w sobie słowa
    # return d, d[m+1][n+1]

    # zwaraca wynik dla tablicy bez słów
    return result


# print( modlevenshtein('pieże', 'pierze') ) # 0.5
print(modlevenshtein('staruch', 'śmiech'))  # 0.2
