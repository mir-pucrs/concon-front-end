# -*- coding:utf-8 -*-
import os
import sys
# import threading
import pypandoc
from constants import *
from nltk.tokenize import sent_tokenize
from models import Contracts, Clauses
from preprocess_norms import to_matrix
from django.conf import settings
from keras.models import  model_from_json
from django.core.files.storage import FileSystemStorage
from conflict_models.msc_model.party_identification.extracting_parties import extract_parties
from conflict_models.msc_model.rule_functions import *
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

clause_classifier, vec = get_classifier()
SUCCESS = 'SUCCESS'
ERR = 'ERROR'
WARN = 'WARNING'


def new_confidence(x): return abs(x - 0.5) * 2


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text


def save_contract(up_file, user_id):
    
    # Check if there is an existing folder for the user.
    # If yes, check if there is an existing contract with the same name.
    user_folder_path = os.path.join(settings.MEDIA_URL, str(user_id))
    abs_user_folder = os.path.join(settings.MEDIA_ROOT, str(user_id))

    # Check the folder existence.
    if os.path.isdir(abs_user_folder):
        name, _ = os.path.splitext(up_file.name)
        file_path = os.path.join(abs_user_folder, str(name + '.txt'))

        print name, "folder exists"

        # Check the file existence.
        if os.path.isfile(file_path):
            # Return with a message.

            print "file exists!!"
            return WARN, "Hey! You've already uploaded this contract."

    else:
        os.makedirs(abs_user_folder)

    # Save file as it is.    
    fs = FileSystemStorage(location=abs_user_folder, base_url=user_folder_path)
    filename = fs.save(up_file.name, up_file)
    file_url = fs.url(filename)
    full_file_url = settings.BASE_DIR + file_url

    # Check its extension.
    name, extension = os.path.splitext(filename)

    if extension == '.pdf':

        print "pdf", extension

        print file_url

        try:            
            txt = convert_pdf_to_txt(full_file_url)
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            return ERR, "Error: %s" % e
        
    elif extension != '.txt' and extension != '.shtml':

        print "pypandoc", extension

        try:
            txt = pypandoc.convert_file(full_file_url, 'rst')
        except: # catch *all* exceptions
            print "some error"
            e = sys.exc_info()[0]
            return ERR, "Error: %s" % e
    
    elif extension == '.txt':

        print "nothing to do here", extension
        return SUCCESS, file_url

    elif extension == '.shtml':

        txt = open(full_file_url, 'r').read()


    # Create a new path to save the converted file.
    new_file_url = file_url[:-(len(extension))] + '.txt'

    # Save new file with the same name but with a different extension.
    with open(settings.BASE_DIR + new_file_url, 'w') as w_file:

        w_file.write(txt.encode('utf-8', "ignore"))

    w_file.close()

    # Remove the first file.
    os.remove(full_file_url)

    return SUCCESS, new_file_url


def insert_contract(path, user_obj):

    # Get the file name to save into the base.
    file_path = path.split('/')[-1]
    filename, _ = os.path.splitext(file_path)

    # Read file.
    file_text = open(path, 'r').read()

    # Break into sentences.
    try:
        sentences = sent_tokenize(file_text.decode('utf-8', 'ignore'))
    except:
        sentences = []

    sent_ranges = []

    for ind, sentence in enumerate(sentences):
        # Run over the sentences and get their range in the text.
        min_limit = file_text.find(sentence.encode('utf-8', 'ignore'))
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


# def check_pair(conflicts, clauses, pair, model):

#    matrix = to_matrix(clauses[pair[0]], clauses[pair[1]], MAX_LENGTH)

#    pred = model.predict(matrix)

#    new_pred = new_confidence(pred) 
    # pred_class = pred.argmax(axis=1)

#    if new_pred > 0.7:
#        conflicts.append((pair[0], pair[1], int(new_pred*100)))


def check_conflict(clauses, pairs):

    # Get model.
    # net = get_model(MAX_LENGTH)
    json_file = open(PATH_TO_MODEL, 'r')	
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    
    model.load_weights(PATH_TO_WEIGHTS)
   
    # net.load_weights(WEIGHTS)

    conflicts = []
    
    # threads = []

    for pair in pairs:

        matrix = to_matrix(clauses[pair[0]], clauses[pair[1]], MAX_LENGTH)

        pred = model.predict(matrix)

	if pred[0][1] > 0.5:
	    new_pred = new_confidence(pred[0][1]) 
	else:
	    continue
    # pred_class = pred.argmax(axis=1)

        if new_pred > 0.8:
            conflicts.append((pair[0], pair[1], int(new_pred*100)))

	# t = threading.Thread(target=check_pair, args=(conflicts, clauses, pair, model))
	# threads.append(t)
	# t.start()        
	# t.join()

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
