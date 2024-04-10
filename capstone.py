import os
from enum import Enum
from functools import partial
import tkinter as tk
from random import randint, uniform
from tkinter import ttk, messagebox
import subprocess
from timeit import default_timer as timer

# my code
import geometry
import file_utils
import minimum_db

MAX_SUPPORTED_SIZE = 32768  # constant

Primitives = Enum('Primitives', ['ARCH', 'BLOCK', 'CYLINDER', 'SPHERE', 'SPIKE', 'TORUS', 'WEDGE'])

preps = ['in', 'on', 'by', 'next to']
articles = ['the']
nouns = ['house', 'room', 'table', 'chair', 'tree', 'bench']

should_write_prefabs = True
should_write_props = True
should_write_primitives = True


class MapSettings:
    # defaults for geometry
    floor_material = "dev/dev_blendmeasure"
    wall_material = "dev/dev_plasterwall001c"


map_settings = MapSettings()

default_padding = 5

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


def load_last_prompt():
    with open('prompt_log.txt', 'r') as fin:
        last_prompt = fin.readlines()[-1]
        if not last_prompt == "":
            input_text.delete(0, 'end')
            input_text.insert(0, last_prompt[:-1])  # [:-1 cuts \n out]


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

    # table_relation = Relation(("table", "desk", "stand"), 0.8, "props_c17\\furnituretable003a.mdl")
    # table_relation.save_relation()

    # table_relation.print_string()

    input_word_dict = {'chair': 'models/props_c17/furniturechair001a.mdl',
                       'table': 'models/props_c17/furnituretable001a.mdl'}
    # TODO: link with relation

    window = tk.Tk()
    window.title("Capstone")
    window.geometry("800x500")

    notebook = ttk.Notebook(window)

    frame = ttk.Frame(notebook)
    dev_settings = ttk.Frame(notebook)

    label = ttk.Label(frame, text="Prompt:")
    label.grid(column=0, row=1, sticky=tk.N, padx=default_padding, pady=default_padding)

    input_text = ttk.Entry(frame, width=26)
    input_text.grid(column=1, row=1, sticky=tk.N, padx=default_padding, pady=default_padding)

    temp_label = ttk.Label(frame, text="Temperature (0-5):")
    temp_label.grid(column=0, row=2, sticky=tk.N, padx=default_padding, pady=default_padding)

    temp_spinbox = ttk.Spinbox(frame, to=5, width=4)
    temp_spinbox.grid(column=1, row=2, sticky=tk.W, padx=default_padding, pady=default_padding)
    temp_spinbox.insert(0,'0')

    grid_var = tk.IntVar()
    grid_size_spinbox = ttk.Spinbox(frame, to=8, width=4, textvariable=grid_var)
    grid_size_spinbox.grid(column=1, row=2, sticky=tk.N, padx=default_padding, pady=default_padding)
    grid_size_spinbox.set(8)

    grid_frame = tk.Frame(frame)
    grid_frame.grid(column=1, row=4, sticky=tk.N)

    theme_var = tk.StringVar()
    theme_combobox = ttk.Combobox(frame, textvariable=theme_var)
    theme_combobox['values'] = ('Urban', 'Natural', 'Sci-Fi')
    theme_combobox['state'] = 'readonly'

    theme_combobox.grid(column=2, row=2, sticky=tk.W, padx=default_padding, pady=default_padding)

    grid_size = 8

    button_grid = []


    def switch_tile_value(i, j):  # using numbers as booleans ("truthy" values in python)
        if true_grid[i][j] == 1:
            true_grid[i][j] = 0
        else:
            true_grid[i][j] = 1


    map_grid_tile_size = MAX_SUPPORTED_SIZE / 8 #TODO: data from spinbox


    def add_grid():

        geo_button['state'] = 'disabled'

        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                command = partial(switch_tile_value, i, j)
                f1 = ImageButton(grid_frame, image1="res/empty2.png", image2="res/handpaintedwall2.png",
                                 command=command)
                f1.grid(column=1 + i, row=4 + j)
                row.append(f1)
            button_grid.append(row)


    geo_button = ttk.Button(frame, text="Do Geometry Painting", command=add_grid)
    geo_button.grid(column=1, row=3, sticky=tk.N, padx=default_padding, pady=default_padding)

    def generate():
        start = timer()
        if theme_combobox.get() == 'Urban':
            map_settings.floor_material = "concrete/concretefloor033k_c17"
            map_settings.wall_material = "building_template/building_template012h"
        if theme_combobox.get() == 'Natural':
            map_settings.floor_material = "nature/blendgrassgravel003a"
            map_settings.wall_material = "nature/blendcliffgrass001a"
        if theme_combobox.get() == 'Sci-Fi':
            map_settings.floor_material = "metal/metalfloor003a"
            map_settings.wall_material = "metal/citadel_metalwall077a"

        prevalidation_temperature = temp_spinbox.get()
        if prevalidation_temperature == '' or not prevalidation_temperature.isdigit() or (
                int(prevalidation_temperature) < 0 or int(prevalidation_temperature) > 5):
            messagebox.showwarning(title="Warning", message="Temperature not set or invalid temperature. Using default")
            temp_spinbox.set(0)
        if input_text.get() == '': # tkinter text input usually handles other edge cases (typing \/, os.open, etc)
            messagebox.showwarning(title="Warning", message="No prompt input or invalid input. Using random.")

            noun_index = randint(0, len(nouns) - 1)
            preps_index = randint(0, len(preps) - 1)
            noun_index_2 = randint(0, len(nouns) - 1)
            rand_prompt = nouns[noun_index] + " " + preps[preps_index] + " " + articles[0] + " " + nouns[noun_index_2]
            input_text.insert(0, string=rand_prompt)
        input_str = input_text.get().lower()

        print(input_str)
        with open("prompt_log.txt", 'a') as promptlog:
            promptlog.write(input_str + "\n")

        temperature_val = int(temp_spinbox.get())

        out_file = "maps/" + input_str + ".vmf"
        file_utils.clear_file(out_file)

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
        #size = 4096
        height = 2
        # default values
        left, right, below, above = 0, 0, 0, 0
        for i in range(grid_size):
            for j in range(grid_size):
                if true_grid[i][j] == 1:
                    if j + 1 < grid_size:
                        right = true_grid[i][j + 1]
                    if i > 0:
                        left = true_grid[i][j - 1]
                    if i + 1 < grid_size:
                        below = true_grid[i + 1][j]
                    if i > 0:
                        above = true_grid[i - 1][j]
                    # checks if on the outside
                    if not (left and right and below and above):
                        height = map_grid_tile_size
                    else:
                        height = 2
                    # TODO: update to match chunk-based generation
                    if height == 2:
                        prop_x = (((i + j * (uniform(0, temperature_val)) / 10) * map_grid_tile_size) - (
                                MAX_SUPPORTED_SIZE / 2) + (map_grid_tile_size / 2))
                        prop_y = (((j + i * (uniform(0, temperature_val)) / 10) * map_grid_tile_size) - (
                                                          MAX_SUPPORTED_SIZE / 2) + (map_grid_tile_size / 2))
                        prop_z = 22 # TODO: fix magic number
                        test_prop = geometry.Prop(prop_x,
                                                  prop_y,
                                                  prop_z, True, False, False,
                                                  prop_name)
                        prop_list.append(test_prop)

                    test_cube = geometry.Primitive("BLOCK", (i * map_grid_tile_size - MAX_SUPPORTED_SIZE / 2),
                                                   (j * map_grid_tile_size - MAX_SUPPORTED_SIZE / 2), 0, map_grid_tile_size, map_grid_tile_size,
                                                   height, i, map_settings.floor_material, map_settings.wall_material)

                    geometry_list.append(test_cube)

        if should_write_primitives:
            for brush in geometry_list:
                brush.save_to_file(out_file)
        if should_write_prefabs:
            file_utils.append_file_to_file("prefabs/big_skybox.vmf", out_file) #TODO: update to scale
            if input_str.__contains__("house"):
                file_utils.append_file_to_file("prefabs/prefab_house_1.vmf",out_file)
        if should_write_props:
            with open(out_file, 'a') as fout:
                fout.write("}")
            for prop in prop_list:
                prop.save_to_file(out_file)
        end = timer()

        overall_time = end-start
        map_settings.ttc = overall_time
        print("Time to completion: " + str(overall_time)) #TODO: integrate into GUI
        calculated_time_label['text'] = str(overall_time) + "s"
    gen_button = ttk.Button(frame, text="Generate", command=generate)
    gen_button.grid(column=2, row=1, sticky=tk.N, padx=default_padding, pady=default_padding)

    llp_button = ttk.Button(frame, text="Load last prompt", command=load_last_prompt)
    llp_button.grid(column=3, row=2, sticky=tk.N, padx=default_padding, pady=default_padding)


    def open_hammer():
        subprocess.Popen(
            r"C:\Program Files (x86)\Steam\steamapps\common\Source SDK Base 2013 Multiplayer\bin\hammerplusplus.exe")


    open_button = ttk.Button(frame, text="Open Hammer", command=open_hammer)
    open_button.grid(column=3, row=1, sticky=tk.N, padx=default_padding, pady=default_padding)

    frame.pack()
    true_grid = []

    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(0)
        true_grid.append(row)

    # TODO: dev insights stuff below here

    gen_time_label = ttk.Label(dev_settings, text="Average generation time for this session: ")
    gen_time_label.grid(column=0, row=0, sticky=tk.N, padx=default_padding, pady=default_padding)

    calculated_time_label = ttk.Label(dev_settings, text="0.0s")
    # TODO: calculated_time should reset on generate try tk.FloatVar()
    calculated_time_label.grid(column=1, row=0, sticky=tk.N, padx=default_padding, pady=default_padding)

    enable_props = ttk.Label(dev_settings, text="Use Props")
    enable_props.grid(column=0, row=1, sticky=tk.W, padx=default_padding, pady=default_padding)

    enable_props_button = ttk.Checkbutton(dev_settings)
    enable_props_button.grid(column=1, row=1, sticky=tk.W, padx=default_padding, pady=default_padding)
    # button

    enable_prims = ttk.Label(dev_settings, text="Use Primitives")
    enable_prims.grid(column=0, row=2, sticky=tk.W, padx=default_padding, pady=default_padding)

    enable_prims_button = ttk.Checkbutton(dev_settings)
    enable_prims_button.grid(column=1, row=2, sticky=tk.W, padx=default_padding, pady=default_padding)
    # button

    enable_prefabs = ttk.Label(dev_settings, text="Use Prefabs")
    enable_prefabs.grid(column=0, row=3, sticky=tk.W, padx=default_padding, pady=default_padding)

    enable_prefabs_button = ttk.Checkbutton(dev_settings)
    enable_prefabs_button.grid(column=1, row=3, sticky=tk.W, padx=default_padding, pady=default_padding)
    # button

    notebook.add(frame, text="Prompt & General Settings")
    notebook.add(dev_settings, text="Developer Insights/Settings")
    notebook.pack(padx=default_padding, pady=default_padding, expand=True, fill='both')
    window.mainloop()
