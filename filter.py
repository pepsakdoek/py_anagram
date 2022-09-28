import itertools

import numpy as np
from datetime import datetime
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
    allwords = f.read().split("\n")
    # print(len(allwords))
    return allwords

def runfilter(wordlist,filtertext):
    returnvalue = []
    print('Filter: ' + filtertext)
    found = False
    multilen = False
    if '*' in filtertext:
        multilen = True

    print("Multilength: " + str(multilen))
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
            if filtertext[x] == ".":
                continue
                # Case insensitive please
            elif filtertext[x].upper() != word[x].upper() and not multilen:
                matching = False
                continue
            elif multilen:
                matching = False
                if contains(filtertext,word):
                    matching = True
                continue

        if matching and multilen:
            returnvalue.append(word)

        elif matching and len(word) == len(filtertext):
            returnvalue.append(word)


    return returnvalue

def subanagrams(wordlist,filtertext):
    returnvalue = []
    print('Filter: ' + filtertext)
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
    returnvalue = []
    pcombos = find_sums(len(filtertext))
    print(pcombos)
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

allwords = readdict("Woorde.csv")
timestart = datetime.now()

f = open("output.txt","w")
#t = subanagrams(allwords,"PIENKPIENKSONOP")
#f.write(repr(t)+"\n")
t = wordcombofinder(allwords,"PIENKPIENKSONOP",2,5,5)
f.write(repr(t)+"\n")
f.close()
# runfilter(allwords,'se.a.')

print(datetime.now() - timestart)


# runfilter(allwords,'V.D.')
# runfilter(allwords,'S.P.R')
# runfilter(allwords,'.S.A')

# runfilter(allwords,'..R.G.T..')
# runfilter(allwords,'D.P..')
# runfilter(allwords,'.S.U.O.I..')
# runfilter(allwords,'..I...O.')
# runfilter(allwords,'..P.I')
# runfilter(allwords,'...A.U')


# kennis pikwykuke
# puik wykke
# wykke

# Konneksie ppinop
# pop inp

# poens iinnekpkop
# knip inekop
# knie
# op

# NOPPIES KINNEKOP
# PONS PIE
# PIENK
# NOK

# KNOP PIESPINNEKO
# IN PIESPNEKO
# NIKS PEPEO
# POEPE
