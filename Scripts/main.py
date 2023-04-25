'''
Name: 
main.py

Purpose:
Core script to extract keywords from news 
articles and transfer them to Firebase

Used by:
None
'''

import spacy
from collections import Counter
from collections import deque
from string import punctuation
import news_get
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
import pytextrank
from rake_nltk import Rake
from nltk.corpus import stopwords
import json
import math
import buzzwords_database
import dictionary_get

# Initialize the nlp pipeline
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacy_wordnet", after='tagger')
nlp.add_pipe("textrank")

# Create a filter of a few commonly-occurring 
# words that should not be keywords
filter = {"axios", "guardian", "newsweek", "forbes", "nbc", 
          "npr", "trump", "biden", "desantis"}

# Given a word, return its set of synonyms
def getSynonyms(token):
    return token._.wordnet.synsets()

# Algorithm 1 for finding keywords: 
# filter all noun/adjective words into a list
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

# Algorithm for finding two-word keyphrases (WIP)
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

# Algorithm 2 for finding keywords:
# Extract all phrases in the text into a list
def get_hotwords2(text: str) -> list:
    if not text:
        return []
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases]

# Algorithm 3 for finding keywords:
# Use Rake built-in keyword extractor
def get_hotwords3(text: str) -> list:
    if not text:
        return []
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()

# tf-idf algorithm for calculating keyword "scores"
# in a document: see https://monkeylearn.com/blog/what-is-tf-idf/
# for more details. Returns top three highest scorers in input text.
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

# Gets current news articles and applies tf-idf
# to get top 3 keywords for each article. Returns
# a counter of how often each term appears as a top-3 KW.
def extractDailyKeywords() -> Counter:
    words = Counter()
    texts = news_get.getUSHeadlines()

    if not texts:
        print("ERR: Error occurred while getting news sources.")
        return

    for text in texts:
        words.update(tf_idf(text))
    
    return words

if __name__ == "__main__":
    most_common_list = extractDailyKeywords().most_common(10)
    jsonData = []
    
    for w in most_common_list:
        definitions = dictionary_get.getDefinitions(w[0])
        jsonData.append({"word": w[0], "definitions": dictionary_get.getDefinitions(w[0])})

    buzzwords_database.DBWrite("/Trending/", jsonData)
    buzzwords_database.DBPush("/All/", {d['word'] : d['definitions'] for d in jsonData})

    for item in most_common_list:
        print(item[0])
