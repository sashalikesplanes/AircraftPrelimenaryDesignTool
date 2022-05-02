import os
import yaml


def load_materials():
    lst = os.listdir("data/materials")
    materials = {}
    for filename in lst:
        with open(f'data/materials/{filename}') as file:
            materials[filename] = yaml.load(file, Loader=yaml.FullLoader)
    # print(materials)
    return materials
