
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# Load packages
import pandas as pd
import numpy as np
from os import listdir, path
from os.path import isfile, join

# Load packages
import pandas as pd
import numpy as np
from os import listdir, path
from os.path import isfile, join

# Get the absolute path of the folder
abspath = path.abspath("C:/Users/TOSHIBAUSER/Desktop/Microestructuras_O2022/myst_phmc_lab1/files")

# Read all the files within the files folder
files = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))]

# Chronologically ordered files list
files = ["NAFTRAC_" + i.strftime("%Y%m%d") for i in sorted(pd.to_datetime(files))]

# Read and store all the files in a dictionary
data_files = {}
for i in files:
    # Read the file
    data = pd.read_csv("C:/Users/TOSHIBAUSER/Desktop/Microestructuras_O2022/myst_phmc_lab1/files" + i + ".csv", skiprows=2, header=0)
    # Select only not null columns
    data = data.loc[:, pd.notnull(data.columns)]
    # Clean the ticker name for later use with yfinance
    data["Ticker"] = [i.replace("*","") for i in data["Ticker"]]
    # Weight as decimal
    data["Peso (%)"] = [i/100 for i in data["Peso (%)"]]
    # Save current file in dictionary of data
    data_files[i] = data

# %%
initialdata = pd.read_csv("C:/Users/TOSHIBAUSER/Desktop/Microestructuras_O2022/myst_phmc_lab1/files", skiprows=2, header=0)
