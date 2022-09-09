
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
#import yfinance as yf
from yahoofinancials import YahooFinancials as yf
import time
import datetime
from data import data
import data as dt
import pandas_datareader as web
from data import files


# Get Dates
def f_dates(p_files):
    # Labels for dataframe and yfinance
    t_dates = [i.strftime("%d-%m-%Y") for i in sorted([pd.to_datetime(i[8:]).date() for i in p_files])]

    # For other calculations
    i_dates = [i.strftime("%Y-%m-%d") for i in sorted([pd.to_datetime(i[8:]).date() for i in p_files])]

    # Final data to return
    r_f_dates = {"i_dates": i_dates, "t_dates": t_dates}

    return r_f_dates


# %%
# Get Tickers
def f_tickers(p_archivos, p_data_archivos):
    tickers = []
    for i in p_archivos:
        l_tickers = list(p_data_archivos[i]["Ticker"])
        [tickers.append(i + ".MX") for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()

    # Name adjustment
    global_tickers = [i.replace("GFREGIOO.MX", "RA.MX") for i in global_tickers]
    global_tickers = [i.replace("MEXCHEM.MX", "ORBIA.MX") for i in global_tickers]
    global_tickers = [i.replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX") for i in global_tickers]

    # Remove problematic tickers and cash entries
    [global_tickers.remove(i) for i in ["MXN.MX", "USD.MX", "KOFL.MX", "KOFUBL.MX",
                                        "BSMXB.MX", "SITESB.1.MX", "NEMAKA.MX", "NMKA.MX"]]

    return global_tickers


# %%
# Get Prices
def f_get_prices(p_tickers, p_fechas):
    # Initial date, no changes
    f_ini = p_fechas[0]

    # Initial date plus 3 days
    f_fin = str(datetime.datetime.strptime(p_fechas[-1], "%Y-%m-%d") + datetime.timedelta(days=3))[:10]

    # Time counter
    inicio = time.time()

    # Yahoo finance data download
    data = yf.download(p_tickers, start=f_ini, end=f_fin, actions=False, group_by="close",
                       interval="1d", auto_adjust=False, prepost=False, threads=True)

    # Time length of process
    tiempo = "It took", round(time.time() - inicio, 2), "seconds."

    # Morph date column
    data_close = pd.DataFrame({i: data[i]["Close"] for i in p_tickers})

    # We assume NAFRTAC rebalance and Yahoo finance close price times align.

    # Only relevant dates
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(p_fechas)))

    # All prices
    precios = data_close.iloc[[int(np.where(data_close.index == i)[0]) for i in ic_fechas]]

    # Order columns
    precios = precios.reindex(sorted(precios.columns), axis=1)

    return {"precios": precios, "tiempo": tiempo}


# %%
def tickin2(start_date, last_date):
    # Datos base
    kay = pd.read_csv("files/a/NAFTRAC_20180131.csv", skiprows=2, header=0)
    # Transformamos a cash los activos seleccionados
    cash = (kay.iloc[35]["Peso (%)"] + kay.iloc[34]["Peso (%)"] + kay.iloc[16]["Peso (%)"] + kay.iloc[10][
        "Peso (%)"]) / 100 * 1000000
    # Limpiamos tickers
    kay["Ticker"] = [i.replace("*", "") for i in data["Ticker"]]
    kay["Ticker"] = kay["Ticker"] + '.MX'
    kay = kay.drop([10, 16, 34, 35, 36])
    kay = kay.sort_values(by=['Ticker'])
    cash = cash + sum(kay["Peso (%)"] / 100 * 1000000 * 0.00125)
    dates = f_dates(p_files=dt.files)
    # Seleccionamos las fechas mensuales
    fechi = dates["i_dates"][start_date:last_date]
    # Ponemos los pesos
    weight = np.array(kay["Peso (%)"])
    kay["Ticker"] = kay["Ticker"].replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX")
    kay["Ticker"] = kay["Ticker"].replace("SITESB.1.MX", "SITESB-1.MX")
    symbols = np.array(kay["Ticker"])
    # Sacamos los datos de yahoo
    startp = datetime.datetime.strptime(fechi[0], "%Y-%m-%d") - datetime.timedelta(days=1)
    price_data = web.get_data_yahoo(symbols,
                                    start=startp,
                                    end=fechi[-1], interval='d')
    # Acomodamos precios
    price_data = price_data["Adj Close"]
    price_data.index.strftime("%Y-%m-%d")
    # Sacamos rendimientos, retornos y retornos acumulados
    price_data = price_data.loc[fechi]
    ret_data = price_data.pct_change()
    weighted_returns = (weight * ret_data)
    port_ret = weighted_returns.sum(axis=1) / 100
    capital = 1000000 * (1 + port_ret) - cash
    cumulative_ret = (port_ret + 1).cumprod() - 1
    # Creamos el dataframe
    df_pasiva = pd.DataFrame()
    df_pasiva["Capital"] = capital
    df_pasiva["Capital"] = df_pasiva["Capital"].map('${:,.2f}'.format)
    df_pasiva["Rendimiento"] = port_ret
    df_pasiva["Rendimiendo Acumulado"] = cumulative_ret
    df_pasiva.index.names = ['Timestamp']
    df_pasiva.index = df_pasiva.index.strftime("%d-%m-%Y")
    return df_pasiva


# %%
# %%
def tickin3(start_date, last_date):
    # Datos base
    kay = pd.read_csv("files/a/NAFTRAC_20180131.csv", skiprows=2, header=0)
    # Transformamos a cash los activos seleccionados
    cash = (kay.iloc[35]["Peso (%)"] + kay.iloc[34]["Peso (%)"] + kay.iloc[16]["Peso (%)"] + kay.iloc[10][
        "Peso (%)"]) / 100 * 1000000
    # Limpiamos tickers
    kay["Ticker"] = [i.replace("*", "") for i in data["Ticker"]]
    kay["Ticker"] = kay["Ticker"] + '.MX'
    kay = kay.drop([10, 16, 34, 35, 36])
    kay = kay.sort_values(by=['Ticker'])
    cash = cash + sum(kay["Peso (%)"] / 100 * 1000000 * 0.00125)
    dates = f_dates(p_files=dt.files)
    # Seleccionamos las fechas mensuales
    fechi = dates["i_dates"][start_date:last_date]
    # Ponemos los pesos
    weight = np.array(kay["Peso (%)"])
    kay["Ticker"] = kay["Ticker"].replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX")
    kay["Ticker"] = kay["Ticker"].replace("SITESB.1.MX", "SITESB-1.MX")
    symbols = np.array(kay["Ticker"])
    # Sacamos los datos de yahoo
    startp = datetime.datetime.strptime(fechi[0], "%Y-%m-%d") - datetime.timedelta(days=1)
    price_data = web.get_data_yahoo(symbols,
                                    start=startp,
                                    end=fechi[-1], interval='d')
    # Acomodamos precios
    price_data = price_data["Adj Close"]
    price_data.index.strftime("%Y-%m-%d")
    # Sacamos rendimientos, retornos y retornos acumulados
    ret_data = np.log(price_data / price_data.shift())
    weighted_returns = (weight * ret_data)
    port_ret = weighted_returns.sum(axis=1) / 100
    capital = 1000000 * (1 + port_ret) - cash
    cumulative_ret = (port_ret + 1).cumprod() - 1
    # Creamos el dataframe
    df_pasiva = pd.DataFrame()
    df_pasiva["Capital"] = capital
    df_pasiva["Capital"] = df_pasiva["Capital"].map('${:,.2f}'.format)
    df_pasiva["Rendimiento"] = port_ret
    df_pasiva["Rendimiendo Acumulado"] = cumulative_ret
    df_pasiva.index.names = ['Timestamp']
    df_pasiva.index = df_pasiva.index.strftime("%d-%m-%Y")
    return df_pasiva

##
def tickin4(start_date, last_date):
    # Datos base
    kay = pd.read_csv("files/b/NAFTRAC_20200228.csv", skiprows=2, header=0)
    # Transformamos a cash los activos seleccionados
    cash = (kay.iloc[32]["Peso (%)"] + kay.iloc[34]["Peso (%)"] + kay.iloc[10][
        "Peso (%)"]) / 100 * 1000000
    # Limpiamos tickers
    kay["Ticker"] = [i.replace("*", "") for i in data["Ticker"]]
    kay["Ticker"] = kay["Ticker"] + '.MX'
    kay = kay.drop([10, 34, 32, 36])
    kay = kay.sort_values(by=['Ticker'])
    cash = cash + sum(kay["Peso (%)"] / 100 * 1000000 * 0.00125)
    dates = f_dates(p_files=dt.files)
    # Seleccionamos las fechas mensuales
    fechi = dates["i_dates"][start_date:last_date]
    # Ponemos los pesos
    weight = np.array(kay["Peso (%)"])
    kay["Ticker"] = kay["Ticker"].replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX")
    kay["Ticker"] = kay["Ticker"].replace("SITESB.1.MX", "SITESB-1.MX")
    symbols = np.array(kay["Ticker"])
    # Sacamos los datos de yahoo
    startp = datetime.datetime.strptime(fechi[0], "%Y-%m-%d") - datetime.timedelta(days=1)
    price_data = web.get_data_yahoo(symbols,
                                    start=startp,
                                    end=fechi[-1], interval='d')
    # Acomodamos precios
    price_data = price_data["Adj Close"]
    price_data.index.strftime("%Y-%m-%d")
    # Sacamos rendimientos, retornos y retornos acumulados
    price_data = price_data.loc[fechi]
    ret_data = price_data.pct_change()
    weighted_returns = (weight * ret_data)
    port_ret = weighted_returns.sum(axis=1) / 100
    capital = 1000000 * (1 + port_ret) - cash
    cumulative_ret = (port_ret + 1).cumprod() - 1
    # Creamos el dataframe
    df_pasiva = pd.DataFrame()
    df_pasiva["Capital"] = capital
    df_pasiva["Capital"] = df_pasiva["Capital"].map('${:,.2f}'.format)
    df_pasiva["Rendimiento"] = port_ret
    df_pasiva["Rendimiendo Acumulado"] = cumulative_ret
    df_pasiva.index.names = ['Timestamp']
    df_pasiva.index = df_pasiva.index.strftime("%d-%m-%Y")
    return df_pasiva