import spacy
import importlib
from collections import Counter
from string import punctuation

importlib.import_module("DictionaryTest")

nlp = spacy.load("en_core_web_sm")

def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.lemma_)
    return result


fh = open("TestScripts\\Example.txt", "r")

new_text = fh.read()

output = get_hotwords(new_text)

most_common_list = Counter(output).most_common(10)

for item in most_common_list:
  print(item[0])

fh.close()