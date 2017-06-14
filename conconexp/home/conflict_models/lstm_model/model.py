import csv
import random
import numpy as np
from extract_features import *
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ModelCheckpoint
from keras.callbacks import Callback
from keras.callbacks import History
from keras.callbacks import EarlyStopping

MAX_FEATURES = 200
NB_CLASSES = 2


def get_model():

    model = Sequential()
    model.add(Embedding(MAX_FEATURES, output_dim=256))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(NB_CLASSES, activation='softmax'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    return model


def train(model, x_train, y_train, x_val, y_val):

    # Set checkpointers to monitor loss anc accuracy during train.
    checkpointer = ModelCheckpoint(
                                 filepath='weights.hdf5',
                                 verbose=1,
                                 save_best_only=True
                                 )

    acc_loss_monitor = History()

    early_stopping = EarlyStopping(monitor='val_loss', patience=22, verbose=1)
   
    model.fit(x_train, y_train, batch_size=16,
          verbose=1, validation_data=(x_val, y_val), callbacks=[checkpointer, acc_loss_monitor, early_stopping])
 
#    model.fit(x_train, y_train, batch_size=16, epochs=10, verbose=1, validation_data=(x_val, y_val))

    return model


def test(model, x_test, y_test):

    model.load_weights('weights.hdf5')

    score = model.evaluate(x_test, y_test, batch_size=16, verbose=1)

    print "Score:", score

    tp, tn, fp, fn = 0, 0, 0, 0

    #print 'before prediction', tup
	
    pred = model.predict(x_test, batch_size=1, verbose=1)

    #print 'after prediction', pred
    for i in range(len(y_test)):

        clss = int(np.argmax(np.round(pred[i])))
        golden = int(np.argmax(y_test[i]))

        print golden, clss

        if golden == 1 == clss:
            tp += 1            
        elif golden == 0 == clss:
            tn += 1
        elif golden != clss == 1:
            fp += 1
        elif golden != clss == 0:
            fn += 1 

    print "Tp: %d, Tn: %d, Fp: %d, Fn: %d" % (tp, tn, fp, fn)
    prec = tp/float(tp + fp)
    rec = tp/float(tp + fn)
    f_measure = 2*((prec * rec)/float(prec + rec))

    print "Precision: %.2f, Recall: %.2f, F-Measure: %.2f" % (prec, rec, f_measure)


def get_data(data_path):
    
    nb_words = 200
    tokenizer = Tokenizer(nb_words=nb_words)

    conflict, non_conflict = [], []

    with open(data_path, 'r') as csv_file:

        rdr = csv.reader(csv_file)

        for ind, row in enumerate(rdr):

            if ind > 0:
                if int(row[-1]) == 1:
                    conflict.append(((row[1], row[2]), int(row[-1])))
                elif int(row[-1]) == 0:
                    non_conflict.append(((row[1], row[2]), int(row[-1])))

    random.shuffle(non_conflict)
    n_conflicts = len(conflict)
    data = conflict + non_conflict[:n_conflicts]

    X = [' '.join(annotate_text(tup[0][0]) + annotate_text(tup[0][1])) for tup in data]
    y = [tup[1] for tup in data]

    y = np_utils.to_categorical(y, NB_CLASSES)

    tokenizer.fit_on_texts(X)
    
    X = tokenizer.texts_to_sequences(X)   

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=42)

    X_train = sequence.pad_sequences(X_train, 200)
    X_val =  sequence.pad_sequences(X_val, 200)
    X_test = sequence.pad_sequences(X_test, 200) 

    return X_train, y_train, X_val, y_val, X_test, y_test

if __name__ == "__main__":

    data_path = 'dataset/dataset.csv'

    model = get_model()

    X_train, y_train, X_val, y_val, X_test, y_test = get_data(data_path)

    model = train(model, X_train, y_train, X_val, y_val)

    test(model, X_test, y_test)
