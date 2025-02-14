import pandas as pd
from nltk.stem import LancasterStemmer
from pyvis.network import Network
import random
from spellchecker import SpellChecker

def main():
    visualizeWordFreqData()

# Vars ----------------------------------------------------------------------------------------------
# vocab = pd.read_pickle('./pickles/vocab')
# vocab_lt = pd.read_pickle('./pickles/vocab_lookup_table')

# doc_lt = pd.read_pickle('./pickles/doc_lookup_table')
doc_lt = pd.read_pickle('./pickles/sm_doc_lookup_table')
# doc_lt = pd.read_pickle('./pickles/vs_doc_lookup_table')

# Word Freq Visualization ---------------------------------------------------------------------------
def visualizeWordFreqData():
    # Count Word Frequencies, then filter words not meeting a threshold
    all_words_freqs = {}
    threshold = 3

    for doc, doc_val in doc_lt.items():
        for word in doc_val:
            # Prevent Nulls from being added
            if word == None:
                continue       

            # Count up times used across documents
            if word not in all_words_freqs:
                all_words_freqs[word] = 0
            all_words_freqs[word] += 1

    # Filter by Threshold Value
    word_freqs = {}
    for word, word_freq in all_words_freqs.items():
        if word_freq >= threshold:
            word_freqs[word] = word_freq

    # Match Similar Words based on Levenshtein Distance
    colorcode_dict = {}
    spell = SpellChecker()
    root_groups = {}
    corrected_groups = {}

    for word, word_freq in word_freqs.items():
        # Create source groups for grouping nodes later
        if word not in corrected_groups:
            corrected_word = spell.correction(word)
            source_word = corrected_word if corrected_word != None else word
            corrected_groups[word] = source_word
        else:
            source_word = corrected_groups[word]  

        # Associate groups
        if source_word not in root_groups:
            root_groups[source_word] = []
            colorcode_dict[source_word] = "%06x" % random.randint(0, 0xFFFFFF)
        
        if word not in root_groups[source_word]:
            root_groups[source_word].append(word)

    # Display Frequencies on PyVis HTML Graph
    net = Network()
    net.set_options("""{
        "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -200,
                "centralGravity": 0.15,
                "springLength": 10,
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

    # Create Visual Graph
    for word, word_freq in word_freqs.items():
        _group = corrected_groups[word]  

        if len(root_groups[_group]) > 1:
            # Add Node to diagram
            net.add_node(
                word, 
                size=min(word_freq * 5, 50), 
                # color= f"#{colorcode_dict[stemmed_word]}", 
                label=f"{word}\n({word_freq})",
                group=_group
                )

            # Add edges to common node to group them together
            if root_groups[_group][0] != word:
                net.add_edge(
                    word,
                    root_groups[_group][0],
                    width=0
                )

    net.save_graph('word_freq_diagram.html')

main()