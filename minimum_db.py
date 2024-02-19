class Relation:
    def __init__(self, wordset, probability, prop):
        self.wordset = wordset
        self.probability = probability
        self.prop = prop

    def print_string(self):
        print(self.wordset, self.probability, self.prop)

    def save_relation(self):
        with open("prop_sample_data.txt","a") as fout:
            fout.write("(")
            for word in self.wordset:
                fout.write(word + ",")
            fout.write(")")

