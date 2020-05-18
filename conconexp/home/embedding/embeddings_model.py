# coding: utf-8
import os
import time
import sys
import re
from subprocess import call
import numpy as np
from nltk import TweetTokenizer
from nltk.tokenize.stanford import StanfordTokenizer

BASE_PATH = "/home/site/concon-front-end-master/conconexp/home/embedding"
FASTTEXT_EXEC_PATH = os.path.join(BASE_PATH, "./fasttext")
BASE_SNLP_PATH = os.path.join(BASE_PATH,
    "models/stanford-corenlp-full-2017-06-09")
SNLP_TAGGER_JAR = os.path.join(BASE_SNLP_PATH, "stanford-corenlp-3.8.0.jar")
MODEL_WIKI_UNIGRAMS = os.path.join(BASE_PATH, "models/wiki_unigrams.bin")


def tokenize(tknzr, sentence, to_lower=True):
    """Arguments:
        - tknzr: a tokenizer implementing the NLTK tokenizer interface
        - sentence: a string to be tokenized
        - to_lower: lowercasing or not
    """
    sentence = sentence.strip()
    sentence = ' '.join([format_token(x) for x in tknzr.tokenize(sentence)])
    if to_lower:
        sentence = sentence.lower()
    sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))','<url>',sentence) #replace urls by <url>
    sentence = re.sub('(\@[^\s]+)','<user>',sentence) #replace @user268 by <user>
    filter(lambda word: ' ' not in word, sentence)
    return sentence


def format_token(token):
    """"""
    if token == '-LRB-':
        token = '('
    elif token == '-RRB-':
        token = ')'
    elif token == '-RSB-':
        token = ']'
    elif token == '-LSB-':
        token = '['
    elif token == '-LCB-':
        token = '{'
    elif token == '-RCB-':
        token = '}'
    return token


def tokenize_sentences(tknzr, sentences, to_lower=True):
    """Arguments:
        - tknzr: a tokenizer implementing the NLTK tokenizer interface
        - sentences: a list of sentences
        - to_lower: lowercasing or not
    """
    return [tokenize(tknzr, s, to_lower) for s in sentences]


def get_embeddings_for_preprocessed_sentences(sentences, model_path,
    fasttext_exec_path):
    """Arguments:
        - sentences: a list of preprocessed sentences
        - model_path: a path to the sent2vec .bin model
        - fasttext_exec_path: a path to the fasttext executable
    """
    timestamp = str(time.time())
    test_path = os.path.join(BASE_PATH, timestamp+'_fasttext.test.txt')
    embeddings_path = os.path.join(BASE_PATH,
        timestamp+'_fasttext.embeddings.txt')

    dump_text_to_disk(test_path, sentences)
    call(fasttext_exec_path+
          ' print-sentence-vectors '+
          model_path + ' < '+
          test_path + ' > ' +
          embeddings_path, shell=True)
    embeddings = read_embeddings(embeddings_path)
    os.remove(test_path)
    os.remove(embeddings_path)

    assert(len(sentences) == len(embeddings)), \
     "Sentences and embeddings have a different number of elements"
    return np.array(embeddings)


def read_embeddings(embeddings_path):
    """Arguments:
        - embeddings_path: path to the embeddings
    """
#     print "I'm reading here. ", embeddings_path
    with open(embeddings_path, 'r') as in_stream:
        embeddings = []
        for line in in_stream:
#             print line
            line = '['+line.replace(' ',',')+']'
            embeddings.append(eval(line))
        return embeddings
    return []


def dump_text_to_disk(file_path, X, Y=None):
    """Arguments:
        - file_path: where to dump the data
        - X: list of sentences to dump
        - Y: labels, if any
    """
    with open(file_path, 'w') as out_stream:
#         print "start writting here. y:", Y
        if Y is not None:
            for x, y in zip(X, Y):
                out_stream.write('__label__'+str(y)+' '+x+' \n')
        else:
            for x in X:
#                 print x
                out_stream.write(x.encode('utf-8')+' \n')


def get_sentence_embeddings(sentences):#, ngram='unigrams',model='concat_wiki_twitter'):
    """ Returns a numpy matrix of embeddings for one of the published models. It
    handles tokenization and can be given raw sentences.
    Arguments:
        - ngram: 'unigrams' or 'bigrams'
        - model: 'wiki', 'twitter', or 'concat_wiki_twitter'
        - sentences: a list of raw sentences ['Once upon a time', 'This is another sentence.', ...]
    """
    wiki_embeddings = None
    tokenized_sentences_SNLP = None
#     if model == "wiki" or model == 'concat_wiki_twitter':
    tknzr = StanfordTokenizer(SNLP_TAGGER_JAR, encoding='utf-8')
    s = ' <delimiter> '.join(sentences) #just a trick to make things faster
    tokenized_sentences_SNLP = tokenize_sentences(tknzr, [s])
    tokenized_sentences_SNLP = tokenized_sentences_SNLP[0].split(
        ' <delimiter> ')
    assert(len(tokenized_sentences_SNLP) == len(sentences))
    wiki_embeddings = get_embeddings_for_preprocessed_sentences(
        tokenized_sentences_SNLP, MODEL_WIKI_UNIGRAMS, FASTTEXT_EXEC_PATH)
    
    return wiki_embeddings
    sys.exit(-1)
