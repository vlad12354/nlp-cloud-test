"""
XXX
"""


import numpy as np
from difflib import SequenceMatcher
import os
import pandas as pd
from fuzzywuzzy import fuzz


df = pd.read_csv('glossary.csv')

# list = RECEIVED BY ANGEL
list = [ 'Interest Rata']

size = df.shape[0]

for term in list:
    max = 0
    for j in range(0,size):
        gl_term = df['term'].ix[j]
        similarity = fuzz.token_sort_ratio( term, gl_term )
        if similarity >=max:
            max = similarity
            max_ind = j
    if max>80:
     print df['definition'].ix[max_ind]
     print max







