import os
from nltk.tokenize import sent_tokenize
from models import Contracts, Clauses


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


def get_conflicts(contract_id):

    # Get contract path.
    contract_path = Contracts.objects.get(con_id=contract_id).path_to_file

    # Read file.
    file_text = open(contract_path, 'r').read()

    # Get ranges from clauses.
    sel = Clauses.objects.filter(con_id=contract_id).order_by('clause_id')

    clauses = dict()

    # Create a list to store each sentence.
    for row in sel:

        rng = row.clause_range
        rng_values = rng.strip('()').split(',')
        min_limit = int(rng_values[0])
        max_limit = int(rng_values[1])

        clauses[row.clause_id] = file_text[min_limit:max_limit]

    # Return the sentences.
    return sel, clauses
