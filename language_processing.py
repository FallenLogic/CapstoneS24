import file_utils
import training
import os

nouns = [x[0].split('\\')[-1] for x in os.walk("training")]  # separate to get folders instead of filenames
numbers = {}


# Adapted from https://stackoverflow.com/questions/8625991/use-python-os-walk-to-identify-a-list-of-files
def file_list(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if filename.endswith('.vmf'):
                matches.append(filename)
    return matches


prefabs = file_list("prefabs")
# load text descriptions for numbers
with open("numbers.txt", 'r') as numfile:
    for line in numfile:
        line_list = line.split(':')
        numbers[line_list[1].strip()] = line_list[0]


def process_prompt_for_prefabs(input_str, pre_x, pre_y, out_file):
    retrieved_prefabs = []
    input_word_list = input_str.strip().split()
    list_of_prefabs = []
    sel_cnt = 0
    for fname in prefabs:
        if sel_cnt == 0:
            word1 = input_word_list[0]
            if fname.__contains__(word1):
                list_of_prefabs.append(fname)
            if fname.__contains__(word1[:-1]):
                list_of_prefabs.append(fname)
            for i in range(0, len(input_word_list) - 1):
                word = input_word_list[i]
                next_word = input_word_list[i + 1]
                if fname.__contains__(word):
                    list_of_prefabs.append(fname)
                if fname.__contains__(word1[:-1]):
                    list_of_prefabs.append(fname)
                if fname.__contains__(next_word):
                    list_of_prefabs.append(fname)
                if fname.__contains__(next_word[:-1]):
                    list_of_prefabs.append(fname)

    for item in list_of_prefabs:
        retrieved_prefabs.append(item)

    print("WORDLIST:", list_of_prefabs)

    for item in retrieved_prefabs:
        file_utils.write_prefab_to_file_with_loc("prefabs/" + item, out_file, pre_x, pre_y, 0)

def process_prompt(input_str, prop_x, prop_y):
    retrieved_props = []
    input_word_list = input_str.strip().split()
    list_of_props = []

    word1 = input_word_list[0]
    if word1 in nouns:
        list_of_props.append(word1)
    if word1[:-1] in nouns:
        list_of_props.append(word1)

    if word1 in prefabs:
        list_of_props.append(word1)
    if word1[:-1] in nouns:
        list_of_props.append(word1)

    for i in range(0, len(input_word_list) - 1):

        word = input_word_list[i]
        next_word = input_word_list[i + 1]
        if word in nouns:
            list_of_props.append(word)
        if word[:-1] in nouns:
            list_of_props.append(word)
        if word in numbers:
            if next_word in nouns:
                for j in range(int(numbers[word])):
                    list_of_props.append(word)
            if next_word[:-1] in nouns:
                for j in range(int(numbers[word])):
                    list_of_props.append(next_word[:-1])

    for item in list_of_props:
        temp_list = training.load_props(item, prop_x, prop_y)
        for item2 in temp_list:
            retrieved_props.append(item2)

    print("WORDLIST:", list_of_props)

    return retrieved_props
