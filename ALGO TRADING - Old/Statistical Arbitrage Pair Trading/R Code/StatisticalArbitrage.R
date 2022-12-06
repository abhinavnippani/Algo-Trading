########################################################################################
##                        Imports and set working directory                           ##
########################################################################################
require(tseries)
require(urca) #Used for the ADF Test
require(PerformanceAnalytics)



##Change this to match where you stored the csv files folder name FullList
setwd("C:/Users/prash/Downloads/ALGO TRADING/Statistical Arbitrage Pair Trading/database/FullList")




########################################################################################
##                                    Functions                                       ##
########################################################################################



AddColumns <- function(csvData){
  #Add Columns to csvDataframe
  csvData$spread <- 0
  csvData$adfTest <- 0
  csvData$mean <- 0
  csvData$stdev <- 0
  csvData$zScore <- 0
  csvData$signal <- 0
  csvData$BuyPrice <- 0
  csvData$SellPrice <- 0
  csvData$LongReturn <- 0
  csvData$ShortReturn <- 0
  csvData$Slippage <- 0
  csvData$TotalReturn <- 0
  csvData$TransactionRatio <- 0
  csvData$TradeClose <- 0
  return(csvData)
}




#calculates the pair ratio and adds columns to the dataframe that will be needed later
PrepareData <- function(csvData){
  
  #Make sure that the date column is not read in as a vector of characters
  csvData$Date <- as.Date(csvData$Date)
  
  #Calculate the Pair Ratio
  csvData$pairRatio  <-  csvData[,2] / csvData[,3]
  
  #Calculate the log prices of the two time series
  csvData$LogA <- log10(csvData[,2])
  csvData$LogB <- log10(csvData[,3])
  
  #Add columns to the DF
  csvData$spread <- 0
  csvData$adfTest <- 0
  csvData$mean <- 0
  csvData$stdev <- 0
  csvData$zScore <- 0
  csvData$signal <- 0
  csvData$BuyPrice <- 0
  csvData$SellPrice <- 0
  csvData$LongReturn <- 0
  csvData$ShortReturn <- 0
  csvData$Slippage <- 0
  csvData$TotalReturn <- 0
  csvData$TransactionRatio <- 0
  csvData$TradeClose <- 0
  
  
  
  return(csvData)
}


###################### Generate Row Value ###########################


#Calculate mean, stdDev, and z-score for the given Row [end]
GenerateRowValue <- function(begin, end, csvData){
  
  average <- mean(csvData$spread[begin:end])
  stdev <- sd(csvData$spread[begin:end])
  
  csvData$mean[end] <-  average
  csvData$stdev[end] <- stdev
  csvData$zScore[end] <- (csvData$spread[end]-average)/stdev
  
  return(csvData)
  
}

########################### Generate Signal #########################


#Generate trading signals based on a z-score of 1 and -1 
GenerateSignal <- function(counter, csvData){
  #Trigger and close represent the entry and exit zones (value refers to the z-score value)
  trigger  <- 1
  close  <-  0.5
  
  currentSignal <- csvData$signal[counter]
  prevSignal <- csvData$signal[counter-1]
  
  #Set trading signal for the given [end] row
  if(csvData$adfTest[counter] == 1)
  {
    #If there is a change in signal from long to short then you must allow for the 
    #current trade to first be closed
    if(currentSignal == -1 && prevSignal == 1)
      csvData$signal[counter] <- 0
    else if(currentSignal == 1 && prevSignal == -1)
      csvData$signal[counter] <- 0
    
    #Create a long / short signal if the current z-score is larger / smaller than the trigger value
    #(respectively)
    else if(csvData$zScore[counter] > trigger)
      csvData$signal[counter] <- -1
    else if (csvData$zScore[counter] < -trigger)
      csvData$signal[counter] <- 1
    
    #Close the position if z-score is beteween the two "close" values
    else if (csvData$zScore[counter] < close && csvData$zScore[counter] > -close)
      csvData$signal[counter] <- 0
    else 
      csvData$signal[counter] <- prevSignal
  }
  else 
    csvData$signal[counter] <- 0
  
  return(csvData)
}


######################### Generate Transactions #########################


#Transactions based on trade signal
#Following the framework set out initially by QuantInsti (Note: this can be coded better) 
GenerateTransactions <- function(currentSignal, prevSignal, end, csvData){
  #In a pair trading strategy you need to go long one share and short the other
  #and then reverse the transaction when you close
  
  ##First Leg of the trade (Set Long position)
  #If there is no change in signal
  if(currentSignal == 0 && prevSignal == 0)
  {
    csvData$BuyPrice[end] <- 0    
    csvData$TransactionRatio[end]<-0
  }
  else if(currentSignal == prevSignal)
  {    csvData$BuyPrice[end] <- csvData$BuyPrice[end-1]     
  csvData$TransactionRatio[end]<-csvData$TransactionRatio[end-1]
  }  
  #If the signals point to a new trade
  #Short B and Long A
  else if(currentSignal == 1 && currentSignal != prevSignal)
    csvData$BuyPrice[end] <- csvData[end, 2] 
  #Short A and Long B
  else if(currentSignal == -1 && currentSignal != prevSignal){
    csvData$BuyPrice[end] <- csvData[end, 3] * csvData$pairRatio[end]
    transactionPairRatio <<- csvData$pairRatio[end]
    csvData$TransactionRatio[end]<- transactionPairRatio
  }
  
  #Close trades
  else if(currentSignal == 0 && prevSignal == 1)
    csvData$BuyPrice[end] <- csvData[end, 2] 
  else if(currentSignal == 0 && prevSignal == -1)
  {csvData$TransactionRatio[end] = csvData$TransactionRatio[end-1]
  csvData$BuyPrice[end] <- csvData[end, 3] * csvData$TransactionRatio[end]
  }
  
  
  ##Second Leg of the trade (Set Short position)
  ##Set Short Prices if there is no change in signal
  if(currentSignal == 0 && prevSignal == 0)
    csvData$SellPrice[end] <- 0    
  else if(currentSignal == prevSignal)
    csvData$SellPrice[end] <- csvData$SellPrice[end-1] 
  
  #If the signals point to a new trade
  else if(currentSignal == 1 && currentSignal != prevSignal){
    csvData$SellPrice[end] <- csvData[end, 3] * csvData$pairRatio[end]
    transactionPairRatio <<- csvData$pairRatio[end]
    csvData$TransactionRatio[end]<- transactionPairRatio
  }
  else if(currentSignal == -1 && currentSignal != prevSignal)
    csvData$SellPrice[end] <- csvData[end, 2] 
  
  #Close trades
  else if(currentSignal == 0 && prevSignal == 1){
    csvData$TransactionRatio[end] = csvData$TransactionRatio[end-1]
    csvData$SellPrice[end] <- csvData[end, 3] * csvData$TransactionRatio[end]
  }
  else if(currentSignal == 0 && prevSignal == -1)
    csvData$SellPrice[end] <- csvData[end, 2] 
  
  
  return(csvData)
}

########################### GetReturns Daily ##################################

#Calculate the returns generated after each transaction
#Add implementation shortfall / slippage
GetReturns <- function(end, csvData, slippage){
  #Calculate the returns generated on each leg of the deal (the long and the short position)
  #Long leg of the trade
  if(csvData$signal[end] == 0 && csvData$signal[end-1] != 0 )
    csvData$LongReturn[end] <- log(csvData$BuyPrice[end] / csvData$BuyPrice[end-1])
  #Short Leg of the trade
  if(csvData$signal[end] == 0 && csvData$signal[end-1] != 0 )
    csvData$ShortReturn[end] <- log(csvData$SellPrice[end-1] / csvData$SellPrice[end])
  
  #Add slippage
  if(csvData$signal[end] == 0 && csvData$signal[end-1] != 0 )
  {  csvData$Slippage[end] <- slippage
  }  
  #If a trade was closed then calculate the total return
  if(csvData$signal[end] == 0 && csvData$signal[end-1] != 0 )
  {    csvData$TotalReturn[end] <- ((csvData$ShortReturn[end] + csvData$LongReturn[end]) / 2) + csvData$Slippage[end]
  }  
  return(csvData)
}

#Calculate daily returns generated 
#Add implementation shortfall / slippage at close of trade
GetReturnsDaily <- function(end, csvData, slippage){
  #Calculate the returns generated on each leg of the deal (the long and the short position)
  #Long leg of the trade
  if(csvData$signal[end-1]>0){csvData$LongReturn[end] <- log(csvData[end,2] / csvData[end-1,2])}
  else
    if(csvData$signal[end-1]<0){csvData$LongReturn[end] <- log(csvData[end,3] / csvData[end-1,3])*csvData$TransactionRatio[end]}  
  
  #Short Leg of the trade
  if(csvData$signal[end-1]>0){csvData$ShortReturn[end] <- -log(csvData[end,3] / csvData[end-1,3])*csvData$TransactionRatio[end]}
  else
    if(csvData$signal[end-1]<0){csvData$ShortReturn[end] <- -log(csvData[end,2] / csvData[end-1,2])}  
  
  #Add slippage
  if(csvData$signal[end] == 0 && csvData$signal[end-1] != 0)
  {
    csvData$Slippage[end] <- slippage
    csvData$TradeClose[end] <-1
  }
  #If a trade was closed then calculate the total return
  csvData$TotalReturn[end] <- ((csvData$ShortReturn[end] + csvData$LongReturn[end]) / 2) + csvData$Slippage[end]
  
  return(csvData)
}


#Returns an equity curve, annualized return, annualized sharpe ratio, and max drawdown
GenerateReport <- function(pairData, startDate, endDate){
  #Subset the dates 
  returns  <-  xts(pairData$TotalReturn, as.Date(pairData$Date))
  returns  <-  returns[paste(startDate,endDate,sep="::")]
  #Plot
  charts.PerformanceSummary(returns)
  
  #Metrics
  print(paste("Annual Returns: ",Return.annualized(returns)))
  print(paste("Annualized Sharpe: " ,SharpeRatio.annualized(returns)))
  print(paste("Max Drawdown: ",maxDrawdown(returns)))
  
  pairDataSub=  pairData[pairData$TradeClose==1,]
  
  returns_sub  <-  xts(pairDataSub$TotalReturn, as.Date(pairDataSub$Date))
  returns_sub  <-  returns_sub[paste(startDate,endDate,sep="::")]  
  #var returns = xts object
  totalTrades  <-  0
  positiveTrades  <-  0
  profitsVector  <- c()
  lossesVector  <- c()
  
  #loop through the data to find the + & - trades and total trades
  for(i in returns_sub){
    if(i != 0){
      totalTrades  <- totalTrades + 1
      if(i > 0){
        positiveTrades  <- positiveTrades + 1
        profitsVector  <- c(profitsVector, i)
      }
      else if (i < 0){
        lossesVector  <- c(lossesVector, i)
      }
    }
  }
  
  #Print the results to the console
  print(paste("Total Trades: ", totalTrades))
  print(paste("Success Rate: ", positiveTrades/totalTrades))
  print(paste("PnL Ratio: ", mean(profitsVector)/mean(lossesVector*-1)))
  print(table.Drawdowns(returns))
  
}




##################### BackTest Pair ############################


#The function that will be called by the user to backtest a pair
BacktestPair <- function(pairData, mean = 35, slippage = -0.0025, adfTest = TRUE, criticalValue = -2.58,
                         startDate = '2005-01-01', endDate = '2014-11-23', generateReport = TRUE){
  # At 150 data points
  # Critical value at 1% : -3.46
  # Critical value at 5% : -2.88
  # Critical value at 10% : -2.57
  
  #Prepare the initial dataframe by adding columns and pre calculations
  pairData <- PrepareData(pairData)
  
  #Itterate through each day in the time series
  for(i in 1:length(pairData[,2])){
    
    #For each day after the amount of days needed to run the ADF test
    if(i > 130){
      begin  <-  i - mean + 1
      end  <-  i
      
      #Calculate Spread
      spread  <-  pairData$pairRatio[end]
      pairData$spread[end]  <-  spread
      
      #ADF Test 
      #120 - 90 - 60 
      if(adfTest == FALSE){
        pairData$adfTest[end]  <-  1 
      }
      
      else {
        if(adf.test(pairData$spread[(i-120):end], k = 1)[1] <= criticalValue){
          if(adf.test(pairData$spread[(i-90):end], k = 1)[1] <= criticalValue){
            if(adf.test(pairData$spread[(i-60):end], k = 1)[1] <= criticalValue){
              #If co-integrated then set the ADFTest value to true / 1
              pairData$adfTest[end]  <-  1           
            }
          }
        }
      }
      
    
      #Calculate the remainder variables needed
      if(i >= mean){
        #Generate Row values
        pairData <- GenerateRowValue(begin, end, pairData)
        
        #Generate the Signals
        pairData <- GenerateSignal(i, pairData)
        
        currentSignal  <-  pairData$signal[i]
        prevSignal  <-  pairData$signal[i-1]
        
        #Generate Transactions
        pairData <- GenerateTransactions(currentSignal, prevSignal, i, pairData)
        
        #Get the returns with added slippage
        pairData <- GetReturnsDaily(i, pairData, slippage)
        
      }
    }
  }
  
  if(generateReport == TRUE)
    GenerateReport(pairData, startDate, endDate)
  
  return(pairData)
}










GenerateReport.xts <- function(returns, startDate = '2005-01-01', endDate = '2015-11-23'){
  #Metrics
  returns  <-  returns[paste(startDate,endDate,sep="::")]
  print(paste("Annual Returns: ",Return.annualized(returns)))
  print(paste("Annualized Sharpe: " ,SharpeRatio.annualized(returns)))
  print(paste("Max Drawdown: ",maxDrawdown(returns)))
  print(table.Drawdowns(returns))
  
}




#An equally weighted portfolio of shares
BacktestPortfolio  <- function(names, mean = 35,leverage = 1, startDate = '2005-01-01', endDate = '2015-11-23'){
  ##Itterates through all the pairs and backtests each one
  ##stores the data in a list of numerical vectors
  returns.list  <- list()
  counter  <-  F
  ticker  <- 1
  for (name in names){
    #A notification to let you know how far it is
    print(paste(ticker, " of ", length(names)))
    ticker  <- ticker + 1
    
    #Run the backtest on the pair
    data <- read.csv(name)   
    BackTest.df <- BacktestPair(data, mean, generateReport = FALSE)
    
    #Store the dates in a seperate vector
    if (counter == F){
      dates  <<- as.Date(BackTest.df$Date)
      counter  <- T
    }
    
    #Append to list
    returns.list  <- c(returns.list, list(BackTest.df[,18]))
  }
  
  ##Aggregates the returns for each day and then calculates the average for each day
  total.returns  <- c()
  for (i in 1:length(returns.list)){
    if(i == 1)
      total.returns = returns.list[[i]]
    else
      total.returns = total.returns + returns.list[[i]]
  }
  
  total.returns <- total.returns / length(returns.list)
  
  ##Generate a report for the portfolio
  returns  <-  xts(total.returns * leverage, dates)
  GenerateReport.xts(returns, startDate, endDate)
  
  return(returns)
}


########################################################################################
##                                    Portfolios                                      ##
########################################################################################



##############################
#          Banking           # 
############################## 
##Use this section to test individual pairs
#data <- read.csv('absaned.csv')  
#data <- read.csv('absarmb.csv')  
#data <- read.csv('firstabsa.csv') 
#data <- read.csv('firstned.csv') 
#data <- read.csv('firstrmb.csv') 
#data <- read.csv('nedrmb.csv')   
#data <- read.csv('sbkabsa.csv')  
#data <- read.csv('sbkfirst.csv') 
#data <- read.csv('sbkned.csv')   

path = 'C:/Users/prash/Downloads/ALGO TRADING/Statistical Arbitrage Pair Trading/'

#data <- read.csv(path + 'sbkrmb.csv')  
data <- read.csv(paste0(path,'database/Banks/','SbkRmb.csv'))

a <- BacktestPair(data, 35)

#paste0("s","z")


##Run this section if you want a portfolio
#names  <- c('sbkrmb.csv', 'sbkned.csv', 'sbkfirst.csv', 'sbkabsa.csv', 'nedrmb.csv', 'firstrmb.csv',
#            'firstned.csv', 'firstabsa.csv',  'absarmb.csv', 'absaned.csv')

names  <- c('sbkrmb.csv')

banking.return.series  <- BacktestPortfolio(names, startDate = '2014-11-23', endDate = '2015-11-23')

##Run this code if you want to see the full series (from begining of data to end)
leverage <- 1
GenerateReport.xts(banking.return.series * leverage)

