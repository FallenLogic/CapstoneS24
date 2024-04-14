import training
import os

nouns = [x[0].split('\\')[-1] for x in os.walk("training")] #TODO see if it works for Capstone
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
    wordlist = input_str.strip().split()
    print(wordlist)
    # TODO: get list of nouns too in addition to words
    for i in range(len(wordlist) - 1):
        word = wordlist[i]
        next_word = wordlist[i + 1]
        if word in nouns or word[:-1] in nouns:
            if next_word in position_words:
                print("{} {} ".format(word, next_word))
                #TODO: position checks
        if word in numbers:
            if next_word in nouns or next_word[:-1] in nouns: # checks for plural or potential typo (s at end)
                print("we need {} of this prop: {}".format(numbers[wordlist[i]], wordlist[i + 1]))
                for j in range(int(numbers[word])):
                    return_list = training.load_props(next_word[:-1], prop_x, prop_y, map_input)
                    for prop in return_list:
                        retrieved_props.append(prop)

    return retrieved_props
