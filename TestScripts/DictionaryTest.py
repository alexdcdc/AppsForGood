import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

def getSynonyms(token):
    return token._.wordnet.synsets()