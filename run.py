import torch
from pythainlp.tokenize import sent_tokenize, word_tokenize
print(torch.__version__)
sentence_1 = "ฉันไปประชุมเมื่อวันที่ 11 มีนาคม"
sentence_2 = "ข้าราชการได้รับการหมุนเวียนเป็นระยะ \
    และได้รับมอบหมายให้ประจำในระดับภูมิภาค"
print("sent_tokenize:", sent_tokenize(sentence_1))
print("sent_tokenize:", word_tokenize(sentence_1))
print("no whitespace:", word_tokenize(sentence_1, keep_whitespace=False))
