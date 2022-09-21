# import re
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


def readdict(dname):
    f = open(dname,"r")
    allwords = f.read().split("\n")
    # print(len(allwords))
    return allwords

def runfilter(wordlist,filtertext):
    matches = 0
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
            print(word)
            matches += 1
        elif matching and len(word) == len(filtertext):
            print(word)
            matches += 1

    return matches

def subanagrams(wordlist,filtertext):
    print('Filter: ' + filtertext)
    matches = 0
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
                print(word)
                matches += 1
    return matches


allwords = readdict("Woorde.csv")
timestart = datetime.now()
# t = subanagrams(allwords,"KNOPIESPINNEKOP")
t2 = runfilter(allwords,"*POE")
print(datetime.now() - timestart)
print('Matches: ' + str(t2))

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
