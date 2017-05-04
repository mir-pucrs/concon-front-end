import nltk
from itertools import combinations
from sentence_similarity.semantic_similarity import similarity

MODAL_VERBS = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'ought']
MODAL_DICT = {
            'can': 'permission',
            'may': 'permission',
            'might': 'permission',
            'could': 'permission',
            'shall': 'obligation',
            'must': 'obligation',
            'will': 'obligation',
            'ought': 'obligation',
            'should': 'obligation',
            'shall not': 'prohibition',
            'can not': 'prohibition',
            'could not': 'prohibition',
            'might not': 'prohibition',
            'may not': 'prohibition',
            'will not': 'prohibition',
            'must not': 'prohibition',
            'ought not': 'prohibition',
            'should not': 'prohibition'
        }
FIRST_ENTITY = 0
SECOND_ENTITY = 1
THRESHOLD = 0.6

def check_modality(cur_token, next_token):

    if next_token == 'not':
        return MODAL_DICT[cur_token + ' ' + next_token]
    else:
        return MODAL_DICT[cur_token]


def check_norms(entities, norms, clauses):

    full_name, nicknames = entities

    first_entity_norms = dict()
    second_entity_norms = dict()

    for norm in norms:

        # Get norm text:
        norm_text = clauses[norm]

        # Break text into tokens and find the one that is a modal verb.
        tokens = nltk.word_tokenize(norm_text.lower())

        for i, token in enumerate(tokens):

            if token in MODAL_VERBS:
                # If it has the modal verb, get
                party_area = tokens[:tokens.index(token)][::-1]

                # Get modality.
                modality = check_modality(token, tokens[i + 1])

                # Get norm action.
                if modality != 'prohibition':
                    norm_action = ' '.join(tokens[i+1:])
                else:
                    norm_action = ' '.join(tokens[i+2:])

                # Find a party name in the stretch of text before modal verb.
                found = find_entity(full_name, party_area)

                if found:

                    if found == FIRST_ENTITY:
                        first_entity_norms[norm] = (modality, norm_action)
                    elif found == SECOND_ENTITY:
                        second_entity_norms[norm] = (modality, norm_action)

                    break

                found = find_nickname(nicknames, party_area)

                if found:

                    if found == FIRST_ENTITY:
                        first_entity_norms[norm] = (modality, norm_action)
                    elif found == SECOND_ENTITY:
                        second_entity_norms[norm] = (modality, norm_action)

                    break

                else:
                    continue

    return first_entity_norms, second_entity_norms


def find_nickname(nicknames, norm):

    for entity in nicknames:
        for word in nltk.word_tokenize(entity):
            for w in norm:
                if w.lower() == word.lower():
                    return nicknames.index(entity)
    return False


def find_entity(full_name, norm):

    for entity in full_name:
        for word in nltk.word_tokenize(entity):
            for w in norm:
                if w.lower() == word.lower():
                    return full_name.index(entity)
    return False


def check_conflicts(entity_1, entity_2, clauses):

    entity_1_comb = combinations(entity_1.keys(), 2)

    entity_2_comb = combinations(entity_2.keys(), 2)

    conflicts = []

    for comb in entity_1_comb:

        norm_1 = comb[0]
        norm_2 = comb[1]

        if entity_1[norm_1][0] != entity_1[norm_2][0]:

            semantic_similarity = similarity(entity_1[norm_1][1], entity_1[norm_2][1])

            if semantic_similarity >= THRESHOLD:
                conflicts.append((norm_1, norm_2, semantic_similarity*100))

    for comb in entity_2_comb:

        norm_1 = comb[0]
        norm_2 = comb[1]

        if entity_2[norm_1][0] != entity_2[norm_2][0]:

            semantic_similarity = similarity(entity_2[norm_1][1], entity_2[norm_2][1])

            if semantic_similarity >= THRESHOLD:
                conflicts.append((norm_1, norm_2, semantic_similarity*100))

    return conflicts