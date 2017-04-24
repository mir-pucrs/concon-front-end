from nltk.tokenize import sent_tokenize
from models import Contracts, Clauses

def handle_uploaded_file(f):
    filename = f.name
    with open('media/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def insert_contract(path, user_id):

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
    ins = Contracts(con_name = name, path_to_file = path, added_by = user_id)
    ins.save()

    # Get the contract id.
    sel = Contracts.objects.get(path_to_file=path)

    contract_id = sel.con_id

    for i, rng in enumerate(sent_ranges):
        ins_cls = Clauses(con_id=contract_id, clause_range=rng)
        ins_cls.save()
