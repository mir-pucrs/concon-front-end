# Sentence Classifier

In this folder, we have the algorithm that classifies sentences as norm or non norm.
In this approach, we use machine learning algorithms to create a model using labeled data from our [gold standard set](../data/dataset/contract_sent_dataset.csv).

### Files

This folder contains the following files:

- [sentence_classifier.py](sentence_classifier.py): Main class that allows one to train and test a machine learning algorithm, as well as load a classifier and test it.

- [classifiers](classifiers/): Sub folder that contains the classifiers already trained. We keep a historic of classifiers so we can choose the best one for the task of sentence classification.

- [clf_results](clf_results/): Sub folder with the results that each classifiers got when tested over our labeled data.

### Prerequisites

To run the ```sentence_classifier.py```, one must install first:

- [scikit-learn](http://scikit-learn.org/stable/install.html)

### Execution

To run the ```sentence_classifier.py```, one should execute the following command:

- ```python -B sentence_classifier.py```