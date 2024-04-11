nouns = ("chair", "table", "house")
position_words = ('in', 'on', 'by', 'next to')
numbers = {}

# load text descriptions for numbers
with open("numbers.txt", 'r') as numfile:
    for line in numfile:
        line_list = line.split(':')
        numbers[line_list[1].strip()] = line_list[0]


def process_prompt(input_str):
    wordlist = input_str.strip().split()
    # TODO: get list of nouns too in addition to words
    for i in range(len(wordlist) - 1):
        word = wordlist[i]
        next_word = wordlist[i + 1]
        if word in nouns or word[:-1] in nouns:
            if next_word in position_words:
                print("{} {} ".format(word, next_word))
        if word in numbers:
            if next_word in nouns:
                print("we need {} of this prop: {}".format(numbers[wordlist[i]], wordlist[i + 1]))
            # checks for plural or potential typo (s at end)
            if next_word[:-1] in nouns:
                print("we need {} of this prop: {}".format(numbers[wordlist[i]], wordlist[i + 1][:-1]))


process_prompt("twenty chairs on the house")
