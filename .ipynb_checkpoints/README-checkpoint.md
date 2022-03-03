# *Project 3 Team 6: Clockwise your Investment* 
---
**Team members: 
Ziwen Chen,
Andy He, 
Shasha Li, 
Minglu Li**

------------------------------------------------------------------------------------------------------------


**Purpose of the Project**

*1) Find the top performers and worst performers among 12 underlying assets in each of 4 economic stages during the most recent 2 business cycles*

*2) Long top performers and Short worst performers during each economic stage for optimizing the investment return.*

*3) Our project is a prototype for further application and research, such as apply into different theories and can be replaced by other indicators/assets*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/Investment.Clock_Fidelity.jpg)

------------------------------------------------------------------------------------------------------------

**Four Parts of the Project**


**Part 1: Data Preparation**


*1) Imported monthly data of US GDP and Inflation from March 1st, 2004 to November 1st, 2011(FRED Economic Data)
*


*2) Imported 12 underlying assets (11 ETFs and 1 bond) for the same time period and frequency through Yahoo Finance API*

*3) Imported SPY as a benchmark for the same time period*

![alt text](https://github.com/Z1WenChen/Project_2/blob/main/Files/Data%20Prep.png)



**GDP and Inflation**

*1) We calculated the speeds of GDP growth rate and Inflation growth rate respectively. In this way, we can categorize the 4 economic stages according to Merrill Lynch’s Investment Clock Theory.*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/econ_graph.png)
![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/Merrill%20Lynch%20Investment%20Clock%20Theory.jpeg)

*2) 
When speed of GDP growth < 0, and speed of inflation growth < 0
Reflation Stage (Stage 0)

When speed of GDP growth > 0, and speed of inflation growth < 0
	Recovery Stage (Stage 1)
    
When speed of GDP growth > 0, and speed of inflation growth >  0
	Overheat Stage (Stage 2)
    
When speed of GDP growth < 0, and speed of inflation growth > 0
	Stagflation Stage (Stage 3)*
    




**12 Underlying Assets**


*1) We calculated the speeds of GDP growth rate and Inflation growth rate respectively. In this way, we can categorize the 4 economic stages according to Merrill Lynch’s Investment Clock Theory.*

*2) Find the mean return of each ETF in each stage in order to find the top performers and worst performers in each economic stages.*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/ETFs.png)
![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/Mean_return_stage_graph.png)

------------------------------------------------------------------------------------------------------------


**Part 2: Neural Network**

*Solution:*
*1) Encode 4 stages as indicators and create categorical variables to make indicators more “significant” to the signal and train scaled Xs.*
*2) Activation function change to “elu” for 4 hidden layers to produce negative output.*
*3)Activation function change to “linear” for the output layer.*
*4)Loss function change to “mse”.*
*5)Metrics change to “mse”.*


*1)  Use training data to predict*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/Neural_network_training.png)

*2)  Use testing data to predict*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/Neural_network_testing.png)


**Results:**

*Please review the codes "Investment_Clock.ipynb" for more details*

**AGG**
![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/AGG.png)

**IYW**
![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/IYW.png)

**IYR**
![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/IYR.png)

*Finding: The results from neural network reinforece the credibility of the theory*


------------------------------------------------------------------------------------------------------------

**Part 3: Backtesting Performance**

*1) Long 3 top performers and Short 3 worst performers (a total of 6 ETFs) during each economic stage*

*2) Give each ETF 16% weights when calculating returns for each stage, and leave 4% for cash reserve*

*3) Suppose 0.1% commission fee*

*4) Import SPY as a benchmark comparison*

![alt text](https://github.com/Z1WenChen/Project_2/blob/main/Files/Backtesting.png)




**Results:**

*Please review the codes "Investment_Clock_backtest.ipynb" for more details*

![alt text](https://github.com/Z1WenChen/Project_3/blob/main/Documents/backtesting_graph.png)

*Finding 1: Our trading strategy generally underperformed than SPY, but outperformed SPY during 2008-2012 financial crisis*

*Finding 2: During the market crisis in the early 2020 triggered by COVID-19, our strategic return grew steadily while SPY dropped rapidly*

*Finding 3: In general, our strategy is arguably more stable than SPY and could be an effective solution to the major market crisis*


------------------------------------------------------------------------------------------------------------

**Part 4: Streamlit Dashboard**





------------------------------------------------------------------------------------------------------------

**Summary**

![alt text](https://github.com/Z1WenChen/Project_2/blob/main/Files/summary.png)

**1) We apply the investment clock theory driven by economic indicators into real-world investing, using neural network to reinforce its credibility and backtest its profitability**

**2) The top and worst performers in each economic stage are not necessarily exactly the same as the theory suggests in the recent 2 decades**

**3) Our strategy yields a more stable return than the SPY benchmark and could be an investment solution during the market crisis**

------------------------------------------------------------------------------------------------------------

**Next Steps**

*1) We have to rebalance the portfolio each month, which however, causes inevitably high commission fee. We’d like to hold the assets and rebalance the portfolio until economic stage changes, but we haven’t found a way to  deploy this idea yet*

*2) We ignored the fact that there might be an early/late period in each economic stage, during which the assets might perform differently, so we can dig deeper to further analyze this application*

*3) We backtest the performance of the theory because we find that SVC model is not applicable, so we are welcoming any potential applicable algo trading models*

*4) Other alternative assets, such as commodities/cryptos, can be applied into our model*

------------------------------------------------------------------------------------------------------------


**Comments**

*Comment 1: *

*Comment 2: *


