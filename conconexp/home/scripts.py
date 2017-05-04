import os
import threading

from constants import *
from itertools import combinations
from nltk.tokenize import sent_tokenize
from models import Contracts, Clauses
from preprocess_norms import turn_into_matrix, to_matrix
from keras.models import  model_from_json
from conflict_models.msc_model.party_identification.extracting_parties import extract_parties
from conflict_models.msc_model.rule_functions import *

clause_classifier, vec = get_classifier()


def insert_contract(path, user_obj):

    # Get the file name to save into the base.
    file_path = path.split('/')[-1]
    filename, _ = os.path.splitext(file_path)

    # Read file.
    file_text = open(path, 'r').read()

    # Break into sentences.
    sentences = sent_tokenize(file_text)

    sent_ranges = []

    for ind, sentence in enumerate(sentences):
        # Run over the sentences and get their range in the text.
        min_limit = file_text.find(sentence)
        max_limit = min_limit + len(sentence)

        sent_ranges.append((min_limit, max_limit))

    # Insert contract.
    ins = Contracts(con_name=filename, path_to_file=path, added_by_id=user_obj)
    ins.save()

    # Get the contract id.
    contract_id = ins.con_id

    for i, rng in enumerate(sent_ranges):
        # Insert each clause from contract.
        ins_cls = Clauses(con_id=contract_id, clause_range=rng)
        ins_cls.save()

    return contract_id


def is_norm(clause):

    vec_clause = vec.fit_transform([clause])
    clause_class = clause_classifier.classifier.predict(vec_clause.A)

    if clause_class[0] == 1:
        return True
    else:
        return False


def get_norm_pairs(norms):

    return combinations(norms, 2)


def check_pair(conflicts, clauses, pair, model):

   matrix = to_matrix(clauses[pair[0]], clauses[pair[1]], MAX_LENGTH)

   pred = model.predict(matrix)

   # pred_class = pred.argmax(axis=1)

   if pred[0][1] > 0.7:
       conflicts.append((pair[0], pair[1], int(pred[0][1]*100)))


def check_conflict(clauses, pairs):

    # Get model.
    #net = get_model(MAX_LENGTH)
    json_file = open(PATH_TO_MODEL, 'r')	
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    
    model.load_weights(PATH_TO_WEIGHTS)
   
    #net.load_weights(WEIGHTS)

    conflicts = []
    
    threads = []

    for pair in pairs:

	t = threading.Thread(target=check_pair, args=(conflicts, clauses, pair, model))
	threads.append(t)
	t.start()        
	t.join()
	#matrix = to_matrix(clauses[pair[0]], clauses[pair[1]], MAX_LENGTH)

        #pred = model.predict(matrix)

        # pred_class = pred.argmax(axis=1)

        #if pred[0][1] > 0.7:
        #    conflicts.append((pair[0], pair[1], int(pred[0][1]*100)))


    return conflicts


class Contract:
    def __init__(self, contract_id):

        self.contract_id = contract_id
        self.contract_path = Contracts.objects.get(con_id=self.contract_id).path_to_file
        self.file_text = open(self.contract_path, 'r').read()
        self.clause_ranges = Clauses.objects.filter(con_id=self.contract_id).order_by('clause_id')
        self.clauses = dict()
        self.norms = list()

    def get_path(self):
        # Get contract path.
        return self.contract_path

    def get_contract_text(self):

        return self.file_text

    def get_clauses(self):

        return self.clause_ranges

    def process_clauses(self):

        # Create a list to store each sentence.
        for row in self.clause_ranges:

            rng = row.clause_range
            rng_values = rng.strip('()').split(',')
            min_limit = int(rng_values[0])
            max_limit = int(rng_values[1])

            clause_text = self.file_text[min_limit:max_limit]

            # Check if it is norm.
            if is_norm(clause_text):
                self.norms.append(row.clause_id)

            # Save clause texts.
            self.clauses[row.clause_id] = clause_text


def cnn_model(contract_id):
    cntrct = Contract(contract_id)

    cntrct.process_clauses()

    # Create norm pairs to compare.
    pairs = get_norm_pairs(cntrct.norms)

    # Find conflicts.
    conflicts = check_conflict(cntrct.clauses, pairs)

    # Return the sentences.
    return cntrct.clause_ranges, cntrct.clauses, conflicts


def msc_model(contract_id):
    cntrct = Contract(contract_id)

    cntrct.process_clauses()

    # Find parties.
    entities = extract_parties(cntrct.file_text)

    if type(entities) == str or not entities:
        return cntrct.clause_ranges, cntrct.clauses, []
    else:        
        
        # Check modalities if norms have the entities.
        entity_1, entity_2 = check_norms(entities, cntrct.norms, cntrct.clauses)

        # Find conflicts.
        conflicts = check_conflicts(entity_1, entity_2, cntrct.clauses)

        return cntrct.clause_ranges, cntrct.clauses, conflicts
