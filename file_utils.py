def clear_file(out_file):
    with open(out_file, 'w') as fout:
        fout.write('\n')
        fout.close()


def write_prefab_to_file(in_file, out_file):
    data = []
    with open(in_file, 'r') as fin:
        for line in fin:
            data.append(line)

    with open(out_file, 'a') as fout:
        fout.write('\n')
        for line in data:
            fout.write(line)
