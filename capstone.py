import numpy

def load_props(filename):
    with open(filename) as fin:
        for line in fin:
            if line.startswith("("):
                overall_data = []
                words = set(line[1:-2].split(","))
            else:
                prop_data = line.split(":")
                prop_name = prop_data[0]
                conditional_probability = float(prop_data[-1])
                data_set = [prop_name, conditional_probability]
                overall_data.append(data_set)
                print(overall_data)


if __name__ == "__main__":
    load_props("prop_sample_data.txt")
