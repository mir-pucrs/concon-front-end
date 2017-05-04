"""
    Class that allows one to train a new classifier and test an existing one.
"""

import os
import csv
import time
import random
from sklearn.externals import joblib
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

STANDARD_DATA_PATH = '../data/dataset/contract_sent_dataset.csv'
BASE_PATH_TO_FOLDS = '../data/dataset/folds/'

random.seed(42)


class SentenceClassifier:

    def __init__(self, classifier=None, debug=False):
        # Receive an existing classifier, default None.
        # When debug is True, it activates some 'print' commands.
        self.classifier = classifier
        self.debug = debug

    def preprocess_data(self, data_path, test_size=0.2):
        # Read a file from data_path and create an embedding for feature extraction.
        # Divide data into train and test.

        self.vectorizer = CountVectorizer(min_df=1)    # TfidfTransformer(min_df=1)
        self.corpus = []
        self.y = []
        
        with open(data_path, 'r') as csvfile:

            rdr = csv.reader(csvfile, delimiter=',')

            first = True

            for row in rdr:

                if first:
                    first = False
                    continue

                self.corpus.append(row[1])
                self.y.append(int(row[2]))

        X = self.vectorizer.fit_transform(self.corpus)
        self.names = self.vectorizer.get_feature_names()

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, self.y, test_size=test_size, random_state=42)

        if self.debug:
            print "Data preprocessed! We have a total of %d examples.\n\tNorm examples: %d\n\tNonNorm Examples: %d\n" % (len(self.corpus), len([x for x in self.y if x == 1]), len([x for x in self.y if x == 0]))
            print "Number of train examples: %d\nNumber of test examples: %d\n" % (self.X_train.shape[0], self.X_test.shape[0])

    def train(self, alg_classifier=SGDClassifier(loss='hinge', penalty='l2', random_state=42), n_folds=10):
        # Use alg_classifier to train a model with 10-fold cross validation.
        # The default value for alg_classifier is the SGDClassifier from scikit learn.

        if self.debug:
            print "Training classifier w/ " + str(n_folds) + "!"

        if not self.classifier:
            self.classifier = alg_classifier

        folds_path = BASE_PATH_TO_FOLDS + str(n_folds)
        if os.path.isdir(folds_path):
            os.listdir(folds_path)

        else:
            os.path.insert(0, '../data')
            from extra_codes import generate_folds

        self.classifier.fit(self.X_train, self.y_train)

    def test(self, save=True):
        # Use self.classifier to predict a new sentence.

        y_pred = []

        for exmpl in self.X_test:
            # Classify sentences and save their classes.
            y_pred.append(self.classifier.predict(exmpl))

        # Evaluate classification.
        acc = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)

        print "Accuracy: %.2f\nPrecision: %.2f\nRecall: %.2f\nF1-Score: %.2f" % (acc, precision, recall, f1)
        
        if save:
            # Save results and classifier.
            self.write_results(acc, precision, recall, f1)
            self.save_classifier()

    def predict_class(self, pred_set):
        
        y_pred = []

        if type(pred_set) == str:
            pred_set = [pred_set]


        vect = CountVectorizer(min_df=1, vocabulary=self.names)
        pred_set = vect.fit_transform(pred_set)

        if self.classifier:
            for exmpl in pred_set:                
                y_pred.append(self.classifier.predict(exmpl))

            return y_pred
        else:
            return "You need to set a classifier first. Train one or pass it by argument. Use load_classifer method to load an existing classifier."


    def write_results(self, acc, prec, rec, f1):

        if self.debug:
            print "Writing results..."

        total_examples = len(self.corpus)
        current_time = time.strftime("%y-%m-%d_%H:%M:%S")
        filename = "clf_results/classifier_results_" + current_time + ".txt"

        sentence = "Total examples: %d\n\nAccuracy: %.2f\nPrecision: %.2f\nRecall: %.2f\nF1-Score: %.2f" % (total_examples, acc, prec, rec, f1)

        with open(filename, 'w') as w_file:

            w_file.write(sentence)

    def save_classifier(self):
        
        if self.debug:
            print "Saving classifier..."

        current_time = time.strftime("%y-%m-%d_%H:%M:%S")
        os.makedirs('classifiers/' + current_time)
        filename = 'classifiers/'+ current_time +'/sentence_classifier_' + current_time + '.pkl'
        joblib.dump(self.classifier, filename)

        # Save names.
        with open('classifiers/' + current_time + '/sentence_classifier_' + current_time + '_names.txt', 'w') as w_file:

            for name in self.names:
                w_file.write(name + "\n")


    def load_classifier(self, clf_path):
        
        if self.debug:
            print "Loading classifier..."

        self.classifier = joblib.load(clf_path)


if __name__ == "__main__":
    
    clf = SentenceClassifier(debug=True)
    clf.preprocess_data(STANDARD_DATA_PATH)
    clf.train()
    clf.test()