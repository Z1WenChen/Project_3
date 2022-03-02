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


def stock_df(ticker, start_date, end_date):
    
    stock = yf.Ticker(ticker)
    stock_df = stock.history(start = start_date , end = end_date)
    return stock_df


# def get_inflation(years, period):
    
#     inflation_rate = []
#     cpi_values = []
#     datetime_values = []

#     #subtract by (years + 1) because we need the beginning annual inflation values by grabbing the year before's data
#     start_year = dt.date.today().year - (years+1)
#     reset_months = 1
#     months =  ( (years + 1) * 12) + (dt.date.today().month-1)

#     for i in range(months):
    
#         if reset_months > 12: 
#             reset_months = 1
#             start_year +=1
        
#         datetime_values.append(dt.date(start_year, reset_months, 1))
    
#         cpi_data = cpi.get(dt.date(start_year, reset_months, 1))
#         cpi_values.append(cpi_data)
     
#         reset_months += 1
    
#         if i >= 12:
#             inflation = (cpi_values[i] - cpi_values[i-12]) / cpi_values[i-12]
#             inflation_rate.append(inflation)

#     datetime_values = datetime_values[12:]
  
#     inflation_df = pd.DataFrame(data = {"Inflation Rate": inflation_rate}, index = datetime_values)  
    
    
#     if period == "Monthly":
        
#         inflation_df["Percent Change"] = inflation_df["Inflation Rate"].pct_change()
#         return inflation_df
    
#     if period == "Annual":
        
#         inflation_df.reset_index(inplace = True)
#         inflation_df["Date"] = pd.to_datetime(inflation_df["index"])

#         inflation_df = pd.DataFrame(inflation_df.groupby(inflation_df['Date'].dt.year)["Inflation Rate"].agg("mean"))
#         inflation_df["Percent Change"] = inflation_df["Inflation Rate"].pct_change()
        
#         return inflation_df

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

def short_term_cycle():
    
    gdp_data = nasdaqdatalink.get("FRED/GDP")
    gdp_data /= 1000
    gdp_data.rename(columns = {"Value": "GDP"}, inplace = True)
    
    cpi_data = nasdaqdatalink.get("FRED/CPIAUCSL")
    cpi_data.rename(columns = {"Value": "CPI"}, inplace = True)
    
    econ_data = pd.concat([gdp_data, cpi_data], axis = 1)
    econ_data =econ_data[-100:]
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
    
    
def retrieve_metrics(ticker_df):
    return 0

