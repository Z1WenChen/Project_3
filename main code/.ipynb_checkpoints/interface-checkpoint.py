import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from functions import stock_df, get_inflation, get_GDP, get_unemployment, get_interest_rates, short_term_cycle, retrieve_beta, retrieve_std, retrieve_sharpe, get_sector
from visualization import line_chart, scatter_chart


stock_sectors = {
            "Energy": ["IYE", "MPC", "HFC", "CLR", "EQT", "XOM", "PSX", "DVN"], 
           "Materials": ["IYM", "BHP", "LIN", "STLD", "X", "FCX", "NEM", "ECL"], 
           "Industrials": ["IYJ", "UPS", "UNP", "RTX", "BA", "GE", "HON", "WM"], 
           "Utilities": ["IDU", "AWK", "DUK", "EIX", "NEE", "BEPC", "ZWS", "NRG"], 
           "Healthcare": ["IYH", "CVS", "UNH", "MCK", "ABC", "CAH", "JNJ", "WBA"], 
           "Financials": ["IYF", "V", "JPM", "BAC", "WFC", "MS", "BX", "C"], 
           "Consumer Discretionary": ["IYC", "AMZN", "TSLA", "HD", "TM", "LVMHF", "MCD", "DIS"], 
           "Consumer Staples": ["IYK", "WMT", "PEP", "COST", "PG", "TGT", "PM", "UL"], 
           "Information Technology": ["IYW", "AAPL", "MSFT", "GOOG", "FB", "NVDA", "HPQ", "INTC"], 
           "Communication Services": ["IYZ", "TMUS", "CMCSA", "VZ", "T", "NTES", "CHTR", "TU"], 
           "Real Estate": ["IYR", "PLD", "AMT", "CCI", "EQIX", "PSA", "SPG", "DLR"],
           "Bonds": ["AGG"]
          }

etf_sectors = {
            "Energy": "IYE", 
           "Materials": "IYM", 
           "Industrials": "IYJ", 
           "Utilities": "IDU", 
           "Healthcare": "IYH", 
           "Financials": "IYF", 
           "Consumer Discretionary": "IYC", 
           "Consumer Staples": "IYK", 
           "Information Technology": "IYW", 
           "Communication Services": "IYZ", 
           "Real Estate": "IYR",
           "Bonds": "AGG"
          }


stocks = []
portfolio = pd.DataFrame()
for key, values in stock_sectors.items():
    if(isinstance(values, list)):
        for value in values:
            stocks.append(value)
                

    
economic_factors = ["Inflation Rate", "Unemployment Rate", "Gross Domestic Product", "Interest Rates"]

short_term_econ_data = short_term_cycle(-100)
long_term_econ_data = short_term_cycle(-225)

etf_dataframe_1 = pd.DataFrame()
for keys, item in stock_sectors.items():
    filler_df = stock_df(item[0], long_term_econ_data.index[0], long_term_econ_data.index[-1], interval_time = "1mo")
    filler_df.dropna(inplace  = True)
    filler_df["Return"] = filler_df["Close"].pct_change()
    etf_dataframe_1[item[0]] = filler_df["Return"]

etf_dataframe_1 = pd.concat([etf_dataframe_1, long_term_econ_data["Economic Stage"] ] , axis = 1)
etf_dataframe_1.dropna(inplace = True)

etf_mean_return = etf_dataframe_1.groupby(["Economic Stage"]).mean()
transposed_etf_mean_return = etf_mean_return.transpose() * 100

    
    
etf_table = pd.DataFrame()
temp_list = []

etf_table["Sector"] = stock_sectors.keys()

for i in range(len(stock_sectors)):
    variable = list(stock_sectors.values())[i][0]
    temp_list.append(variable)

etf_table["ETF Ticker"] = temp_list
etf_table.set_index("ETF Ticker", inplace = True)
 

    
#-----------------------------------------------------------------------------------------------------------------------------------------
    
    
    

    
st.markdown("# Testing ")


st.sidebar.table(etf_table)
    
st.write("The recent changes in economic factors suggest the economy is in a short-term", str(short_term_econ_data["Economic Stage"][-1]).lower() , "condition.")
# st.sidebar.write(stock_sectors)


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


    
#Review factors for client    

select_economic_factor = st.selectbox('Review Economic Factors', [ "" ] + economic_factors)

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
        




#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------



st.plotly_chart(
    scatter_chart(
    etf_mean_return,
    title = "Performance during Economic Cycles since " + str(long_term_econ_data.index[0].year),
    y_axis_title = "Mean Return",
    height = 700,
    width = 650
    ) 
)

with st.expander("Best ETF Returns"):
    st.subheader("Highest Returns: ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(transposed_etf_mean_return["Overheat"].nlargest(n = 3).round(2).astype(str) + "%")
    with col2:
        st.write(transposed_etf_mean_return["Recovery"].nlargest(n = 3).round(2).astype(str) + "%")
    with col3:
        st.write(transposed_etf_mean_return["Reflation"].nlargest(n = 3).round(2).astype(str) + "%")
    with col4:
        st.write(transposed_etf_mean_return["Stagflation"].nlargest(n = 3).round(2).astype(str) + "%")
        
        

with st.expander("Worst ETF Returns"):
    st.subheader("Lowest Returns: ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write(transposed_etf_mean_return["Overheat"].nsmallest(n = 3).round(2).astype(str) + "%")
    with col2:
        st.write(transposed_etf_mean_return["Recovery"].nsmallest(n = 3).round(2).astype(str) + "%")
    with col3:
        st.write(transposed_etf_mean_return["Reflation"].nsmallest(n = 3).round(2).astype(str) + "%")
    with col4:
        st.write(transposed_etf_mean_return["Stagflation"].nsmallest(n = 3).round(2).astype(str) + "%")

    

# select_sector = st.selectbox('Select a sector', [ "" ] + list( stock_sectors.keys() ), 0)

# if select_sector:
    
#     select_ticker = st.selectbox('Select a stock from this sector', [ "" ] + stock_sectors[select_sector])
    
#     if select_ticker:
#         start = st.date_input('Start Date', value= pd.to_datetime('2011-01-01'))
#         end = st.date_input('End Date', value= pd.to_datetime('today'))

#         ticker_df = stock_df(select_ticker, start, end)
#         st.line_chart(ticker_df["Close"])    
        
        
st.write("")
st.write("")
st.write("")
st.write("")

st.write("Choose 3 stocks:")
st.caption("The 3 stocks will be equally weighted with 33% each in the portfolio, and the remaining 1% as cash reserve to pay for 0.1% commission fee. Partial shares are implemented.")

create_portfolio = st.checkbox("Simulate a portfolio")


if create_portfolio:
    
    
    
    initial_value = st.number_input("Initial Portfolio Capital: ", min_value = 1000)    
    
    select_sector = st.selectbox('Select a sector', [ "" ] + list( stock_sectors.keys() ))
    
    
    if select_sector:
    
#         st.write("this is working")
#         click_this = st.button("See what happens")
            
#         if click_this:
#             st.write("This is what happens")
        select_ticker = st.selectbox('Select a stock from this sector', [ "" ] + stock_sectors[select_sector])
    
        if select_ticker:
            
            start = st.date_input('Start Date', value= pd.to_datetime('2022-02-01'))
            end = st.date_input('End Date', value= pd.to_datetime('today'))
        
            market_df = stock_df("^GSPC", start, end)
            ticker_df = stock_df(select_ticker, start, end)
                
            beta = retrieve_beta(ticker_df, market_df)
            beta.dropna(inplace = True)
            
            monthly_volatility = retrieve_std(ticker_df)
            monthly_volatility.dropna(inplace = True)
            
            monthly_sharpe = retrieve_sharpe(ticker_df)
            monthly_sharpe.dropna(inplace = True)
            
            col1, col2, col3, col4 = st.columns(4)
            col2.metric("Weekly Rolling Beta", round(beta[-1], 3), str( round( (beta[-1] - beta[0])/beta[0], 3)  ) + "%",  delta_color ="inverse")
            col1.metric("Closing Price", "$ " + str( round(ticker_df["Close"][-1], 2) ), str( round( (ticker_df["Close"][-1] - ticker_df["Close"][0] ) / ticker_df["Close"][0], 3 )  ) + "%")
            col3.metric("Volatility", round(monthly_volatility[-1], 3), str( round( (monthly_volatility[-1] - monthly_volatility[0])/monthly_volatility[0], 3)  ) + "%", delta_color = "inverse")
            col4.metric("Sharpe Ratio", round(monthly_sharpe[-1], 3), str( round( (monthly_sharpe[-1] - monthly_sharpe[0])/monthly_sharpe[0], 3) ) + "%" )
            
            
    portfolio_tickers = st.multiselect(
        "Select 3 stocks you would like to add to the portfolio.",
         stocks)
    
    portfolio["Ticker"] = portfolio_tickers
    
    sector_list = []
    
    for i in range(len(portfolio_tickers)):
        sector_list.append(get_sector(portfolio_tickers[i]))
                 
    portfolio["Sector"] = sector_list
    
    
    spending_money = initial_value - (0.01 * initial_value)/len(portfolio_tickers)
    
    shares = []
    
    for i in range(len(portfolio_tickers)):
        yf_stock = yf.Ticker(portfolio_tickers[i])
        buy_price = yf_stock.info["regularMarketPrice"]
        shares.append(spending_money/buy_price)
        
    portfolio["Shares"] = shares
    st.dataframe(portfolio)
    st.write("There is $", 0.01 * initial_value, " remaining in your balance.")