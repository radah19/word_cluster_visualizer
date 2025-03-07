import os
import pandas as pd
from pyvis.network import Network
import random
from spellchecker import SpellChecker
from affixspellchecker import AffixSpellChecker
import time
from tqdm import tqdm
import nltk
nltk.download('words')
from nltk.corpus import words as nltk_words

def main():
    choice = -1

    while choice == -1:
        print("\nChoose an algorithm to run: \n\t1 - Word Frequency Visualizer \n\t2 - Word Cluster Visualizer \n\t3 - Word Cluster w/ Frequency Visualizer \n\t4 - Quit \nex usage: \'1\'\n")
        choice = input()
        match choice:
            case "1": # Word Frequency Visualizer
                threshold = int(input("Enter threshold value to filter by as number: "))

                docsize_choice = input("Choose a document size to look through: \n\t- vs (Very Small)\n\t- sm (Small)\n\t- lg (Large)\nex usage: \'sm\'\n")
                doc_choice = None

                match docsize_choice:
                    case "vs":
                        doc_choice = vs_doc_lt
                    case "sm":
                        doc_choice = sm_doc_lt
                    case "lg":
                        doc_choice = lg_doc_lt
                    case _:
                        print("Size not found")
                        choice = -1
                        return
                
                spellcheck_lvl = input("Enter the associated value of type of spellchecker to use: \n\t1 - pyspellchecker with Distance=1 (Fast)\n\t2 - pyspellchecker with Distance=2 (Precise)\n\t3 - AffixSpellChecker (Prioritizes Affixes)\n")
                spellchecker_choice = None

                match spellcheck_lvl:
                    case "1":
                        spellchecker_choice = "Peter Norvig Spellchecker - Distance = 1"
                    case "2":
                        spellchecker_choice = "Peter Norvig Spellchecker - Distance = 2"
                    case "3":
                        spellchecker_choice = "Affix Spellchecker"
                    case _:
                        print("Invalid Value")
                        choice = -1
                        return
             
                print("Threshold: ", threshold, " | Document Size: ", docsize_choice, " | Spellchecker: ", spellchecker_choice)
                visualizeWordFreqData(threshold, doc_choice, spellcheck_lvl)

            case "2": # Word Cluster Visualizer
                min_threshold = int(input("Enter minimum threshold value (clusters with less words than this threshold are not included): "))
                max_threshold = int(input("Enter maximum threshold value (clusters with more words than this threshold are not included): "))
                visualizeClusterCompData(min_threshold, max_threshold)

            case "3": # Word Cluster w/ Frequency Visualizer
                print("N/A")

            case "4": # Quit
                print("Quitting app")

            case _:
                print("Option invalid/unavailable, please try again")
                choice = -1
    
# Vars ----------------------------------------------------------------------------------------------
# vocab = pd.read_pickle('./pickles/vocab')
# vocab_lt = pd.read_pickle('./pickles/vocab_lookup_table')

lg_doc_lt = pd.read_pickle('./pickles/doc_lookup_table')
sm_doc_lt = pd.read_pickle('./pickles/sm_doc_lookup_table')
vs_doc_lt = pd.read_pickle('./pickles/vs_doc_lookup_table')

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

# Word Freq Visualization ---------------------------------------------------------------------------
def visualizeWordFreqData(threshold: int, doc_lt: dict, spellcheck_lvl: int):
    timer = 0

    # Count Word Frequencies, then filter words not meeting a threshold
    all_words_freqs = {}

    timer = time.time()

    for doc, doc_val in tqdm(doc_lt.items(), desc="Counting Frequencies of all Words across documents".ljust(65)):
        for word in doc_val:
            # Prevent Nulls from being added
            if word == None:
                continue       

            # Count up times used across documents
            if word not in all_words_freqs:
                all_words_freqs[word] = 0
            all_words_freqs[word] += 1

    print("\tExecution time: ", time.time() - timer, " seconds")

    # Filter by Threshold Value
    timer = time.time()

    word_freqs = {}
    for word, word_freq in tqdm(all_words_freqs.items(), desc="Filtering words with frequencies below threshold".ljust(65)):
        if word_freq >= threshold:
            word_freqs[word] = word_freq
    print("\tExecution time: ", time.time() - timer, " seconds")

    # Match Similar Words based on Levenshtein Distance
    colorcode_dict = {}
    root_groups = {}
    corrected_groups = {}

    spell = None
    if spellcheck_lvl == 1:
        spell = SpellChecker(distance=1)
    elif spellcheck_lvl == 2:
        spell = SpellChecker()
    else:
        spell = AffixSpellChecker()

    timer = time.time()

    for word, word_freq in tqdm(word_freqs.items(), desc="Spell Checking words via Levensthein Algorithm & Grouping them".ljust(65)):
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
    
    print("\tExecution time: ", time.time() - timer, " seconds")

    # Create Visual Graph
    timer = time.time()

    for word, word_freq in tqdm(word_freqs.items(), desc="Generating Graph...".ljust(65)):
        _group = corrected_groups[word]  

        if len(root_groups[_group]) > 1:
            # Add Node to diagram
            net.add_node(
                word, 
                size=max(min(word_freq / 2, 30), 3), 
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
    
    print("\tExecution time: ", time.time() - timer, " seconds")

    print("Done! Look for word_freq_diagram.html")
    net.save_graph('word_freq_diagram.html')

def visualizeClusterCompData(min_threshold: int, max_threshold: int):
    timer = 0

    # Merge pickled information into one list
    timer = time.time()

    directory = './connected_comps_pickles'
    final_ls = []
    for filename in tqdm(os.scandir(directory), desc="Compiling cluster list from data: "):
        ls = pd.read_pickle(os.path.join(filename))

        for i in ls:
            if len(i) >= min_threshold and len(i) <= max_threshold:
                final_ls.append(i)

    print("\tExecution time: ", time.time() - timer, " seconds")

    # Generate Graph
    timer = time.time()

    word_set = nltk_words.words()

    for ls in tqdm(final_ls, desc="Generating Graph & Pairing words"):
        # Edge case in case there's only one word
        if len(ls) <= 1:
            net.add_node(
                word, 
                size=2,  
                label=f"{word}",
                group=word
                )
            continue

        # Identify Correct Word to link the words to, or at least the closest
        correct_word = ls[0]

        for word in ls: 
            if word in word_set:
                correct_word = word
                break

        net.add_node(
            correct_word, 
            size=5, 
            label=f"{word}",
            group=correct_word
            )
        
        for word in ls: 
            if word != correct_word:
                net.add_node(
                    word, 
                    size=2, 
                    label=f"{word}",
                    group=correct_word
                    )
    
                net.add_edge(
                    word,
                    correct_word,
                    width=0
                )

    print("\tExecution time: ", time.time() - timer, " seconds")

    print("Done! Look for cluster_comp_diagram.html")
    net.save_graph('cluster_comp_diagram.html')

main()