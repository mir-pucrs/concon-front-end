# -*- coding: utf-8 -*-

"""
	Algorithm that, given two sentences, returns the semantic similarity between them.
"""

import nltk
import re
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

remove_punctuation = re.compile(r'[\"\#\$\%\&\\\'\(\)\*\+\,\-\/\:\;\<\=\>\@\[\\\\\]\^\_\`\{\|\}\~]+')
wnl = WordNetLemmatizer()

def similarity(sent1, sent2):
    similarity = 0
    sent1 = remove_punctuation.sub('', sent1.lower())
    sent2 = remove_punctuation.sub('', sent2.lower())
    sent1, sent2 = nltk.word_tokenize(sent1), nltk.word_tokenize(sent2)

    if len(sent1) > 2 * len(sent2) or len(sent2) > 2 * len(sent1):
        return 0

    if len(sent1) > len(sent2):
        large = sent1
        small = sent2
    else:
        small = sent1
        large = sent2

    for index1 in range(len(small)):
        # Go through the first sentence.

        higher = 0      # Auxiliar variable that keeps the higher semantic similarity between the words.

        if wnl.lemmatize(small[index1]) == wnl.lemmatize(large[index1]):
            # If there are equal words in the same position in both sentences, we add 1 to the final score.
            similarity += 1
        else:
            # Else, we go through the larger sentence until we find either the same word or a semantic similar word.
            for index2 in range(len(large)):
                word1 = wnl.lemmatize(small[index1])
                word2 = wnl.lemmatize(large[index2])
                if  word1 == word2:
                    # If we find the same word in a different position, we add 0.7 to the final score.
                    higher = 0.7
                    break
                else:
                    # Else, we get all synonyms of each word and compare them according to its semantic meaning.
                    syn_1 = wn.synsets(word1)
                    syn_2 = wn.synsets(word2)
                    for s1 in syn_1:
                        sim = 0
                        for s2 in syn_2:
                            sim = s1.wup_similarity(s2)
                            if sim and sim > higher:
                                higher = sim
                    higher *= 0.7
            if higher > 0:
                similarity += higher

    return similarity/( (len(large) + len(small) ) / 2 )

if __name__ == "__main__":
    
    sentence_pairs = [("I like that bachelor.","I like that unmarried man."), ("I have a pen.","Where do you live?"), ("John is very nice.", "Is John very nice?"), ("Red alcoholic drink.", "A bottle of wine."),
        ("It is a dog.", "That must be your dog."), ("Red alcoholic drink.", "Fresh orange juice."), ("It is a dog.", "It is a log."), ("Red alcoholic drink.", "An English dictionary."), ("It is a dog.", "It is a pig."),
        ("Dogs are animals.", "They are common pets."), ("I have a hammer.", "Take some nails."), ("Canis familiaris are animals.", "Dogs are common pets."), ("I have a pen.", "Where is ink."), ("Red alcoholic drink.", "Fresh apple juice."),
        ("A glass of cider.", "A full cup of apple juice."), ("I have a hammer.", "Take some apples.")]


    print similarity("use only approved suppliers listed on AorTech's approved supplier list when purchasing such material.", "use unapproved suppliers listed on AorTech's unapproved supplier list when purchasing such material.")