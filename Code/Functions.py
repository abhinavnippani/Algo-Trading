

def prev_trading_day(df,date_col = "DATE"):
    
    nse = mcal.get_calendar('NSE')
    holidays = nse.holidays()
    holidays = list(holidays.holidays)
    BUSINESS_DAY = CustomBusinessDay(holidays=holidays)
    result =  df[date_col] - 1 * BUSINESS_DAY
    
    return np.array(result)

