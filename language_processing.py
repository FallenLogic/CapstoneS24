import training
import os

nouns = [x[0].split('\\')[-1] for x in os.walk("training")]  # TODO see if it works for Capstone
print(nouns)
position_words = ('in', 'on', 'by', 'next to')
numbers = {}

# def load_props(filename):
#     with open(filename) as fin:
#         for line in fin:
#             if line.startswith("("):
#                 overall_data = []
#                 words = set(line[1:-2].split(","))
#             else:
#                 prop_data = line.split(":")
#                 prop_name = prop_data[0]
#                 conditional_probability = float(prop_data[-1])
#                 data_set = [prop_name, conditional_probability]
#                 overall_data.append(data_set)
#                 print(overall_data)


# load text descriptions for numbers
with open("numbers.txt", 'r') as numfile:
    for line in numfile:
        line_list = line.split(':')
        numbers[line_list[1].strip()] = line_list[0]


def process_prompt(input_str, prop_x, prop_y, map_input):
    retrieved_props = []
    input_word_list = input_str.strip().split()
    print(input_word_list)
    list_of_words = []

    word1 = input_word_list[0]
    if word1 in nouns:
        list_of_words.append(word1)
    if word1[:-1] in nouns:
        list_of_words.append(word1)
        
    for i in range(0, len(input_word_list)-1):

        word = input_word_list[i]
        next_word = input_word_list[i+1]
        print("WORDS:", word, next_word)
        if word in nouns:
            list_of_words.append(word)
        if word[:-1] in nouns:
            list_of_words.append(word)
        if word in numbers:
            if next_word in nouns:
                for j in range(int(numbers[word])):
                    list_of_words.append(word)
            if next_word[:-1] in nouns:
                for j in range(int(numbers[word])):
                    list_of_words.append(next_word[:-1])

    for item in list_of_words:
        temp_list = training.load_props(item, prop_x, prop_y, map_input)
        for item2 in temp_list:
            retrieved_props.append(item2)

    print("WORDLIST:", list_of_words)

    # TODO: get list of nouns too in addition to words
    # for i in range(len(wordlist) - 1):
    #     word = wordlist[i]
    #     next_word = wordlist[i + 1]
    #     if word in numbers:
    #         if next_word in nouns or next_word[:-1] in nouns:  # checks for plural or potential typo (s at end)
    #             print("we need {} of this object: {}".format(numbers[wordlist[i]], wordlist[i + 1]))
    #             for j in range(int(numbers[word])):
    #                 return_list = training.load_props(next_word[:-1], prop_x, prop_y, map_input)
    #                 for prop in return_list:
    #                     retrieved_props.append(prop)
    #     if word in nouns or word[:-1] in nouns:  # checks for plural
    #         return_list = training.load_props(word[:-1], prop_x, prop_y, map_input)
    #         for prop in return_list:
    #             retrieved_props.append(prop)
    #         if next_word in position_words:
    #             print("{} {} ".format(word, next_word))
    # TODO: position checks

    return retrieved_props
