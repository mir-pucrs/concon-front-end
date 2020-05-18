# coding: utf-8
import pandas as pd
import random
random.seed(42)

# Get norm sentence paths.
conflicts_path = '/home/aires/datasets/conflicts/conflicts.csv'
non_conflicts_path = '/home/aires/datasets/conflicts/non-conflicts.csv'
CONFLICT = 1
N_CONFLICT = 0

norms_seen = []
counter = 0
cnflcts = []
nn_cnflcts = []
y = []

# Read conflicts.
df_conflict = pd.read_csv(conflicts_path)

conf_rows = len(df_conflict) # Get the number of conflicting samples.

for i in range(conf_rows):
    # Get norm pair.
    norm1, norm2 = df_conflict['norm1'][i], df_conflict['norm2'][i]
    
    cnflcts.append((norm1, norm2))
    y.append(CONFLICT) # Mark the pair as a conflicting one.
    
    if norm1 not in norms_seen:
        # Avoid adding duplicates.
        norms_seen.append(norm1)
    if norm2 not in norms_seen:
        norms_seen.append(norm2)

# Read non-conflicts.
df_non_conflict = pd.read_csv(non_conflicts_path)

non_conf_rows = len(df_non_conflict)

for i in range(conf_rows):
    
    j = random.randint(0, non_conf_rows) # Get a random pair of non-conflicting norms.
    
    norm1, norm2 = df_non_conflict['norm1'][j], df_non_conflict['norm2'][j]
    
    nn_cnflcts.append((norm1, norm2))
    y.append(N_CONFLICT) # Mark the pair as a non-conflicting one.
    
    if norm1 not in norms_seen:
        norms_seen.append(norm1)
    if norm2 not in norms_seen:
        norms_seen.append(norm2)
        
norms = dict() # Create a dictionary to acess norms addresing an index for each one.
for i, x in enumerate(norms_seen):
    norms[x] = i

# Generating embeddings
embeddings = get_sentence_embeddings(norms_seen)#, ngram='unigrams', model='wiki')