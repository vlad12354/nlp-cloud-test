"""
similarity function
"""

import pandas as pd
from fuzzywuzzy import fuzz


# list = RECEIVED BY ANGEL

def match_and_output(list):

    df = pd.read_csv('glossary.csv')
    size = df.shape[0]
    out_dict = {}
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
        out_dict[term]= df['definition'].ix[max_ind]


    return out_dict






