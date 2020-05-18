# -*- coding:utf-8 -*-
import os
import sys
import nltk
import random
from django.conf import settings
from scripts import insert_contract
from constants import get_classifier
from models import AuthUser, Contracts, Clauses, Conflicts, ConflictTypes

# Constants.
ROOT_PATH = '/home/site/concon-front-end-master/conconexp/home/data\
/manufacturing/'
CONFLICTS_PATH = 'data/conflicts'
USER_ID = 22 # Special user that saves all contracts.

class ConflictCreator():
    """
        Class that creates a system to generate new conflicts given real
        norms.
    """
    def __init__(self):
        self.user_id = None
        self.contract_id = None
        self.contract_path = ''
        self.contract_name = ''
        self.contract_text = ''
        self.n_altered_norms = 0
        self.conflicts = dict()
        self.norms = dict()
        self.n_norms = 0
        
    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_contract(self, con_id):
        # Get a contract from DB given a contract id.
        sel_cntrct = Contracts.objects.get(con_id=con_id)
        self.contract_name = sel_cntrct.con_name
        self.contract_path = sel_cntrct.path_to_file
        self.contract_id = sel_cntrct.con_id
        self.contract_text = open(self.contract_path, 'r').read()
        # Get the number of norms and altered norms.
        self.n_norms = Clauses.objects.filter(con_id=self.contract_id,
            norm=1).count()
        self.n_altered_norms = Conflicts.objects.filter(
            con_id=self.contract_id, added_by=USER_ID).count()
        # To ensure that people don't get the same norms over and over,
        # don't let the number of altered norms be the same as norms.
        if self.n_altered_norms == ((self.n_norms/2) - 1):
            self.n_norms = 0
            self.n_altered_norms = 0
            self.select_contract()

    def select_contract(self):
        # From ROOT_PATH, select a random contract, make a copy and
        # save into database.
        # Select the contract.
        contracts = os.listdir(ROOT_PATH)
        contract = random.choice(contracts)
        contract_path = os.path.join(ROOT_PATH, contract)
        # Modify the original contract name to highlight it has
        # conflicts.
        original_name, ext = os.path.splitext(contract)
        self.contract_name = original_name + "_conflicting"

        # Check if the contract was selected before.
        sel_cntrct = Contracts.objects.filter(con_name=self.contract_name)
        if sel_cntrct:
            # Get info from database.
            sel_cntrct = sel_cntrct[0]
            self.contract_id   = sel_cntrct.con_id
            self.contract_path = sel_cntrct.path_to_file            
        else:
            # Save the new file on the contract annotator user folder.
            abs_user_folder = os.path.join(settings.MEDIA_ROOT, str(USER_ID))
            # Check the folder existence.
            if not os.path.isdir(abs_user_folder):
                os.makedirs(abs_user_folder)
            # Create the new file path.
            self.contract_path = os.path.join(abs_user_folder, str(
                self.contract_name + '.txt'))
            # Get the original text from contract.
            original_text = open(contract_path, 'r').read()
            # Open the new file to write the content from contract.
            write_file = open(self.contract_path, 'w')
            # Write original text.
            write_file.write(original_text)
            # Close file.
            write_file.close()
            # Insert the new contract to DB.
            user_obj = AuthUser.objects.get(id=USER_ID).pk
            self.contract_id = insert_contract(self.contract_path, user_obj)
        # Read contract text.    
        self.contract_text = open(self.contract_path, 'r').read()

    def get_new_contract(self):
        # Select a new contract.
        self.select_contract()
        self.get_norms()

    def get_norms(self):
        # Use sentence classifier to select norms from contract
        # sentences.
        min_n_of_norms = 5
        # Check if a contract was previously selected.
        if not self.contract_id:
            self.select_contract()

        # Retrieve sentences from contract that are assigned as norms.
        con_obj = Clauses.objects.filter(con_id=self.contract_id, norm=1)

        if con_obj.count() > min_n_of_norms:
            # If the number of norms already assingned in a contract is
            # higher than a 
            for row in con_obj:
                rng_values = row.clause_range.strip('()').split(',')
                min_limit = int(rng_values[0])
                max_limit = int(rng_values[1])
                self.norms[row.clause_id] = self.contract_text[
                    min_limit:max_limit]
                self.n_norms += 1
        else:
            # Set classifier.
            sent_classifier, vec = get_classifier()
            con_obj = Clauses.objects.filter(con_id=self.contract_id)
            if not con_obj:
                sys.exit(1)
            for row in con_obj:
                # Run over contract sentences.
                rng = row.clause_range
                rng_values = rng.strip('()').split(',')
                min_limit = int(rng_values[0])
                max_limit = int(rng_values[1])

                sent_text = self.contract_text[min_limit:max_limit]

                # Turn the sentence into vector.
                vec_sent = vec.fit_transform([sent_text])
                sent_class = sent_classifier.classifier.predict(vec_sent.A)

                if sent_class[0] == 1:
                    # Add to the norm set.
                    self.norms[row.clause_id] = sent_text
                    self.n_norms += 1
                    # Add info to DB.
                    if not row.norm:
                        row.norm = 1
                        row.modal_id = 1
                        row.save()

        if not self.n_norms:
            self.get_new_contract()

    def get_a_norm(self, norm_id=None):
        # Using the set of norms, select one at random.
        selected_norm_id = random.choice(self.norms.keys())
        if norm_id and norm_id == selected_norm_id:
            # If the selected norm is the same as the previous one, get
            # another one.
            return self.get_a_norm(norm_id=norm_id)
        return selected_norm_id

    def save_new_norm(self, new_norm):
        # Add norm text to contract file.
        cntrct_len = len(self.contract_text)
        norm_len = len(new_norm)
        w_file = open(self.contract_path, 'a')
        w_file.write(' ' + new_norm)
        w_file.close()
        # Save norms into Clauses table.
        # Add 1 to cntrct_len to consider the space.
        cntrct_len = cntrct_len + 1
        rng = '(%d, %d)' % ((cntrct_len), (cntrct_len + norm_len))
        cls_insert = Clauses(con_id=self.contract_id, clause_range=rng,
            norm=1)
        cls_insert.save()
        # Add norm to contract text var.
        self.contract_text += ' ' + new_norm

        return cls_insert.clause_id

    def save_conflict(self, norm_id, new_norm_id, type_id):
        # Save conflict to database.
        conf_type_obj = ConflictTypes.objects.get(type_id=type_id)
        norm_1 = Clauses.objects.get(clause_id=norm_id)
        norm_2 = Clauses.objects.get(clause_id=new_norm_id)
        user_obj = AuthUser.objects.get(id=self.user_id)
        cnflct_insert = Conflicts(con_id=self.contract_id,
            clause_id_1=norm_1, clause_id_2=norm_2, confidence=100,
            added_by=user_obj, type_id=conf_type_obj)
        cnflct_insert.save()

    def save_conflicts(self):
        # Save all created conflicts on DB and in a new contract.
        if self.conflicts:
            
            # Create a new contract name and save it on the DB
            # and in a file.
            contract_path, ext = os.path.splitext(self.contract_path)
            cntrct_name = contract_path.split('/')[-1]
            cntrct_name = cntrct_name + "_conflicting"
            # Check if the new contract already exists on the DB.
            cntrct_query = Contracts.objects.filter(con_name=cntrct_name)
            if cntrct_query:
                # If it already is on DB.
                # Get info from database.
                cntrct = cntrct_query[0]
                cntrct_id = cntrc.con_id
                cntrct_path = cntrc.path_to_file
                cntrct_obj = Contracts.objects.get(con_id=cntrct_id)
                file_write = open(cntrct_path, "a") # Append to file.
            else:
                # If not, create a new file and add to DB.
                # Save the new file on the contract annotator user
                # folder.
                abs_user_folder = os.path.join(settings.MEDIA_ROOT, str(
                    USER_ID))
                # Check the folder existence.
                if not os.path.isdir(abs_user_folder):
                    os.makedirs(abs_user_folder)
                # Create file name.
                cntrct_path = os.path.join(abs_user_folder, str(
                    cntrct_name + '.txt'))
                file_write = open(cntrct_path, 'w')
                # Write original text.
                file_write.write(self.contract_text)
                # Insert the new contract to DB.
                user_obj = AuthUser.objects.get(id=USER_ID).pk
                cntrct_id = insert_contract(cntrct_path, user_obj)
                    
            text_len = len(self.contract_text)
            for norm_id in self.conflicts:

                norm = self.conflicts[norm_id]
                # Write new norms (that conflict with original ones).
                file_write.write(" " + norm)
                # Add norm to Clauses table.
                norm_len = len(norm)
                # Add 1 to text_len to jump the space.
                text_len = text_len + 1
                rng = '(%d, %d)' % (text_len, (text_len + norm_len))
                # Insert the clause.
                cls_insert = Clauses(con_id=cntrct_id, clause_range=rng,
                    norm=1)
                cls_insert.save()
                text_len = text_len + norm_len

                # Add new conflict.
                new_norm_id = cls_insert.clause_id
                conf_insert = Conflicts(con_id=cntrct_id, clause_id_1=norm_id, 
                    clause_id_2=new_norm_id, confidence=100,
                    added_by=self.user_id)
                conf_insert.save()

            file_write.close()
            self.conflicts = dict()


def remove_norm(norm_id):
    Clauses.objects.filter(clause_id=norm_id).update(norm=0)

if __name__ == '__main__':
    
    cc = ConflictCreator()
    cc.get_contract()
    print "Selected contract: %s\nPath: %s\nText excerpt: %s" % (
        cc.contract_name, cc.contract_path, cc.contract_text[:10])
