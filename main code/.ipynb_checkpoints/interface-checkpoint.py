import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from functions import stock_df, get_inflation, get_GDP, get_unemployment, get_interest_rates, short_term_cycle
from visualization import line_chart


sectors = {
            "Energy": ["IYE"], 
           "Materials": ["IYM"], 
           "Industrials": ["IYJ"], 
           "Utilities": ["IDU"], 
           "Healthcare": ["IYH"], 
           "Financials": ["IYF"], 
           "Consumer Discretionary": ["IYC"], 
           "Consumer Staples": ["IYK"], 
           "Information Technology": ["IYW"], 
           "Communication Services": ["IYZ"], 
           "Real Estate": ["IYR"],
           "Bonds": ["AGG"]
          }

economic_factors = ["Inflation Rate", "Unemployment Rate", "Gross Domestic Product", "Interest Rates"]

etf_tickers = ["IYE", "IYM", "IYJ", "IDU", "IYH", "IYF", "IYC", "IYK", "IYW", "IYZ", "IYR", "AGG"]


st.markdown("# Testing ")


short_term_econ_data = short_term_cycle()

st.write("The recent changes in economic factors suggest the economy is in a short-term", str(short_term_econ_data["Economic Stage"][-1]).lower() , "condition.")

if st.checkbox("Show short term phases"):
    
    st.plotly_chart(
        line_chart(
            short_term_econ_data["Stage Index"],
            title = "Implied Economic Conditions",
            y_ticks = short_term_econ_data["Economic Stage"], 
            y_axis_title = "Economic Stage",
            marker_status = True
            )
        )


select_economic_factor = st.selectbox('Review Economic Status', [ "" ] + economic_factors)

if select_economic_factor:
    
    if select_economic_factor == economic_factors[0]:
        
        years = st.number_input("How many years of data would you like?", max_value = 100, value = 1)
        data_period = st.selectbox("Would you like annually averaged rates or monthly updated rates?", ["Monthly", "Annual"])
        
        historic_inflation_rates = get_inflation(years, data_period)
        st.dataframe(historic_inflation_rates)
        
        st.plotly_chart(
            line_chart(
                historic_inflation_rates["Inflation Rate"],
                "Inflation Rate"
            )
        )
#         st.line_chart(historic_inflation_rates["Inflation Rate"])
        
        st.write("Current Inflation Rate is", round( historic_inflation_rates.iloc[-1,0] , 4 ), "%.")
        
    if select_economic_factor == economic_factors[1]:
        
        years = st.number_input("How many years of data would you like? (Max value is 73 years)", max_value = 73, value = 1)
        data_period = st.selectbox("Would you like monthly updated or annual count?", ["Monthly", "Annual"])
        
        historic_unemployment = get_unemployment(years, data_period)
        st.dataframe(historic_unemployment)
#         st.line_chart(historic_employment["Employment in the Millions"])
        st.plotly_chart(
            line_chart(
                historic_unemployment["Unemployment Rate"],
                "Unemployment Rate"
            )
        )
        
        
    if select_economic_factor == economic_factors[2]:
        
        years = st.number_input("How many years of data would you like? (Max value is 75 years)", max_value = 75, value = 1)
        data_period = st.selectbox("Would you like quarterly updated or annually average?", ["Quarterly", "Annual"])
        
        historic_gdp = get_GDP(years, data_period)
        st.dataframe(historic_gdp)
#         st.line_chart(historic_gdp["USA GDP in $ Trillions"])
        st.plotly_chart(
            line_chart(
                historic_gdp["USA GDP in $ Trillions"],
                "USA GDP in $ Trillions"
            )
        )
    
    if select_economic_factor == economic_factors[3]:
        
        years = st.number_input("How many years of data would you like? (Max value is 67 years)", max_value = 67, value = 1)
        data_period = st.selectbox("Would you like monthly rates or annual rates?", ["Monthly", "Annual"])
        
        historic_interest = get_interest_rates(years, data_period)
        st.dataframe(historic_interest)
#         st.line_chart(historic_interest["Interest Rate"])
        st.plotly_chart(
            line_chart(
                historic_interest["Interest Rate"],
                "Interest Rate"
            )
        )
        


select_sector = st.selectbox('Select a sector', [ "" ] + list( sectors.keys() ), 0)

if select_sector:
    
    select_ticker = st.selectbox('Select a stock from this sector', [ "" ] + sectors[select_sector])
    
    if select_ticker:
        start = st.date_input('Start Date', value= pd.to_datetime('2011-01-01'))
        end = st.date_input('End Date', value= pd.to_datetime('today'))

        ticker_df = stock_df(select_ticker, start, end)
        st.line_chart(ticker_df["Close"])


