import numpy as np
import pythainlp
from pythainlp import word_tokenize, Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words


# ตัดคำโดยใช้ newmm
def tokenize(sentence):
    return pythainlp.word_tokenize(sentence, engine='newmm')


# สร้างคลังคำศัพท์
def bag_of_words(tokenized_sentence, words):
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag

