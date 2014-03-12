from nltk.tokenize import word_tokenize, RegexpTokenizer
import re

__author__ = 'jeremy'


def tokenize(sentences):
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        print((sentence, tokens))


word_reg = re.compile('\w+')
tokenizer = RegexpTokenizer(word_reg)


def reg_tokenize(sentences):
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        print((sentence, tokens))


if __name__ == '__main__':
    __sentences = ['it&#39;s fun it&#39;s goodgraphic is good nice and good game',
                   'I like the anime style graphics good defense']
    tokenize(__sentences)
    reg_tokenize(__sentences)