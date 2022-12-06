
################### Importing Necessary Libraries ##########################

require(tseries)
require(urca) #Used for the ADF Test
require(PerformanceAnalytics)



##Change this to match where you stored the csv files folder name FullList
setwd("C:/Users/prash/Downloads/ALGO TRADING/QuantInsti-Final-Project-Statistical-Arbitrage-master/database/FullList")


########################### Import Data ##############################

data <- read.csv('sbkrmb.csv')  

pairData <- data


################### Parameters #####################

mean <- 35
criticalValue = -2.58
adfTest = TRUE

####################### Data Cleaning ###############################

#Make sure that the date column is not read in as a vector of characters
pairData$Date <- as.Date(pairData$Date)

#Calculate the Pair Ratio
pairData$pairRatio  <-  pairData[,2] / pairData[,3]

#Calculate the log prices of the two time series
pairData$LogA <- log10(pairData[,2])
pairData$LogB <- log10(pairData[,3])

#Add columns to the DF
pairData$spread <- 0
pairData$adfTest <- 0
pairData$mean <- 0
pairData$stdev <- 0
pairData$zScore <- 0
pairData$signal <- 0
pairData$BuyPrice <- 0
pairData$SellPrice <- 0
pairData$LongReturn <- 0
pairData$ShortReturn <- 0
pairData$Slippage <- 0
pairData$TotalReturn <- 0
pairData$TransactionRatio <- 0
pairData$TradeClose <- 0


######################### ADF Test ###################################


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
  }
}




