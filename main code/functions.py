import yfinance as yf
import pandas as pd
import cpi
import nasdaqdatalink
import datetime as dt

def stock_df(ticker, start_date, end_date):
    
    stock = yf.Ticker(ticker)
    stock_df = stock.history(start = start_date , end = end_date)
    return stock_df


def get_inflation(years, period):
    
    inflation_rate = []
    cpi_values = []
    datetime_values = []

    #subtract by (years + 1) because we need the beginning annual inflation values by grabbing the year before's data
    start_year = dt.date.today().year - (years+1)
    reset_months = 1
    months =  ( (years + 1) * 12) + (dt.date.today().month-1)

    for i in range(months):
    
        if reset_months > 12: 
            reset_months = 1
            start_year +=1
        
        datetime_values.append(dt.date(start_year, reset_months, 1))
    
        cpi_data = cpi.get(dt.date(start_year, reset_months, 1))
        cpi_values.append(cpi_data)
     
        reset_months += 1
    
        if i >= 12:
            inflation = (cpi_values[i] - cpi_values[i-12]) / cpi_values[i-12]
            inflation_rate.append(inflation)

    datetime_values = datetime_values[12:]
  
    inflation_df = pd.DataFrame(data = {"Inflation Rate": inflation_rate}, index = datetime_values)  
    
    
    if period == "Monthly":
        
        inflation_df["Percent Change"] = inflation_df["Inflation Rate"].pct_change()
        return inflation_df
    
    if period == "Annual":
        
        inflation_df.reset_index(inplace = True)
        inflation_df["Date"] = pd.to_datetime(inflation_df["index"])

        inflation_df = pd.DataFrame(inflation_df.groupby(inflation_df['Date'].dt.year)["Inflation Rate"].agg("mean"))
        inflation_df["Percent Change"] = inflation_df["Inflation Rate"].pct_change()
        
        return inflation_df
    

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
    

def get_employment(years, period):
    
    employment_data = nasdaqdatalink.get("FRED/PAYEMS")
    employment_data /= 1000

    start_year = dt.date.today().year - years
    
    employment_data = employment_data.reset_index()

    for i in range(len(employment_data)):
        entry_year = employment_data.iloc[i,0].date().year
        
        if entry_year == start_year:
            employment_data = employment_data[i:]
            break
    
    if period == "Monthly":
        employment_data.set_index("Date", inplace = True)
        employment_data.rename(columns = {"Value": "Employment in the Millions"}, inplace = True)
        employment_data["Percent Change"] = employment_data["Employment in the Millions"].pct_change()
        return employment_data
    
    if period == "Annual":
        employment_data = pd.DataFrame(employment_data.groupby(employment_data['Date'].dt.year)["Value"].nth(-1))
        employment_data.rename(columns = {"Value": "Employment in the Millions"}, inplace = True)
        employment_data["Percent Change"] = employment_data["Employment in the Millions"].pct_change()
        return employment_data
    

def retrieve_metrics(ticker_df):
    return 0

