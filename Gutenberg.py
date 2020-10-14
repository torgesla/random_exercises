import random
import os
import sys
import string
import itertools
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist
from gensim import corpora

random.seed(123)

with open(os.path.join(sys.path[0], 'gutenberg.txt'), encoding='utf-8', mode='r') as f:
    paragraphs = [p for p in f.read().lower().split('\r\n\r\n')]  # Split text into paragraphs and add to list
filtered_paragraphs = [p for p in paragraphs if 'gutenberg' not in p]  # Remove from list if contains 'gutenberg'
tokenized_paragraphs = [p.split() for p in filtered_paragraphs]  # Split every paragraph into tokens => 2d list
stripped_paragraphs = [[word.strip(string.punctuation+'\n\r\t') for word in paragraph] for paragraph in tokenized_paragraphs]  # Remove punctuation and whitespace from words
non_empty_paragraphs = [paragraph for paragraph in stripped_paragraphs if paragraph]  # Remove all paragraph lists that are empty
stemmer = PorterStemmer()
stemmed_paragraphs = [[stemmer.stem(word) for word in paragraph] for paragraph in non_empty_paragraphs]  # Stem all words
fdist = FreqDist(list(itertools.chain.from_iterable(stemmed_paragraphs)))  # Flatten list and add to word count dict
dictionary = corpora.Dictionary(stemmed_paragraphs)

with open(os.path.join(sys.path[0], 'stopwords.txt'), encoding='utf-8', mode='r') as stopwordsfile:
    stopwords = stopwordsfile.read().split(',')
stopword_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id]  # Make a list of all ids for stopwords
dictionary.filter_tokens(stopword_ids)
print(*stopword_ids)
