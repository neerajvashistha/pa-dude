import re, collections
import sys
from bitmap  import Bitmap
from hashlib import md5

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('corpus.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def correct_top(word, n):
    candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
    s = sorted(candidates, key=NWORDS.get, reverse=True)
    return s[0], s[:n]

def makeHashes(word) :
    # convert 32 hexdigits to list of 6 hash keys
    hex32 = md5(word).hexdigest()
    hashes = []
    for i in range(0,30,5) :
        hashes.append(int(hex32[i:i+5],16))
    return hashes

def loadBitmap(file) :
    # generate bitmap from lexicon file (one word per line)
    words = open(file).readlines()
    words = map(lambda x: x.strip(), words) # no newlines please
    bmap  = Bitmap(2**20)
    for word in words :
        hashes = makeHashes(word)
        for hash in hashes :
            bmap.setBit(hash)
    return bmap

bmap  = loadBitmap("spell.words")

def checkWord(bmap, word) :
    # return True if word in lexicon
    hashes = makeHashes(word)
    for hash in hashes :
        if not bmap.getBit(hash): return False
    return True

def sentence_correct(sentence):

    wordlist = sentence.split()
    correctSentenceList = []
    for word in wordlist:
        if checkWord(bmap,word) is False:
            word = correct(word)
        correctSentenceList.append(word)
    #print correctSentenceList
    correctSentence = ' '.join(correctSentenceList)
    return correctSentence


if __name__ == "__main__":
    print(sentence_correct("I wuld lik to ordr manchrian"))
