import os
from enum import Enum
from functools import partial
import tkinter as tk
from random import randint, uniform
from tkinter import ttk, messagebox
import subprocess
import numpy

from minimum_db import Relation

MAX_SUPPORTED_SIZE = 32768  # constant

Primitives = Enum('Primitives', ['ARCH', 'BLOCK', 'CYLINDER', 'SPHERE', 'SPIKE', 'TORUS', 'WEDGE'])

preps = ['in', 'on', 'by', 'next to']
articles = ['the']
nouns = ['house', 'room', 'table', 'chair', 'tree', 'bench']


def clear_file(out_file):
    with open(out_file, 'w') as fout:
        fout.write('\n')
        fout.close()


class MapSettings:
    floor_material = "dev/dev_blendmeasure"
    wall_material = "dev/dev_plasterwall001c"


class ImageButton(ttk.Button):
    # Adapted from: https://stackoverflow.com/questions/69167947/how-to-change-tkinter-button-image-on-click
    def __init__(self, master, image1, image2, *args, **kwargs):
        self.unclickedImage = tk.PhotoImage(file=image1)
        self.clickedImage = tk.PhotoImage(file=image2)
        super().__init__(master, *args, image=self.unclickedImage, **kwargs)
        self.toggleState = 1
        self.bind("<Button-1>", self.click_function)

    def click_function(self, event=None):
        if self.cget("state") != "disabled":  # Ignore click if button is disabled
            self.toggleState *= -1
            if self.toggleState == -1:
                self.config(image=self.clickedImage)
            else:
                self.config(image=self.unclickedImage)


def add_grid(parent, size):
    overall_grid = []
    for i in range(size):
        row = []
        overall_grid.append(row)
        for j in range(size):
            row.append("e")
    tile_grid = []
    for k in range(size):
        for j in range(size):
            tile = tk.Button(parent, borderwidth=0)
            tile.grid(column=k + 1, row=j + 4, sticky=tk.N, padx=0, pady=0)
            tile_grid.append(tile)
            print(tile)
    print(tile_grid)
    print(overall_grid)


class OutFile:
    out_file = "map.vmf"


class Primitive:
    def __init__(self, prim_type, loc_x, loc_y, loc_z, size_x, size_y, size_z, id):
        self.prim_type = prim_type
        self.x = loc_x
        self.y = loc_y
        self.z = loc_z
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.id = id

    def save_to_file(self, out_file):
        # TODO: implement writing to a map file
        with open(out_file, 'a') as fout:
            fout.write("solid\n")
            fout.write("{\n")
            fout.write(r'"id" ' + '"{}"\n'.format(self.id))
            s = self.size_x
            texture = "tools/toolsnodraw"
            for k in range(6):
                face_id = k + 1
                if face_id == (1 or 2 or 3 or 4):
                    texture = MapSettings.wall_material
                if face_id == 5:
                    texture = MapSettings.floor_material
                fout.write("side\n")
                fout.write("{\n")
                fout.write(r'"id"' + ' "{}"\n'.format(face_id))
                # winding order matters, hardcoded
                if face_id == 1:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y + s, self.z + s,
                               self.x + s, self.y + s, self.z + s,
                               self.x + s, self.y, self.z + s))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")

                if face_id == 2:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y, self.z,
                               self.x + s, self.y, self.z,
                               self.x + s, self.y + s, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")

                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")

                # TODO: check y-axis
                if face_id == 3:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x, self.y + s, self.z + s,
                               self.x, self.y, self.z + s,
                               self.x, self.y, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[0 1 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")

                if face_id == 4:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + s, self.y + s, self.z,
                               self.x + s, self.y, self.z,
                               self.x + s, self.y, self.z + s))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[0 1 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")
                if face_id == 5:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + s, self.y + s, self.z + s,
                               self.x, self.y + s, self.z + s,
                               self.x, self.y + s, self.z))
                    fout.write(r'"material" ' + '"{}"'.format(texture) + "\n")
                    fout.write(r'"uaxis" "[1 0 0 0] 0.25"' + "\n")
                    fout.write(r'"vaxis" "[0 0 -1 0] 0.25"' + "\n")
                if face_id == 6:
                    fout.write(
                        r'"plane"' + ' "({} {} {}) ({} {} {}) ({} {} {})"\n'.
                        format(self.x + s, self.y, self.z,
                               self.x, self.y, self.z,
                               self.x, self.y, self.z + s))
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
        # Change to append
        with open(out_file, 'a') as fout:
            fout.write("entity\n")
            fout.write("{\n")
            fout.write("\t" + r'"id" "2"' + "\n")
            if self.is_static:
                fout.write("\t" + r'"classname" "prop_static"' + "\n")
            if self.is_physics:
                fout.write("\t" + r'"classname" "prop_physics"' + "\n")
            if self.is_dynamic:
                fout.write("\t" + r'"classname" "prop_dynamic"' + "\n")
            boilerplate_list = [r'"angles" "0 0 0"', r'"disableselfshadowing" "0"', r'"disableshadows" "0"',
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
    prop_path = "prop_sample_data.txt"

    load_props(prop_path)

    table_relation = Relation(("table", "desk", "stand"), 0.8, "props_c17\\furnituretable003a.mdl")
    table_relation.save_relation()

    table_relation.print_string()

    input_word_dict = {'chair': 'models/props_c17/furniturechair001a.mdl',
                       'table': 'models/props_c17/furnituretable001a.mdl'}
    # TODO: link with relation

    window = tk.Tk()
    window.title("Capstone")
    window.geometry("800x500")

    frame = ttk.Frame(window)
    frame.columnconfigure(0, weight=1)

    label = ttk.Label(frame, text="Prompt:")
    label.grid(column=0, row=1, sticky=tk.N, padx=5, pady=5)

    input_text = ttk.Entry(frame, width=26)
    input_text.grid(column=1, row=1, sticky=tk.N, padx=5, pady=5)

    temp_label = ttk.Label(frame, text="Temperature:")
    temp_label.grid(column=0, row=2, sticky=tk.N, padx=5, pady=5)

    temp_spinbox = ttk.Spinbox(frame, to=5, width=4)
    temp_spinbox.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

    grid_size_spinbox = ttk.Spinbox(frame, to=8, width=4)
    grid_size_spinbox.grid(column=1, row=2, sticky=tk.N, padx=5, pady=5)

    geo_label = ttk.Label(frame, text="Geometry Painting:")
    geo_label.grid(column=1, row=3, sticky=tk.N, padx=5, pady=5)

    grid_frame = tk.Frame(frame)
    grid_frame.grid(column=1, row=4, sticky=tk.N)

    theme_var = tk.StringVar()
    theme_combobox = ttk.Combobox(frame, textvariable=theme_var)
    theme_combobox['values'] = ('Urban', 'Natural', 'Sci-Fi')
    theme_combobox['state'] = 'readonly'

    theme_combobox.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5)

    grid_size = 8

    map_grid_tile_size = MAX_SUPPORTED_SIZE / grid_size

    button_grid = []


    def switch_tile_value(i, j):  # using numbers as booleans ("truthy" values in python)
        if true_grid[i][j] == 1:
            true_grid[i][j] = 0
        else:
            true_grid[i][j] = 1


    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            command = partial(switch_tile_value, i, j)
            f1 = ImageButton(grid_frame, image1="res/handpaintedwall1.png", image2="res/handpaintedwall2.png",
                             command=command)
            f1.grid(column=1 + i, row=4 + j)
            row.append(f1)
        button_grid.append(row)


    def generate():
        if theme_combobox.get() == 'Urban':
            MapSettings.floor_material = "concrete/concretefloor033k_c17"
            MapSettings.wall_material = "building_template/building_template012h"

        if temp_spinbox.get() == '':
            messagebox.showwarning(title="Warning", message="Temperature not set. Using default")
            temp_spinbox.set(0)
        if input_text.get() == '':
            messagebox.showwarning(title="Warning", message="No prompt input. Using random")

            noun_index = randint(0, len(nouns) - 1)
            preps_index = randint(0, len(preps) - 1)
            noun_index_2 = randint(0, len(nouns) - 1)
            rand_prompt = nouns[noun_index] + " " + preps[preps_index] + " " + articles[0] + " " + nouns[noun_index_2]
            input_text.insert(0, string=rand_prompt)
        input_str = input_text.get().lower()
        print(input_str)
        with open("prompt_log.txt", 'a') as promptlog:
            promptlog.write(input_str + "\n")

        temp = int(temp_spinbox.get())

        out_file = "maps/" + input_str + ".vmf"
        clear_file(out_file)

        with open(out_file, 'a') as fout:
            fout.write("world\n{\n")
            fout.close()

        # TODO: generalize this (for word in db, if input_str contains word: prop_name_prob? )
        if input_str.__contains__("table"):
            prop_name = input_word_dict["table"]
        else:
            prop_name = input_word_dict["chair"]

        prop_list = []
        geometry_list = []
        for i in range(grid_size):
            for j in range(grid_size):
                if true_grid[i][j] == 1:
                    # TODO: update to match chunk-based generation
                    test_prop = Prop((((i + j * (uniform(0, temp)) / 10) * map_grid_tile_size) - (
                            MAX_SUPPORTED_SIZE / 2) + (map_grid_tile_size / 2)),
                                     (((j + i * (uniform(0, temp)) / 10) * map_grid_tile_size) - (
                                             MAX_SUPPORTED_SIZE / 2) + (map_grid_tile_size / 2)),
                                     randint(0, 10 * temp), True, False, False,
                                     prop_name)
                    size = 4096
                    test_cube = Primitive("BLOCK", (i * map_grid_tile_size - MAX_SUPPORTED_SIZE / 2), (j * map_grid_tile_size - MAX_SUPPORTED_SIZE / 2), 0, size, size, 1, i)
                    test_cube.save_to_file(out_file)

                    geometry_list.append(test_cube)
                    prop_list.append(test_prop)

        for prop in prop_list:
            prop.save_to_file(out_file)

        with open(out_file, 'a') as fout:
            fout.write("}")


    gen_button = ttk.Button(frame, text="Generate", command=generate)
    gen_button.grid(column=2, row=1, sticky=tk.N, padx=5, pady=5)


    def open_hammer():
        subprocess.run(
            r"C:\Program Files (x86)\Steam\steamapps\common\Source SDK Base 2013 Multiplayer\bin\hammerplusplus.exe")


    open_button = ttk.Button(frame, text="Open Hammer", command=open_hammer)
    open_button.grid(column=3, row=1, sticky=tk.N, padx=5, pady=5)

    frame.pack()
    true_grid = []

    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(0)
        true_grid.append(row)

    window.mainloop()
