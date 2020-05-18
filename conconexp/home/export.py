from models import Clauses, Contracts


class Contract():
    """docstring for Contract"""
    def __init__(self, con_id):
        self.con_id = con_id
        self.con_obj = Contracts.objects.get(con_id=con_id)
        self.con_path = con_obj.path_to_file
        self.text = open(self.con_path, 'r').read()
        self.sentences = Clauses.objects.filter(con_id=self.con_id)
            
    def annotate(self):
        pass

