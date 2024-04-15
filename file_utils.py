def clear_file(out_file):
    with open(out_file, 'w') as fout:
        fout.write('\n')
        fout.close()


def write_prefab_to_file(in_file, out_file):
    data = []
    with open(in_file, 'r') as fin:
        for line in fin:
            data.append(line)
            # if line.__contains__(r'"v"'):
            #     #print(line)
    with open(out_file, 'a') as fout:
        fout.write('\n')
        for line in data:
            fout.write(line)


def write_prefab_to_file_with_loc(in_file, out_file, x, y, z):
    data = []
    with open(in_file, 'r') as fin:
        for line in fin:
            if line.__contains__(r'"plane"'):
                plane_data = line.split(' "')
                print(plane_data[1])

                verts = plane_data[1].split("(")
                corner1 = verts[1].strip()[:-1]
                corner2 = verts[2].strip()[:-1]
                corner3 = verts[3].strip()[:-2]

                print(corner1, corner2, corner3)

                points_one = corner1.split(' ')
                points_two = corner2.split(' ')
                points_three = corner3.split(' ')

                x1 = int(points_one[0]) + int(x)
                y1 = int(points_one[1]) + int(y)
                z1 = int(points_one[2]) + int(z)

                x2 = int(points_two[0]) + int(x)
                y2 = int(points_two[1]) + int(y)
                z2 = int(points_two[2]) + int(z)

                x3 = int(points_three[0]) + int(x)
                y3 = int(points_three[1]) + int(y)
                z3 = int(points_three[2]) + int(z)

                out_line = '\t\t\t"plane" "({} {} {}) ({} {} {}) ({} {} {})"\n'.format(x1, y1, z1, x2, y2, z2, x3, y3, z3)
                data.append(out_line)
            else:
                if line.__contains__(r'"v"'):
                    face_data = line.split(' "')
                    print(face_data)
                    vert_data = face_data[1].split(' ')
                    print(vert_data)

                    new_loc_x = int(vert_data[0].strip()) + int(x)
                    new_loc_y = int(vert_data[1].strip()) + int(y)
                    new_loc_z = int(vert_data[2].strip()[:-1]) + int(z)

                    data.append('\t\t\t\t"v" "{} {} {}"\n'.format(new_loc_x, new_loc_y, new_loc_z))
                else:
                    data.append(line)

    with open(out_file, 'a') as fout:
        fout.write('\n')
        for line in data:
            print(line)
            fout.write(line)
