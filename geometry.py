import math
import numpy as np


class Primitive:
    def __init__(self, prim_type, loc_x, loc_y, loc_z, size_x, size_y, size_z, id, floor_texture, wall_texture):
        self.prim_type = prim_type
        self.x = loc_x
        self.y = loc_y
        self.z = loc_z
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.id = id
        self.floor_texture = floor_texture
        self.wall_texture = wall_texture

    def save_to_file(self, out_file):
        # TODO: implement writing to a map file
        with open(out_file, 'a') as fout:
            fout.write("solid\n")
            fout.write("{\n")
            fout.write(r'"id" ' + '"{}"\n'.format(self.id))
            sx = self.size_x
            sy = self.size_y
            sz = self.size_z
            for k in range(6):
                face_id = k + 1
                if face_id == 1:
                    texture = self.floor_texture
                else:
                    texture = self.wall_texture
                fout.write("side\n")
                fout.write("{\n")
                fout.write(r'"id"' + ' "{}"\n'.format(face_id))
                # winding order matters, hardcoded
                if face_id == 1:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y + sy, self.z + sz,
                               self.x + sx, self.y + sy, self.z + sz,
                               self.x + sx, self.y, self.z + sz))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 -1 0 0] 0.25"' + "\n")

                if face_id == 2:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y, self.z,
                               self.x + sx, self.y, self.z,
                               self.x + sx, self.y + sy, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")

                    fout.write(r'"vaxis" "[0 -1 0 0] 0.25"' + "\n")
                if face_id == 3:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y + sy, self.z + sz,
                               self.x, self.y, self.z + sz,
                               self.x, self.y, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[0 1 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")

                if face_id == 4:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + sx, self.y + sy, self.z,
                               self.x + sx, self.y, self.z,
                               self.x + sx, self.y, self.z + sz))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[0 1 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")
                if face_id == 5:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + sx, self.y + sy, self.z + sz,
                               self.x, self.y + sy, self.z + sz,
                               self.x, self.y + sy, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")
                if face_id == 6:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + sx, self.y, self.z,
                               self.x, self.y, self.z,
                               self.x, self.y, self.z + sz))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")

                fout.write(r'"rotation" "0"' + "\n")
                fout.write(r'"lightmapscale" "16"' + "\n")
                fout.write(r'"smoothing_groups" "0"' + "\n")
                fout.write("}\n")
            fout.write("}\n")
            fout.write("editor\n{\n")
            fout.write(r'"color" "0 228 161"' + "\n")
            fout.write(r'"visgroupshown" "1"' + "\n")
            fout.write(r'"visgroupautoshown" "1"' + "\n")
            fout.write('}\n')
            fout.close()


class Prop:
    def __init__(self, loc_x, loc_y, loc_z, is_static, is_dynamic, is_physics, name):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z
        self.is_static = is_static
        self.is_dynamic = is_dynamic
        self.is_physics = is_physics
        self.name = name

    def save_to_file(self, out_file):
        with open(out_file, 'a') as fout:
            fout.write("entity\n")
            fout.write("{\n")
            fout.write("\t" + r'"id" "' + str(int(math.floor(self.loc_x))) + '"' + "\n")
            if self.is_static:
                fout.write("\t" + r'"classname" "prop_static"' + "\n")
            if self.is_physics:
                fout.write("\t" + r'"classname" "prop_physics"' + "\n")
            if self.is_dynamic:
                fout.write("\t" + r'"classname" "prop_dynamic"' + "\n")
            rot = np.random.choice([0,90,180])
            boilerplate_list = [r'"angles" "0 {} 0"'.format(rot), r'"disableselfshadowing" "0"', r'"disableshadows" "0"',
                                r'"disablevertexlighting" "0"',
                                r'"fademaxdist" "0"', r'"fademindist" "-1"', r'"fadescale" "1"',
                                r'"generatelightmaps" "0"', r'"ignorenormals" "0"',
                                r'"lightmapresolutionx" "32"', r'"lightmapresolutiony" "32"', r'"maxdxlevel" "0"',
                                r'"mindxlevel" "0"']
            for bp in boilerplate_list:
                fout.write("\t" + bp + "\n")
            fout.write("\t" + r'"model" "' + self.name + "\"\n")

            settings_list = [r'"screenspacefade" "0"', r'"skin" "0"', r'"solid" "6"']
            for setting in settings_list:
                fout.write("\t" + setting + "\n")
            fout.write("\t" + r'"origin" ')
            fout.write("\"{} {} {}\"\n".format(self.loc_x, self.loc_y, self.loc_z))

            fout.write('\teditor\n')
            fout.write('\t{\n')

            boilerplate_ending_list = [r'"color" "255 255 0"', r'"visgroupshown" "1"',
                                       r'"visgroupautoshown" "1"', r'"logicalpos" "[0 0]"']
            for bp in boilerplate_ending_list:
                fout.write("\t\t" + bp + "\n")
            fout.write("\t}\n")
            fout.write("}\n")
            fout.close()
