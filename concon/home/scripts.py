from nltk.tokenize import sent_tokenize
from models import Contracts, Clauses


def insert_contract(path, user_obj):

    # Get the file name to save into the base.
    name = path.split('/')[-1][:-4]

    # Read file.
    file_text = open(path, 'r').read()

    # Break into sentences.
    sentences = sent_tokenize(file_text)

    sent_ranges = []
    last_char_read = 0

    for ind, sentence in enumerate(sentences):
        # Run over the sentences and get their range in the text.
        if not ind:
            sent_ranges.append((0, len(sentence)))
            last_char_read = len(sentence)
        else:
            sent_ranges.append((last_char_read + 1, last_char_read + len(sentence)))
            last_char_read += len(sentence)

    # Insert contract.
    ins = Contracts(con_name=name, path_to_file=path, added_by_id=user_obj)
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

    clauses = []

    # Create a list to store each sentence.
    for row in sel:

        rng = row.clause_range
        rng_values = rng[1:-1].split(',')
        min_limit = int(rng_values[0])
        max_limit = int(rng_values[1])

        clauses.append(file_text[min_limit:max_limit])

    # Return the sentences.
    return clauses
