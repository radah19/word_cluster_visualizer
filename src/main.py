import pandas as pd
from nltk.stem import LancasterStemmer
from pyvis.network import Network
import random
from spellchecker import SpellChecker

def main():
    visualizeWordFreqData()

# Vars ----------------------------------------------------------------------------------------------
# vocab = pd.read_pickle('./data/vocab')
doc_lt = pd.read_pickle('./data/doc_lookup_table')
# doc_lt = pd.read_pickle('./data/temp.pkl')
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

    # Update Physics variables for graph
    net.set_options("""{
        "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -200,
                "centralGravity": 0.15,
                "springLength": 50,
                "springConstant": 0.2,
                "damping": 0.9,
                "avoidOverlap": 1
            },
            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 25,
                "fit": true
            },
            "minVelocity": 0.75,
            "maxVelocity": 30
        }
    }""")
    
    colorcode_dict = {}
    lancaster = LancasterStemmer()
    spell = SpellChecker()
    stem_groups = {}

    for word, word_freq in word_freqs.items():
        if word == None:
            continue

        # Find closest properly spelt stem
        corrected_word = spell.correction(word)
        stemmed_word = lancaster.stem(corrected_word if corrected_word != None else word)

        # Associate common color to the stem
        if stemmed_word not in stem_groups:
            stem_groups[stemmed_word] = []
            colorcode_dict[stemmed_word] = "%06x" % random.randint(0, 0xFFFFFF)

        stem_groups[stemmed_word].append(word)

        # Add Node to diagram
        net.add_node(
            word, 
            size=min(word_freq * 5, 100), 
            # color= f"#{colorcode_dict[stemmed_word]}", 
            label=f"{word}\n({word_freq})",
            group=stemmed_word
            )

        # Add edges to common node to group them together
        if len(stem_groups[stemmed_word]) > 1:
            net.add_edge(
                word,
                stem_groups[stemmed_word][0],
                width=0
            )

    net.save_graph('word_freq_diagram.html')

main()