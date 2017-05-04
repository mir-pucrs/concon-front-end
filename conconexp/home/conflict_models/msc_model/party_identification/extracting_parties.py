# -*- coding: utf-8 -*-
#Algorithm to extract parties from contracts
import re
import os
import nltk
import hashlib


# Global variables.
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
dictionary = {}


def find_entities(block_entities):
    # Function that finds entities in the sentence and returns a list with them.

    entities = []
    nicknames = ['', '']

    block_nick = re.compile(r'\(\"?.+?\"?\)')
    extract_nick = re.compile(r'[\'\`\(\"\"\)]|& quot ;|Hereinafter |hereinafter | referred | to | as ')

    if block_entities.__contains__('AND'):
        try:
            entities.append(' '.join(block_entities[1:block_entities.index('AND')]))
            entities.append(' '.join(block_entities[block_entities.index('AND')+1:]))
        except:
            pass
    else:
        try:
            entities.append(' '.join(block_entities[1:block_entities.index('and')]))
            entities.append(' '.join(block_entities[block_entities.index('and')+1:]))
        except:
            pass

    found = [False, False]
    for ind in range(len(entities)):
        entity = entities[ind].split()
        for index in range(len(entity)):
            counter = index
            while counter <= len(entity):
                key = hashlib.md5(' '.join(entity[index:counter])).digest()
                if dictionary.has_key(key):
                    found[ind] = True
                    block = block_nick.findall(entities[ind])
                    if block:
                        nick = extract_nick.sub("", block[0])
                    if nick:
                        nicknames[ind] = nick                        
                    entities[ind] = ' '.join(entity[index:counter])
                    break
                counter += 1
    # print entities
    for index in range(len(found)):
        if not found[index]:
            block = block_nick.findall(entities[index])
            if block:
                nick = extract_nick.sub("", block[0])
                if nick:
                    nicknames[index] = nick
                else:
                    nicknames[index] = ''                    
            list_entity = entities[index].split()
            pos_entity = nltk.pos_tag(list_entity)
            pos_entity = [(name, tag) for (name, tag) in pos_entity if name != '(' and name != ')']
            nnp_list = [name for name, tag in pos_entity if tag == 'NNP' or tag == 'VBD' or tag == 'NN' or tag == 'JJ']
            entities[index] = ' '.join(nnp_list)

    return entities, nicknames


def extract_parties(contract):
    # Function that opens and process a contract in order to identify parties.

    entities = []

    regex = re.compile('BETWEEN[\r]*.+ AND.+', re.I)
    regex_2 = re.compile('AMONG[\r]*.+ AND.+', re.I)

    try:
        contract_sents = sent_tokenizer.tokenize(contract)
    except:
        print "I can't parse this file."
    
    for sentence in contract_sents:            
        list_tokens = nltk.word_tokenize(sentence)
        sentence = ' '.join(list_tokens)
        block = regex.findall(sentence)
        if block:
            block_entities = block[0].split()
            entities = find_entities(block_entities)
            break
        else:
            block = regex_2.findall(sentence)
            if block:
                block_entities = block[0].split()
                entities = find_entities(block_entities)
                break
    if entities:
        return entities
    else:
        print "No entity was found"