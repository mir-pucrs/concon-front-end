# coding: utf-8
import pickle
import numpy as np
from itertools import permutations
from embeddings_model import get_sentence_embeddings

OFFSET_PATH = '/home/site/concon-front-end-master/conconexp/home/embedding/models/offset.pkl'
THRESHOLD = 2


def create_dictionaries(elem_list, norm_ids):
    """
        Generate a dictionary from a list of elements.
        Keys are just the element counter.
    """
    dic = dict()
    index = 0
    
    for elem in elem_list:
        dic[norm_ids[index]] = elem
        index += 1

    return dic


def find_conflicts(clauses, norms):

    conflicts = list()

    sentences = list()
    for norm_id in norms:
        sentences.append(clauses[norm_id])

    # Get offset.
    offset = pickle.load(open(OFFSET_PATH, 'r'))

    # Generate embeddings from sentences.
    embeddings = get_sentence_embeddings(sentences)

    # Create a dictionary for sentences and embeddings.
    sent_dict = create_dictionaries(sentences, norms)
    emb_dict = create_dictionaries(embeddings, norms)

    # Generate all possible tuple between norms.
    assert (len(sent_dict) == len(emb_dict)), "Sentences and embeddings have a different number of elements."
    perm = permutations(sent_dict.keys(), 2)

    for tup in perm:
        # Run over the the tuples and compare the difference
        # with the offset.

        # Calculate the difference between both sentence embeddings.
        diff = emb_dict[tup[0]] - emb_dict[tup[1]]
        
        # Compare the difference with the conflict_offset.
        conflict_diff = np.linalg.norm(offset - diff)

        if conflict_diff < THRESHOLD:
            # If the difference is below the THRESHOLD, add it to a list
            # of conflicts.
            """
                Calculating confidence by using the difference (0 to 1) 
                and multiplying by -20 and adding 100, which gives 100
                and 80, respectively.
            """
            confidence = (-20*conflict_diff) + 100
            conflicts.append((tup[0], tup[1], int(confidence)))
                       
    return conflicts