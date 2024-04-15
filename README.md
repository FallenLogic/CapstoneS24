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


Use the GUI for layout and settings, then type a prompt to generate a Source Engine map.
