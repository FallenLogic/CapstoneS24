import math
import os
import random

import file_utils

word_association_training_filename = "res/word_association_training_results.txt"
loc_association_training_filename = "res/loc_association_training_results.txt"


def train_prop_statistics(input_word):
    props_list = []

    prop_locations_dict = {}

    total_props = 0
    total_maps = 0
    for entry in os.scandir(input_word):
        total_maps += 1
        print(entry.name)
        with open(entry, 'r') as vmf:
            data = vmf.readlines()
            for line_index in range(len(data)):
                line = data[line_index]
                if line.__contains__("prop_static") or line.__contains__("prop_dynamic") or line.__contains__(
                        "prop_physics"):
                    total_props += 1
                    prop_name = data[line_index + 14].strip().split()[1][1:-1]
                    #print(data[line_index], data[line_index + 14], data[line_index + 18])
                    props_list.append(prop_name)  # adds props' model names to the list
                    # for prop in props_list:
                    #     prop_locations_dict[prop] = []  # creates an empty list for multivalued results
                    prop_locations_dict[prop_name] = []
            for line_index in range(len(data)):
                line = data[line_index]
                if line.__contains__("prop_static") or line.__contains__("prop_dynamic") or line.__contains__(
                        "prop_physics"):
                    prop_locations_dict[prop_name].append(data[line_index + 18].strip().split('" "')[1][:-1])
    # print(total_props)
    #print(props_list)
    #print(prop_locations_dict)

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

    #print(items)
    # print(weights)
    #
    # for prop in prop_locations_dict:
    #     print(prop)
    #     print(prop_locations_dict[prop])

    print(random.choices(population=items, weights=weights, k=10))  # shows a random sampling from the distribution

    prop_avg_count = math.floor(total_props / total_maps)

    with open(word_association_training_filename, 'a') as fout:
        fout.write("{\n")
        for i in range(len(items)):
            data = items[i] + ":" + str(weights[i])
            fout.write(data + "\n")
        fout.write(input_word.split('\\')[1] + ":" + str(prop_avg_count) + "\n")  # gets the folder name
        fout.write("}\n")

    with open(loc_association_training_filename, 'a') as fout2:
        fout2.write("{\n")
        for prop in prop_locations_dict:
            fout2.write(prop + ":")
            for i in range(len(prop_locations_dict[prop])):
                if i == 0:
                    fout2.write(prop_locations_dict[prop][i])
                else:
                    fout2.write("," + prop_locations_dict[prop][i])
            fout2.write("\n")
        fout2.write(input_word.split('\\')[1] + "\n")  # gets the folder name
        fout2.write("}\n")


def load_props(input_word):
    final_prop_list = []
    with open(word_association_training_filename, 'r') as fin:
        data = fin.readlines()
        for i in range(len(data)):
            line = data[i]
            if line.startswith("{"):
                props_list = []
                probs_list = []
                continue
            if line.startswith("}"):
                word = data[i - 1].split(":")[0].strip()
                print("WORD:", word)
                if word == input_word:
                    print("CORRECT DATA LOADED")
                    print("WEIGHTED CHOICES:",random.choices(population=props_list[:-1], weights=probs_list[:-1], k=int(probs_list[-1])))
                    print(props_list[:-1])
                    print(probs_list[:-1])
                    break
                else:
                    continue
            if line.__contains__(":"):
                word_and_prob = line.split(":")
                #print(word_and_prob)
                props_list.append(word_and_prob[0])
                probs_list.append(float(word_and_prob[-1].strip()))
                # props_list.pop()
                # probs_list.pop()

# iterate steps from stackoverflow
training_folders = [x[0] for x in os.walk("training")]

file_utils.clear_file(loc_association_training_filename)
file_utils.clear_file(word_association_training_filename)

for folder_index in range(1, len(training_folders)):
    folder = training_folders[folder_index]
    train_prop_statistics(folder)

load_props("kitchen")
