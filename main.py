
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# %%
# Import other scripts
import data as dt
import functions as fn
import visualizations as vz

# %%
# ---- Base

# Step 1 - Read all the files
data_files = dt.data_files

# Step 2 - Get all the dates
dates = fn.f_dates(p_files=dt.files)

# Display the first 5 dates in the 2 formats
print(dates["i_dates"][0:4])
print(dates["t_dates"][0:4])
# %%
# Step 3 - Get the tickers for the calculations
global_tickers = fn.f_tickers(p_archivos=dt.files, p_data_archivos=data_files)

# Display global tickers
print(global_tickers[0:4])
# %%
# ---- Historical Prices
global_prices = fn.f_get_prices(p_tickers=global_tickers, p_fechas=dates["i_dates"])
precios = global_prices["precios"]

# %%
# DF pasivos
df_pasiva_a = fn.tickin2(0, 25)

df_pasiva_b = fn.tickin4(25, 39)

#%% DF activa
df_activa = fn.tickin3(0,39)