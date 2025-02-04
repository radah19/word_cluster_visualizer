import pandas as pd
from nltk.stem import LancasterStemmer
from pyvis.network import Network
import random
from spellchecker import SpellChecker

def main():
    visualizeWordFreqData()

# Vars ----------------------------------------------------------------------------------------------
# vocab = pd.read_pickle('./data/vocab')
# doc_lt = pd.read_pickle('./data/doc_lookup_table')
doc_lt = pd.read_pickle('./data/temp.pkl')
# vocab_lt = pd.read_pickle('./data/vocab_lookup_table')


# Word Freq Visualization ---------------------------------------------------------------------------
def visualizeWordFreqData():
    # Simple Counter for Words
    word_freqs = {}

    for doc, doc_val in doc_lt.items():
        for word in doc_val:
            if word not in word_freqs:
                word_freqs[word] = 0
            word_freqs[word] += 1

    # Display Frequencies on PyVis HTML Graph
    net = Network()
    net.toggle_physics(True)
    
    colorcode_dict = {}
    lancaster = LancasterStemmer()
    spell = SpellChecker()

    for word, word_freq in word_freqs.items():
        if word == None:
            continue

        corrected_word = spell.correction(word)
        stemmed_word = lancaster.stem(corrected_word if corrected_word != None else word)

        if stemmed_word not in colorcode_dict:
            colorcode_dict[stemmed_word] = "%06x" % random.randint(0, 0xFFFFFF)

        net.add_node(
            word, 
            size=min(word_freq * 5, 100), 
            color= f"#{colorcode_dict[stemmed_word]}", 
            label=f"{word}\n({word_freq})"
            )

    net.save_graph('word_freq_diagram.html')

main()