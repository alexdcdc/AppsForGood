import spacy
import importlib
from collections import Counter
from collections import deque
from string import punctuation
import NewsTest
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
import pytextrank
from rake_nltk import Rake
from nltk.corpus import stopwords
import json
import math
import BuzzwordsDatabase

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacy_wordnet", after='tagger')
nlp.add_pipe("textrank")

filter = {"axios", "guardian", "newsweek", "forbes", "nbc", "npr", "trump", "biden", "desantis"}

def getSynonyms(token):
    return token._.wordnet.synsets()

def get_hotwords1(text: str) -> list:
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    if not text:
        return []
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation or token.text in filter):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.lemma_)
    
    return result

def get_hotwordsDouble(text: str) -> list:
    pair = deque()
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    if not text:
        return []
    doc = nlp(text.lower()) 
    for token in doc:
        if len(pair) == 2:
            pair.popleft()
        pair.append(token.lemma_)
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation or token.text in filter):
            continue
        if(token.pos_ in pos_tag):
            result.append(list(pair))
            

    return result

def get_hotwords2(text: str) -> list:
    if not text:
        return []
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases]

def get_hotwords3(text: str) -> list:
    if not text:
        return []
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()

def tf_idf(text: str) -> list:
    tf = Counter(get_hotwords1(text))
    fh = open("idf.json")
    idf = json.load(fh)
    n = idf["NoD"]
    idf = idf["IDF"]

    fh.close()
    scores = {}
    for t in tf:
        scores[t] = tf[t] * math.log((n + 1)/((idf[t] + 1) if t in idf else 1))
    
    
    return sorted(scores.keys(), key = lambda x: -scores[x])[:3]

def extractDailyKeywords() -> Counter:
    words = Counter()
    texts = NewsTest.getUSHeadlines()

    if not texts:
        print("ERR: Error occurred while getting news sources.")
        return

    for text in texts:
        words.update(tf_idf(text))
    
    return words

fh = open("TestScripts\\Example.txt", "r", encoding = "utf-8")

most_common_list = extractDailyKeywords().most_common(10)

BuzzwordsDatabase.DBWrite({"Trending": most_common_list})

for item in most_common_list:
  print(item[0])

fh.close()
