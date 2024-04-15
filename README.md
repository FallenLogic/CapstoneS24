# CapstoneS24
My Senior Capstone Project.

## Main GUI:
Prompt: Type here what you want in the map's empty space (statistics model must be trained on it first, more on that later.)
Grid Size: The size of the X and Y axis of the top-down grid. 
Theme: What kind of textures should the map use? Sci-Fi, Urban, Natural or Default?
Temperature: The amount of randomness in the output map.

The grid is a top-down view of your map's layout.
To edit the map layout, click on each square. This will adjust its height and whether a primitive is in the selected space or props are in the selected space.
A purple square is entirely empty, green is a space for props and prefabs, and otherwise is a linear multiplier for the height. (4 = 4x the height of 1, for example).

GENERATE MAP: Actually write the output file. This calls functions that process the prompt and load associated prop types, locations, and conditional probabilities based on the input words.

Open Hammer: Hammer is a more advanced viewer and editor for Source Engine maps. This opens it and allows you to look around your new map in three dimensions.

Load last prompt: This does what it says. Useful if you close the program and want to load the last thing you entered.

## Developer Insights

Here, you can see how long it's taking to output the maps you've created this session (on average).
You can also choose to include or exclude props, primitives, and prefabs.
Finally, the most important button: "TRAIN MODEL"
This button tells the program to model the worlds it sees by ingesting the maps in the training subfolders.

## Files/Folders

To create new data that you want to associate with a term, create a folder named the same as the term under the "training" folder. 
Place your VMF files in that subdirectory.
When you train the model again, statistics for each term will be updated.
The current demo build has a folder with "city", "kitchen", "room", and "tree" in it.

The maps folder is where your generated maps will be output.
The prefabs folder stores geometry that isn't for training and isn't a full map - for instance, the two sizes of skybox.

## Viewing maps

To view your maps you will need Hammer++ installed at "C:\Program Files (x86)\Steam\steamapps\common\Source SDK Base 2013 Multiplayer\bin\hammerplusplus.exe"
