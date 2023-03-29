import sys
import collections
import spacy
from string import punctuation
import math

import json

nlp = spacy.load("en_core_web_sm")

def computeIDF(n):
    pos_tag = {'PROPN', 'ADJ', 'NOUN'}

    counts = collections.Counter()
    stem = "article_"
    ending = ".txt"
    for i in range(n):
        id = str(i).rjust(6, '0')
        
        fh = open("C:\\Users\\alexd\\OneDrive\\Documents\\AppsForGood\\data\\" + stem + id + ending, encoding = "utf-8")
        s = set()
        for l in fh:
            for token in nlp(l.lower()):
                if not (token.pos_ in pos_tag) or (token.text in nlp.Defaults.stop_words or token.text in punctuation):
                    continue
                s.add(token.lemma_)
        
        counts.update(s)
        fh.close()
    
    return counts

if __name__ == "__main__":
    n = 1000
    counts = computeIDF(n)
    idf = {}
    
    with open("idf.json", "w") as fh:
        json.dump({"NoD" : n, "IDF" : counts}, fh)