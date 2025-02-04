import pandas as pd
from collections import Counter
import nltk
from pyvis.network import Network

# Vars
vocab = pd.read_pickle('./data/vocab')
doc_lt = pd.read_pickle('./data/doc_lookup_table')
doc_lt = pd.read_pickle('./data/temp.pkl')
vocab_lt = pd.read_pickle('./data/vocab_lookup_table')

# Word Freq Visualization
def visualizeWordFreqData():
    colorcode_dict = {}

visualizeWordFreqData()