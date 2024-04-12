import os
import random

import file_utils

word_association_training_filename = "res/word_association_training_results.txt"
loc_association_training_filename = "res/loc_association_training_results.txt"


def train_prop_statistics(input_word):
    props_list = []
    # prop_locations_list = []

    prop_locations_dict = {}

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
                    print(data[line_index], data[line_index + 14], data[line_index + 18])
                    props_list.append(
                        data[line_index + 14].strip().split()[1][1:-1])  # adds props' model names to the list
                    prop_locations_dict[data[line_index + 14].strip().split()[1][1:-1]] = \
                    data[line_index + 18].strip().split('"')[3]
    # print(total_props)
    print(props_list)
    print(prop_locations_dict)

    counts = dict()
    for i in props_list:
        counts[i] = counts.get(i, 0) + 1

    prop_probabilities = {}

    items = []
    weights = []
    for item in counts:
        prop_probabilities[item] = counts[item] / total_props  # gets the probability
        items.append(item)
        weights.append(prop_probabilities[item])

    # TODO: allow duplicates
    loc_counts = dict()
    for i in prop_locations_dict:
        loc_counts[i] = loc_counts.get(i, 0) + 1

    loc_items = []
    loc_weights = []
    loc_prop_probabilities = {}
    for loc_item in loc_counts:
        loc_prop_probabilities[loc_item] = loc_counts[loc_item] / total_props
        loc_items.append(loc_item)
        loc_weights.append(loc_prop_probabilities[loc_item])

    print(items)
    # print(weights)

    print(loc_items)
    # print(loc_weights)

    print(random.choices(population=items, weights=weights, k=10))  # shows a random sampling from the distribution

    with open(word_association_training_filename, 'a') as fout:
        fout.write("{\n")
        for i in range(len(items)):
            data = items[i] + ":" + str(weights[i])
            fout.write(data + "\n")
        fout.write(input_word.split('\\')[1] + "\n")  # gets the folder name
        fout.write("}\n")

    with open(loc_association_training_filename, 'a') as fout2:
        fout2.write("{\n")
        print("len1", len(items))
        print("len2", len(loc_items))

        for i in range(len(loc_items)):
            data = loc_items[i] + ":" + items[i] + ":" + str(loc_weights[i])  # TODO: store associated name
            fout2.write(data + "\n")
        fout2.write(input_word.split('\\')[1] + "\n")  # gets the folder name
        fout2.write("}\n")


# iterate steps from stackoverflow
training_folders = [x[0] for x in os.walk("training")]

file_utils.clear_file(word_association_training_filename)
for folder_index in range(1, len(training_folders)):
    folder = training_folders[folder_index]
    train_prop_statistics(folder)
