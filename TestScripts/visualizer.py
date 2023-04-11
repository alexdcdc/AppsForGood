import spacy
from spacy import displacy
import NewsTest

fh = open("TestScripts\\Example.txt", "r", encoding = "utf-8")

nlp = spacy.load("en_core_web_sm")

formatted = NewsTest.format(fh.read())
print(formatted)
doc = nlp(formatted)
displacy.serve(doc, host = "127.0.0.1", style="dep")