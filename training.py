import os
import random

import file_utils

word_association_training_filename = "res/word_association_training_results.txt"
loc_association_training_filename = "res/loc_association_training_results.txt"
def train_prop_statistics(input_word):
    props_list = []
    total_props = 0
    for entry in os.scandir(input_word):
        print(entry.name)
        with open(entry, 'r') as vmf:
            data = vmf.readlines()
            for line_index in range(len(data)):
                line = data[line_index]
                if line.__contains__("prop_static") or line.__contains__("prop_dynamic") or line.__contains__(
                        "prop_physics"):
                    total_props += 1
                    print(data[line_index], data[line_index + 14],data[line_index + 18])
                    props_list.append(
                        data[line_index + 14].strip().split()[1][1:-1])  # adds props' model names to the list

    print(total_props)
    print(props_list)

    counts = dict()
    for i in props_list:
        counts[i] = counts.get(i, 0) + 1

    prop_probabilities = {}

    items = []
    weights = []
    for item in counts:
        prop_probabilities[item] = counts[item] / total_props # gets the probability
        items.append(item)
        weights.append(prop_probabilities[item])

    print(items)
    print(weights)

    print(random.choices(population=items, weights=weights, k=10)) # shows a random sampling from the distribution

    with open(word_association_training_filename, 'a') as fout:
        fout.write("{\n")
        for i in range(len(items)):
            data = items[i] + ":" + str(weights[i])
            fout.write(data + "\n")
        fout.write(input_word.split('\\')[1] + "\n") # gets the folder name
        fout.write("}\n")


training_folders = [x[0] for x in os.walk("training")]
print(training_folders)

file_utils.clear_file(word_association_training_filename)
for folder_index in range(1, len(training_folders)):
    folder = training_folders[folder_index]
    train_prop_statistics(folder)
