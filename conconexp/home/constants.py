from sklearn.feature_extraction.text import CountVectorizer
from norm_identifier.sentence_classifier import SentenceClassifier

BASE_FOLDER_PATH = 'dataset/'
CLASSIFIER_PATH = '/home/lsa/conconexp/home/norm_identifier/classifiers/' \
                  '16-10-25_12:18:39/' \
                  'sentence_classifier_16-10-25_12:18:39.pkl'
PATH_TO_WEIGHTS = '/home/lsa/conconexp/home/model/model.h5'
PATH_TO_MODEL = '/home/lsa/conconexp/home/model/model.json'
NAMES_PATH = '/home/lsa/conconexp/home/norm_identifier/classifiers/' \
             '16-10-25_12:18:39/sentence_classifier_16-10-25_12:18:39_names.txt'
MAX_LENGTH = 200
WEIGHTS = '/home/lsa/conconexp/home/model/weights.hdf5'


def get_classifier():
    sent_classifier = SentenceClassifier()
    sent_classifier.load_classifier(CLASSIFIER_PATH)
    names = [n[:-1] for n in open(NAMES_PATH, 'r').readlines()]
    vec = CountVectorizer(vocabulary=names)

    return sent_classifier, vec
