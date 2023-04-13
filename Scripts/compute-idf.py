'''
Name: 
compute-idf.py

Purpose:
Reads through a number of news articles in the corpus (see data/ folder)
and compiles inverse document frequencies of each term into a json file (idf.json)

Read more on tf-idf at https://monkeylearn.com/blog/what-is-tf-idf/

Used by:
None

Note: This does take a while to run, so it is
advisable to use the json that has already been generated.
'''

import sys
import collections
import spacy
from string import punctuation
import math

import json

import os

cwd = os.getcwd()

nlp = spacy.load("en_core_web_sm")

# Reads n total articles from the corpus and
# generates a .json file of word idfs.
def computeIDF(n):
    pos_tag = {'PROPN', 'ADJ', 'NOUN'}

    counts = collections.Counter()
    stem = "article_"
    ending = ".txt"
    for i in range(n):
        id = str(i).rjust(6, '0')
        
        fh = open(os.path.join(cwd, "data", stem + id + ending), encoding = "utf-8")
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
    n = 10000
    counts = computeIDF(n)
    idf = {}
    
    with open("idf.json", "w") as fh:
        json.dump({"NoD" : n, "IDF" : counts}, fh)