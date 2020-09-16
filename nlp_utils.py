import numpy as np
import pythainlp

def tokenize(sentence):
    return pythainlp.word_tokenize(sentence)

def bag_of_words(tokenized_sentence, words):
