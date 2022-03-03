import yfinance as yf
import pandas as pd
import cpi
import nasdaqdatalink
import datetime as dt

import os
from dotenv import load_dotenv

load_dotenv("keys.env")

nasdaq_api_key = os.getenv("NASDAQ_API_KEY")

nasdaqdatalink.ApiConfig.api_key = nasdaq_api_key


def stock_df(ticker, start_date, end_date, interval_time = "1d"):
    
    stock = yf.Ticker(ticker)
    stock_df = stock.history(start = start_date , end = end_date, interval = interval_time)
    return stock_df

def get_sector(ticker, etf_status = False):
    
    if etf_status == True:
        stock = yf.Ticker(ticker)
        max_val = 0

        for i in range(len(stock.info["sectorWeightings"])):
            for x,y in stock.info["sectorWeightings"][i].items():
                if y > max_val:
                    max_val = y
                    sector = x
                    return sector

    if etf_status == False:    
        stock = yf.Ticker(ticker)
        sector = stock.info['sector']
        return sector



def get_inflation(years, period):
    
    cpi_data = nasdaqdatalink.get("FRED/CPIAUCSL")

    start_year = dt.date.today().year - years
    
    cpi_data = cpi_data.reset_index()

    for i in range(len(cpi_data)):
        entry_year = cpi_data.iloc[i,0].date().year
        
        if entry_year == start_year:
            cpi_data = cpi_data[i:]
            break
    
    
    if period == "Monthly":
        cpi_data.set_index("Date", inplace = True)
        cpi_data.rename(columns = {"Value": "CPI"}, inplace = True)
        cpi_data["Inflation Rate"] = cpi_data["CPI"].pct_change(4)
        return cpi_data
    
    if period == "Annual":
        cpi_data = pd.DataFrame(cpi_data.groupby(cpi_data['Date'].dt.year)["Value"].agg("mean"))
        cpi_data.rename(columns = {"Value": "CPI"}, inplace = True)
        cpi_data["Inflation Rate"] = cpi_data["CPI"].pct_change(12)
        return cpi_data
    

def get_GDP(years, period):
    
    gdp_data = nasdaqdatalink.get("FRED/GDP")
    gdp_data /= 1000

    start_year = dt.date.today().year - years
    
    gdp_data = gdp_data.reset_index()

    for i in range(len(gdp_data)):
        entry_year = gdp_data.iloc[i,0].date().year
        
        if entry_year == start_year:
            gdp_data = gdp_data[i:]
            break
    
    if period == "Quarterly":
        gdp_data.set_index("Date", inplace = True)
        gdp_data.rename(columns = {"Value": "USA GDP in $ Trillions"}, inplace = True)
        gdp_data["Percent Change"] = gdp_data["USA GDP in $ Trillions"].pct_change()
        return gdp_data
    
    if period == "Annual":
        gdp_data = pd.DataFrame(gdp_data.groupby(gdp_data['Date'].dt.year)["Value"].agg("mean"))
        gdp_data.rename(columns = {"Value": "USA GDP in $ Trillions"}, inplace = True)
        gdp_data["Percent Change"] = gdp_data["USA GDP in $ Trillions"].pct_change()
        return gdp_data
    

def get_unemployment(years, period):
    
    unemployment_data = nasdaqdatalink.get("FRED/UNRATE")

    start_year = dt.date.today().year - years
    
    unemployment_data = unemployment_data.reset_index()

    for i in range(len(unemployment_data)):
        entry_year = unemployment_data.iloc[i,0].date().year
        
        if entry_year == start_year:
            unemployment_data = unemployment_data[i:]
            break
    
    if period == "Monthly":
        unemployment_data.set_index("Date", inplace = True)
        unemployment_data.rename(columns = {"Value": "Unemployment Rate"}, inplace = True)
        unemployment_data["Percent Change"] = unemployment_data["Unemployment Rate"].pct_change()
        return unemployment_data
    
    if period == "Annual":
        unemployment_data = pd.DataFrame(unemployment_data.groupby(unemployment_data['Date'].dt.year)["Value"].nth(-1))
        unemployment_data.rename(columns = {"Value": "Unemployment Rate"}, inplace = True)
        unemployment_data["Percent Change"] = unemployment_data["Unemployment Rate"].pct_change()
        return unemployment_data
    

def get_interest_rates(years, period):
    
    interest_rates = nasdaqdatalink.get("FRED/FEDFUNDS")

    start_year = dt.date.today().year - years
    
    interest_rates = interest_rates.reset_index()

    for i in range(len(interest_rates)):
        entry_year = interest_rates.iloc[i,0].date().year
        
        if entry_year == start_year:
            interest_rates = interest_rates[i:]
            break
    
    if period == "Monthly":
        interest_rates.set_index("Date", inplace = True)
        interest_rates.rename(columns = {"Value": "Interest Rate"}, inplace = True)
        interest_rates["Percent Change"] = interest_rates["Interest Rate"].pct_change()
        return interest_rates
    
    if period == "Annual":
        interest_rates = pd.DataFrame(interest_rates.groupby(interest_rates['Date'].dt.year)["Value"].nth(-1))
        interest_rates.rename(columns = {"Value": "Interest Rate"}, inplace = True)
        interest_rates["Percent Change"] = interest_rates["Interest Rate"].pct_change()
        return interest_rates

def short_term_cycle(data_entries):
    
    gdp_data = nasdaqdatalink.get("FRED/GDP")
    gdp_data /= 1000
    gdp_data.rename(columns = {"Value": "GDP"}, inplace = True)
    
    cpi_data = nasdaqdatalink.get("FRED/CPIAUCSL")
    cpi_data.rename(columns = {"Value": "CPI"}, inplace = True)
    
    econ_data = pd.concat([gdp_data, cpi_data], axis = 1)
    econ_data =econ_data[data_entries:]
    econ_data.dropna(inplace = True)
    
    econ_data["Inflation_Growth"] = econ_data["CPI"].pct_change()
    econ_data["GDP_Growth"] = econ_data["GDP"].pct_change()

    #Calculate the 1st derivative of economic data
    econ_data["Speed_of_Inflation_Growth"] = econ_data["Inflation_Growth"].pct_change()
    econ_data["Speed_of_GDP_Growth"] = econ_data["GDP_Growth"].pct_change()
    
    econ_data.dropna(inplace = True)
    
    for index, row in econ_data.iterrows():
        if (econ_data.loc[index, 'Speed_of_GDP_Growth'] < 0 and econ_data.loc[index, 'Speed_of_Inflation_Growth'] < 0):
            econ_data.loc[index, 'Stage Index'] = 1
            econ_data.loc[index, 'Economic Stage'] = 'Reflation'
        if (econ_data.loc[index, 'Speed_of_GDP_Growth'] > 0 and econ_data.loc[index, 'Speed_of_Inflation_Growth'] < 0):
            econ_data.loc[index, 'Stage Index'] = 2
            econ_data.loc[index, 'Economic Stage'] = 'Recovery'
        if (econ_data.loc[index, 'Speed_of_GDP_Growth'] > 0 and econ_data.loc[index, 'Speed_of_Inflation_Growth'] > 0):
            econ_data.loc[index, 'Stage Index'] = 3
            econ_data.loc[index, 'Economic Stage'] = 'Overheat'
        if (econ_data.loc[index, 'Speed_of_GDP_Growth'] < 0 and econ_data.loc[index, 'Speed_of_Inflation_Growth'] > 0):
            econ_data.loc[index, 'Stage Index'] = 4
            econ_data.loc[index, 'Economic Stage'] = 'Stagflation'
    
    return econ_data
    
    

    
    
def retrieve_beta(ticker_df, comparison_ticker_df):
    

    adjusted_return = ticker_df["Close"].pct_change()
    benchmark_return = comparison_ticker_df["Close"].pct_change()
    
    rolling_ticker_cov = adjusted_return.rolling(window = 7).cov(benchmark_return)
    benchmark_var = benchmark_return.rolling(window = 7).var()
    
    rolling_beta = rolling_ticker_cov/benchmark_var
    
    return rolling_beta

def retrieve_std(ticker_df):
    
    rolling_volatility  = ticker_df["Close"].rolling(window = 7).std()
    
    return rolling_volatility

def retrieve_sharpe(ticker_df):
    
    trading_days = 252
    
    adjusted_return = ticker_df["Close"].pct_change().dropna()
    rolling_mean_return = adjusted_return.rolling(window = 7).mean()
    annualized_average = rolling_mean_return * trading_days
    
    annualized_rolling_std = adjusted_return.rolling(window = 7).std() * trading_days ** (1/2)
    
    rolling_sharpe = annualized_average/annualized_rolling_std
    
    return rolling_sharpe