'''
Name: 
visualizer.py

Purpose:
Test script for learning how spaCy creates word associations

Used by:
None
'''

import spacy
from spacy import displacy
import news_get

fh = open("data\\example-article.txt", "r", encoding = "utf-8")

nlp = spacy.load("en_core_web_sm")

formatted = news_get.format(fh.read())
print(formatted)
doc = nlp(formatted)
displacy.serve(doc, host = "127.0.0.1", style="dep")