import itertools
import numpy as np
import pandas as pd
def contains(needle,haystack):
    tempstack = sorted(haystack)
    tempn = sorted(needle)

    for x in tempn:
        if not (x in tempstack):
            return False
        else:
            i = tempstack.index(x)
            tempstack = sorted(tempstack[:i]+tempstack[i+1:])

    return True

def diffletters(word1,word2):
    if len(word1) <= len(word2):
        needle = word1
        haystack = word2
    else:
        needle = word2
        haystack = word1

    tempstack = haystack

    for x in needle:
        for y in tempstack:
            if x == y:
                i = tempstack.index(x)
                tempstack = tempstack[:i] + tempstack[i+1:]
                break

    return tempstack

def readdict(dname):
    f = open(dname,"r")
    allwords = f.read().upper().split("\n")
    # print(len(allwords))
    return allwords

def runfilter(wordlist,filtertext,excludeletters = '',mustcontain='',charcombos=[[]]):
    filtertext = filtertext.upper()
    excludeletters = excludeletters.upper()
    mustcontain = mustcontain.upper()
    returnvalue = []
    # print('Filter: ' + filtertext
    found = False
    multilen = False
    if '*' in filtertext:
        multilen = True

    # print("Multilength: " + str(multilen))
    filtertext = filtertext.replace("*","")

    for word in wordlist:
        # print(word)
        matching = True
        if multilen == False:
            if len(word) != len(filtertext):
                matching = False
                continue

        for x in range(len(word)):
            if x >= len(filtertext):
                continue
            # immediately filter out exclude words
            if word[x] in excludeletters:
                matching = False
                continue
            # any letter
            if filtertext[x] == ".":
                continue
            # match the letter to the location
            elif filtertext[x] != word[x] and not multilen:
                matching = False
                continue
            elif multilen:
                matching = False
                # Todo multilen is implemented incompletely / incorrectly
                if contains(filtertext, word):
                    matching = True
                continue

        # char combos are letters with positions they can't be
        # array with [0] being the letter, and [1:] being the positions it's not allowed to be

        for charcombo in charcombos:
            if len(charcombo) == 0 : continue
            letter = charcombo[0].upper()
            nonpositions = charcombo[1:]
            for pos in nonpositions:
                if word[pos] == letter:
                    matching = False

        if matching and multilen:
            if mustcontain == '':
                returnvalue.append(word)
            elif set(mustcontain).issubset(set(word)):
                returnvalue.append(word)

        elif matching and len(word) == len(filtertext):
            if mustcontain == '':
                returnvalue.append(word)
            elif set(mustcontain).issubset(set(word)):
                returnvalue.append(word)

    return returnvalue

def subanagrams(wordlist,filtertext):
    filtertext = filtertext.upper()
    returnvalue = []
    # print('Filter: ' + filtertext)
    found = False

    for word in wordlist:
        # We find out which letters are not common between the two words and delete those from the
        # filterword, and check then if what remains are sorted are the same then we have an anagram

        # find out which letters are not common
        diff = (set(word)-set(filtertext)).union(set(filtertext) - set(word))
        difflist = list(diff)  # change from set back to list



        # remove the different characters from the list via regex
        # this code feels slow, perhaps I can make it faster (is regex maybe a hammer
        # when something smaller like a for loop will work?)
        # if len(difflist)>0:
        #     rx = '[' + re.escape(''.join(difflist)) + ']'
        #     newcompare = re.sub(rx,'',filtertext)
        # else: newcompare = filtertext

        # this is quite a bit faster (about 7x faster)
        newcompare = ''
        for x in filtertext:
            if not x in difflist:
                newcompare = newcompare + x

        # check if the two sorted are the same
        if contains(word,newcompare):
            if word != '':
                returnvalue.append(word)

    return returnvalue

def createsublist(wordlist,filtertext, size = 0):
    filtertext = filtertext.upper()
    sublist = []

    for word in wordlist:
        if contains(word,filtertext):
            if (size > 0) and (len(word) == size):
                sublist.append(word)
            elif size == 0:
                sublist.append(word)

    return sublist

# https://stackoverflow.com/questions/73803844/find-unique-sums-to-add-to-total-using-only-positive-integers-above-0
def find_sums(n):
    sums = []
    all_sums = []
    find_sums_helper(n, n, sums, all_sums)
    return all_sums

def createlengthlist(list,length):
    sublist = []
    for word in list:
        if len(word)==length:
            sublist.append(word)
    return sublist

def find_sums_helper(n, n_max, sums, all_sums):
    if n == 0:
        all_sums.append(sums)
        return

    for i in reversed(range(1, min(n, n_max) + 1)):
        find_sums_helper(n - i, i, sums + [i], all_sums)

def subcontains(word,word2):
    if len(word) > len(word2):
        needle = word2
        haystack = word
    else:
        needle = word
        haystack = word2

    if not contains(needle,haystack):
        return [haystack,needle]
    else:
        return False

def possibilityhelper(wordlist,filtertext):
    filtertext = filtertext.upper()
    returnvalue = []
    for element in itertools.product(*wordlist):
        teststring = ''.join(element)
        if sorted(teststring) == sorted(filtertext):
            returnvalue.append(element)
    return set(returnvalue)

def wordcombofinder(wordlist,filtertext,minlength = 3,minmax = 3, maxwords = 4):
    # this is very inefficient way of doing this, so I have 2 parameters to control the vast amounts of combinations
    # If the total wordlength is less than like 10 you should be fine for runtime, but it explodes exponentially
    # after that
    # - minlength:  the minimum size of word we want to consider, increasing this reduces runtime considerably,
    #               3 is recommended, but you miss out on important words sometimes like 'IN','ON','BY' etc.
    # - minmax:     this is the minimum size of the biggest word, so you might have a 5 letter word and a bunch
    #               of smaller ones
    # - maxwords:   The max number of words
    #
    # Suggestion for long words, use the subanagrams to find words that you like, then reduce the letters in the
    # big word to reduce the workload
    returnvalue = []
    filtertext = filtertext.upper()
    pcombos = find_sums(len(filtertext))
    # print(pcombos)
    sublist = createsublist(wordlist, filtertext)

    for wordset in pcombos:
        combolist = []
        # create possibilities
        if max(wordset) < minmax:
            continue
        if len(wordset) > maxwords:
            continue
        for wordlen in wordset:
            # have a minimum word length to optimize it a little
            if wordlen >= minlength:
                alist = createlengthlist(sublist, wordlen)
                combolist.append(alist)

        # reduce obvious wrong combinations
        if [] in combolist:
            continue

        # find possibilities
        pos = possibilityhelper(combolist,filtertext)
        if pos:
            returnvalue.append(pos)
            continue

    return returnvalue

def letterdistribution(wordlist):
    letters = {}
    for word in wordlist:
        for letter in word:
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
    df = pd.DataFrame(letters.items()).sort_values(by=[1], ascending=False)
    return df

def wordsubsets(wordlist1, letter1, wordlist2, letter2):

    # the idea of this is to check which letters at letter1 and letter2 overlap  (word arrays start at 1 not at 0, so
    # letter1/2 is 'fixed' so 3 means 3rd letter
    # used for when you set a crossword and you have intersections and you want to get the list of words which are available
    # typical usage would be wordsubsets(runfilter(dict,'a...n.a'),3,runfilter(dict,'e..nd.a'),3)
    # this will check both sets of words for matching letters in letter1 and letter2
    # run this on filtered datasets it will try all words in both sets, so it's a cartesean join

    returnarr = []
    letters = []
    for word1 in wordlist1:
        for word2 in wordlist2:
            if word1[letter1-1] == word2[letter2-1]:
                wordcombination = []
                wordcombination.append(word1[letter1-1])
                letters.append(word1[letter1-1])
                wordcombination.append(word1)
                wordcombination.append(word2)
                returnarr.append(wordcombination)
    returnarr.insert(0,list(set(letters
                                )))
    return returnarr
