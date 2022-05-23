import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm
from designSpace import optimize_altitude
import pandas as pd


material_data: dict = load_materials()