import pandas as pd
from pyvis.network import Network
from spellchecker import SpellChecker
from affixspellchecker import AffixSpellChecker
import time
from tqdm import tqdm
import nltk
nltk.download('words')
from nltk.corpus import words as nltk_words
import matplotlib.pyplot as plt
import numpy as np
from playwright.sync_api import sync_playwright

def main():
    choice = -1
    cluster_distances.sort()

    while choice == -1:
        print("\nChoose an algorithm to run: "
                "\n\t1 - Word Frequency Visualizer "
                "\n\t2 - Word Cluster Visualizer "
                "\n\t3 - Word Cluster w/ Frequency Visualizer "
                "\n\t4 - Sandbox "
                "\n\t5 - Quit \nex usage: \'1\'\n")

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
                visualizeWordFreqData(threshold, doc_choice, docsize_choice, spellcheck_lvl)

            case "2": # Word Cluster Visualizer
                distance = -1
                while(distance == -1):
                    new_dist = float(input(f"Choose a Distance Value for Clustering Algorithm Data | Selectable Distances:\n{cluster_distances}:\n\n"))

                    if new_dist not in cluster_distances:
                        print("Invalid Distance :(")
                    else:
                        distance = new_dist
                
                min_threshold = int(input("Enter minimum threshold value (clusters with less words than this threshold are not included) (-1 for none): "))
                max_threshold = int(input("Enter maximum threshold value (clusters with more words than this threshold are not included) (-1 for none): "))
                visualizeClusterCompData(distance, min_threshold, max_threshold)

            case "3": # Word Cluster w/ Frequency Visualizer
                distance = -1
                while(distance == -1):
                    new_dist = float(input(f"Choose a Distance Value for Clustering Algorithm Data | Selectable Distances:\n{cluster_distances}:\n\n"))

                    if new_dist not in cluster_distances:
                        print("Invalid Distance :(")
                    else:
                        distance = new_dist

                freq_threshold = int(input("Enter threshold value to filter by as number: "))

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
                
                min_cluster_threshold = int(input("Enter minimum threshold value (clusters with less words than this threshold are not included) (-1 for none): "))
                max_cluster_threshold = int(input("Enter maximum threshold value (clusters with more words than this threshold are not included) (-1 for none): "))
                
                print(f"Distance: {distance} | Freq. Threshold: {freq_threshold} | Doc Size: {docsize_choice} | Min Cluster Threshold: {min_cluster_threshold} | Max Cluster Threshold: {max_cluster_threshold}")
                visualizeClusterCompFreqData(distance, freq_threshold, doc_choice, min_cluster_threshold, max_cluster_threshold)

            case "4": # Sandbox
                for d in cluster_distances:
                    if d <= 0.077: 
                        visualizeClusterCompData(d, 2, 25)
                    elif d <= 0.154:
                        visualizeClusterCompData(d, 3, 25)
                    elif d <= 0.167:
                        visualizeClusterCompData(d, 4, 25)
                    elif d <= 0.188:
                        visualizeClusterCompData(d, 5, 25)
                    elif d <= 0.222:
                        visualizeClusterCompData(d, 7, 20)
                    else:
                        visualizeClusterCompData(d, 8, 20)

            case "5": # Quit
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

cluster_distances = [
    0.04, 0.059, 0.095, 0.136, 0.188, 0.231, 0.043, 0.062, 
    0.1, 0.143, 0.19, 0.235, 0.045, 0.067, 0.105, 0.154, 
    0.2, 0.238, 0.048, 0.071, 0.111, 0.158, 0.211, 0.241, 
    0.05, 0.077, 0.118, 0.167, 0.214, 0.25, 0.053, 0.083, 
    0.125, 0.176, 0.222, 0.056, 0.091, 0.133, 0.182, 0.227
]

# Pyvis Graph Config
net = Network(select_menu=True, cdn_resources='remote')
net.show_buttons(filter_=['physics'])

''' 
Uncomment this network initialization to remove the select menu & physics menu
This also enforces a default physics option of forceAtlas2Based, which usually appears
better in the screenshotted images made by Playwright.
I wish generating images of the PyVis graph was less like this 😔
'''
# net = Network()
# net.set_options("""{
#     "physics": {
#         "enabled": true,
#         "solver": "forceAtlas2Based",
#         "forceAtlas2Based": {
#             "gravitationalConstant": -200,
#             "centralGravity": 0.15,
#             "springLength": 130,
#             "springConstant": 0.2,
#             "damping": 0.9,
#             "avoidOverlap": 1
#         },
#         "stabilization": {
#             "enabled": true,
#             "iterations": 1000,
#             "updateInterval": 25,
#             "fit": true
#         },
#         "minVelocity": 0.75,
#         "maxVelocity": 30
#     }
# }""")

# Functions -------------------------------------------------------------------------------------------
''' Word Frequency Visualization

Given a threshold size and a size set for the document list to analyze, generates associations based off
levensthein distances between words available in the corpus

'''
def visualizeWordFreqData(threshold: int, doc_lt: dict, docsize_choice: str, spellcheck_lvl: int):
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

    pyvisSaveGraph(f"word_freq_diagram_{threshold}_{docsize_choice}_{spellcheck_lvl}")

def visualizeClusterCompData(distance: float, min_threshold: int, max_threshold: int):
    timer = 0
    initial_ls = pd.read_pickle(f'./pickles/connected_comps_{distance}')
    cluster_ls = []

    # Filter Cluster Comp List by thresholds
    if min_threshold != -1 or max_threshold != -1:
        timer = time.time()
        for ls in tqdm(initial_ls, desc="Compiling cluster list from data: ".ljust(65)):
            if len(ls) >= min_threshold and (max_threshold == -1 or len(ls) <= max_threshold):
                cluster_ls.append(ls)
        print("\tExecution time: ", time.time() - timer, " seconds")
    else:
        cluster_ls = initial_ls

    # Generate Graph
    timer = time.time()
    word_set = nltk_words.words()

    for ls in tqdm(cluster_ls, desc="Generating Graph & Pairing words: ".ljust(65)):
        # Edge case in case there's only one word
        if len(ls) <= 1:
            net.add_node(
                ls[0], 
                size=2,  
                label=f"{ls[0]}",
                group=ls[0]
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
            size=9, 
            label=f"{correct_word}",
            group=correct_word
        )
        
        for word in ls: 
            if word != correct_word:
                net.add_node(
                    word, 
                    size=6, 
                    label=f"{word}",
                    group=correct_word
                )
    
                net.add_edge(
                    word,
                    correct_word,
                    width=0
                )

    print("\tExecution time: ", time.time() - timer, " seconds")

    pyvisSaveGraph(f"cluster_comp_diagram_{distance}_{min_threshold}_{max_threshold}")

def visualizeClusterCompFreqData(distance: float, freq_threshold: int, doc_lt: dict, min_cluster_threshold: int, max_cluster_threshold: int):
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
        if word_freq >= freq_threshold:
            word_freqs[word] = word_freq
    print("\tExecution time: ", time.time() - timer, " seconds")

    # Merge pickled information into one list
    initial_ls = pd.read_pickle(f'./pickles/connected_comps_{distance}')
    full_cluster_ls = []

    # Filter Cluster Comp List by thresholds
    if min_cluster_threshold != -1 or max_cluster_threshold != -1:
        timer = time.time()
        for ls in tqdm(initial_ls, desc="Compiling cluster list from data: ".ljust(65)):
            if len(ls) >= min_cluster_threshold and (max_cluster_threshold == -1 or len(ls) <= max_cluster_threshold):
                full_cluster_ls.append(ls)
        print("\tExecution time: ", time.time() - timer, " seconds")
    else:
        full_cluster_ls = initial_ls

    # Filter by Words with recorded word frequencies
    timer = time.time()
    final_cluster_ls = []
    for ls in tqdm(full_cluster_ls, desc="Culling clusters with low frequencies: ".ljust(65)):
        # Remove words from each list that did not meet the word frequency threshold
        for word in ls[:]: # Iterate through copy of list
            if word not in word_freqs:
                ls.remove(word)
        # If every word met requirements, then yay!
        if len(ls) > 1:
            final_cluster_ls.append(ls)
    print("\tExecution time: ", time.time() - timer, " seconds")

    # Now Perform Clustering Algorithm & Generate Graph
    timer = time.time()
    word_set = nltk_words.words()

    for ls in tqdm(final_cluster_ls, desc="Generating Graph & Pairing words: ".ljust(65)):
        # print("List I'm looking at !! ", ls)
        # Edge case in case there's only one word
        if len(ls) <= 1:
            net.add_node(
                word, 
                size=2,  
                label=f"{word}\n({word_freqs[word] if word in word_freqs else 'BROKEN'})",
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
            label=f"{correct_word}\n({word_freqs[correct_word] if correct_word in word_freqs else 'BROKEN'})",
            group=correct_word
            )
        
        for word in ls: 
            if word != correct_word:
                net.add_node(
                    word, 
                    size=2, 
                    label=f"{word}\n({word_freqs[word] if word in word_freqs else 'BROKEN'})",
                    group=correct_word
                )
    
                net.add_edge(
                    word,
                    correct_word,
                    width=0
                )
    print("\tExecution time: ", time.time() - timer, " seconds")

    pyvisSaveGraph(f"cluster_comp_freq_diagram_{distance}_{freq_threshold}_{min_cluster_threshold}_{max_cluster_threshold}")

def pyvisSaveGraph(name: str):
    html = net.generate_html()
    with open(f"cluster_visualizations/{name}.html", mode='w', encoding='utf-8') as fp:
        fp.write(html)
    print(f"Done! Look for cluster_visualizations/{name}.html")

    # Generate png of graph, comment out line in case you don't want this... this may take a while >.<
    # pyvisGenerateScreenshot(name)

def pyvisGenerateScreenshot(filename: str):
    print(f"Saving Image of Visualization...")
    timer = time.time()

    with sync_playwright() as p:
        for browser_type in [p.firefox]:
            browser = browser_type.launch()
            page = browser.new_page()

            with open(f"cluster_visualizations/{filename}.html", "r") as file:
                file_contents = file.read()
            page.set_content(file_contents, wait_until="load", timeout=10000000000)

            # Custom Javascript function to await the loading screen to finish & the network to become visible
            # print("\tWaiting for Network to load...")
            # page.evaluate('''
            #     () => {
            #         return new Promise((resolve) => {
            #             // Check if the network graph is loaded
            #             const checkGraphLoaded = () => {
            #                 const networkElements = document.querySelectorAll('.vis-network');
            #                 if (networkElements.length > 0) {
            #                     resolve(true);
            #                 } else {
            #                     setTimeout(checkGraphLoaded, 500);
            #                 }
            #             };
            #             checkGraphLoaded();
            #         });
            #     }
            # ''')


            # Additional Timeout after load to let physics organize nodes a bit... hopefully...
            print("\tWaiting for a few seconds...")
            page.wait_for_timeout(30000)

            page.screenshot(path=f'cluster_visualizations/{filename}.png', full_page=True)
            file.close()
            browser.close()

    print(f"\tDone! Look for cluster_visualizations/{filename}.png")
    print("\tExecution time: ", time.time() - timer, " seconds")

def analyzeClusterCompData():
    spell = SpellChecker()

    for dist_val in cluster_distances:
        cluster_ls = pd.read_pickle(f'./pickles/connected_comps_{dist_val}')

        for cluster in tqdm(cluster_ls, desc=f"Processing cluster accuracy at distance of {dist_val}: ".ljust(30)):
            for i in len(cluster):
                cluster[i] = spell.correction(cluster[i])
            
            correctPercent = 0

                

main()