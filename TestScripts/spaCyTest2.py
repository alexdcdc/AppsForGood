import spacy
import pytextrank
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


fh = open("TestScripts\\Example.txt", "r")

doc = nlp(fh.read())



for phrase in doc._.phrases[:10]:
    print(phrase.text)

fh.close()
