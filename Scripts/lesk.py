from nltk.tokenize import word_tokenize

def custom_lesk(word, sentence, definitions):
    best_sense = None
    max_overlap = 0
    context = set(word_tokenize(sentence))
    for i in range(len(definitions)):
        signature = set(word_tokenize(definitions[sense.name()]))
        overlap = len(signature.intersection(context))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense
    return best_sense.definition()

word = "bank"
sentence = "I deposited my money in the bank"
definitions = {
    "bank.n.01": "a financial institution that accepts deposits from the public and creates credit",
    "bank.n.02": "a long ridge or pile",
    "bank.n.03": "a slope in the turn of a road or track"
}
sense = custom_lesk(word, sentence, definitions)
print(sense)  # Output: "a financial institution that accepts deposits from the public and creates credit"