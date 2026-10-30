import os

interaction_folder = "C:\\Users\\conso\\OneDrive\\Documents\\GitHub\\robot-barriers\\data\\interactions"
programs_folder = "C:\\Users\\conso\\OneDrive\\Documents\\GitHub\\robot-barriers\\data\\interactions"
interaction_subfolders = [os.path.basename(str(folder.path)).replace("P", "p")  for folder in os.scandir(interaction_folder) if folder.is_dir()]
program_subfolders = [os.path.basename(str(folder.path)).replace("P", "p")  for folder in os.scandir(programs_folder) if folder.is_dir()]

ids_list = [
    "p04101103",
    "p04101428",
    "p04101549",
    "p04111055",
    "p04111301",
    "p04111434",
    "p04111617",
    "p04121334",
    "p04121200",
    "p04121302",
    "p04121421",
    "p04121600",
    "p04151704",
    "p04151833",
    "p04152005",
    "p04161322",
    "p04161834",
    "p04171512",
    "p04171840",
    "p04181446",
    "p04181705",
    "p04191709",
    "p04191839",
    "p04192002",
    "p04221958",
    "p04231657",
    "p04231833",
    "p04241504",
    "p05011504",
    "p05011708",
    "p05011842",
    "p05021329",
    "p05021458",
    "p05021659",
    "p05021829"
]

difference = [item for item in interaction_subfolders if item not in ids_list]
print(difference)
difference = [item for item in program_subfolders if item not in ids_list]
print(difference)