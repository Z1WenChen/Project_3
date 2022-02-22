import streamlit as st
import yfinance as yf
import pandas as pd

from functions import stock_df, get_inflation, get_GDP, get_employment


sectors = {
            "Energy": ["XLE"], 
           "Materials": ["XLB"], 
           "Industrials": ["XLI"], 
           "Utilities": ["XLU"], 
           "Healthcare": ["XLV"], 
           "Financials": ["XLF"], 
           "Consumer Discretionary": ["XLY"], 
           "Consumer Staples": ["XLP"], 
           "Information Technology": ["SMH"], 
           "Communication Services": ["XTL"], 
           "Real Estate": ["IYR"]
          }

economic_factors = ["Inflation Rate", "Employment Rate", "Gross Domestic Product", "Interest Rates"]



st.markdown("# Testing ")

select_economic_factor = st.selectbox('Review Economic Status', [ "" ] + economic_factors)

if select_economic_factor:
    
    if select_economic_factor == economic_factors[0]:
        
        years = st.number_input("How many years of data would you like?", max_value = 100, value = 1)
        data_period = st.selectbox("Would you like annually averaged rates or monthly updated rates?", ["Monthly", "Annual"])
        
        historic_inflation_rates = get_inflation(years, data_period)
        st.dataframe(historic_inflation_rates)
        st.line_chart(historic_inflation_rates["Inflation Rate"])
        
        st.write("Current Inflation Rate is", round( historic_inflation_rates.iloc[-1,0] , 4 ), "%.")
        
    if select_economic_factor == economic_factors[1]:
        
        years = st.number_input("How many years of data would you like? (Max value is 83 years)", max_value = 83, value = 1)
        data_period = st.selectbox("Would you like monthly updated or annual count?", ["Monthly", "Annual"])
        
        historic_employment = get_employment(years, data_period)
        st.dataframe(historic_employment)
        st.line_chart(historic_employment["Employment in the Millions"])
        
        
    if select_economic_factor == economic_factors[2]:
        
        years = st.number_input("How many years of data would you like? (Max value is 75 years)", max_value = 75, value = 1)
        data_period = st.selectbox("Would you like quarterly updated or annually average?", ["Quarterly", "Annual"])
        
        historic_gdp = get_GDP(years, data_period)
        st.dataframe(historic_gdp)
        st.line_chart(historic_gdp["USA GDP in $ Trillions"])
        
        


select_sector = st.selectbox('Select a sector', [ "" ] + list( sectors.keys() ), 0)

if select_sector:
    
    select_ticker = st.selectbox('Select a stock from this sector', [ "" ] + sectors[select_sector])
    
    if select_ticker:
        start = st.date_input('Start Date', value= pd.to_datetime('2011-01-01'))
        end = st.date_input('End Date', value= pd.to_datetime('today'))

        ticker_df = stock_df(select_ticker, start, end)
        st.line_chart(ticker_df["Close"])


