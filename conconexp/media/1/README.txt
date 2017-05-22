Norm Conflict Identification
============================

This project aims to create a system able to read natural language
contracts and identify conflicts between their norms.

To Do
-----

-  [x] Add instructions on how to run this system
-  [x] Add references (with links) to the papers we published on this
   (only COIN so far)

Files
~~~~~

So far, we have the following files:

-  `global\_variables.py <global_variables.py>`__: Variables for common
   use.

-  `preprocess\_norm.py <preprocess_norm.py>`__: Algorithm that
   initiates a norm processing given a contract file path.

Classes
'''''''

The following classes define the structures needed to manipulate
contracts and norms and find conflicts.

-  `contract.py <contract.py>`__

-  `norm.py <contract.py>`__

-  `party.py <party.py>`__

Folders
'''''''

-  `data <data/>`__: Folder with contracts for dataset creation and gold
   standard for sentence classifier train.

-  `dataset\_creator <dataset_creator/>`__: Folder with the process of
   manual labeling of contract sentences. We classify them as *norm* and
   *no norm*.

-  `sentence\_classifier <sentence_classifier/>`__: Folder with the
   algorithm that generates a model to classify sentences as *norm* and
   *no norm*.

Prerequisites
~~~~~~~~~~~~~

The main code is not ready yet, however, to run other codes already
ready one must install the following packages:

-  `scikit-learn <http://scikit-learn.org/stable/install.html>`__

-  `corenlp <https://github.com/stanfordnlp/CoreNLP>`__

-  `corenlp
   python <https://github.com/dasmith/stanford-corenlp-python>`__

Execution
~~~~~~~~~

There are still nothing to execute, it will be filled in as we add more
codes.

Publications
~~~~~~~~~~~~

-  `COIN
   2015 <http://coin2015.tbm.tudelft.nl/files/2015/06/COINIJCAI_2015_submission_7-1.pdf>`__

