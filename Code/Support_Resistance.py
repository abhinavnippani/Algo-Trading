


def pythag(pt1, pt2):
    a_sq = (pt2[0] - pt1[0]) ** 2
    b_sq = (pt2[1] - pt1[1]) ** 2
    return np.sqrt(a_sq + b_sq)

def local_min_max(pts):
    local_min = []
    local_max = []
    prev_pts = [(0, pts[0]), (1, pts[1])]
    for i in range(1, len(pts) - 1):
        append_to = ''
        if pts[i-1] > pts[i] < pts[i+1]:
            append_to = 'min'
        elif pts[i-1] < pts[i] > pts[i+1]:
            append_to = 'max'
        if append_to:
            if local_min or local_max:
                prev_distance = pythag(prev_pts[0], prev_pts[1]) * 0.5
                curr_distance = pythag(prev_pts[1], (i, pts[i]))
                if curr_distance >= prev_distance:
                    prev_pts[0] = prev_pts[1]
                    prev_pts[1] = (i, pts[i])
                    if append_to == 'min':
                        local_min.append((i, pts[i]))
                    else:
                        local_max.append((i, pts[i]))
            else:
                prev_pts[0] = prev_pts[1]
                prev_pts[1] = (i, pts[i])
                if append_to == 'min':
                    local_min.append((i, pts[i]))
                else:
                    local_max.append((i, pts[i]))
    return local_min, local_max

def regression_ceof(pts):
    X = np.array([pt[0] for pt in pts]).reshape(-1, 1)
    y = np.array([pt[1] for pt in pts])
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0], model.intercept_






def calculate_support_resistance_parameters(series):

    '''
    plt.title(symbol)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.plot(series, label=symbol)
    plt.legend()
    plt.show()
    '''

    # Smoothen the time series plot
    month_diff = series.shape[0] // 30 # Integer divide the number of prices we have by 30
    if month_diff == 0: # We want a value greater than 0
        month_diff = 1
    smooth = int(2 * month_diff + 3) # Simple algo to determine smoothness
    pts = savgol_filter(series, smooth, 3) # Get the smoothened price data


    '''
    plt.title(symbol)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.plot(pts, label=f'Smooth {symbol}')
    plt.legend()
    plt.show()



    plt.title(symbol)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.plot(series, label=symbol)
    plt.plot(pts, label=f'Smooth {symbol}')
    plt.legend()
    plt.show()
    '''


    # Identify the local min and max points in the series
    local_min,local_max = local_min_max(pts)

    # Calculate the Slope and Intercept from the local min and local max points
    local_min_slope, local_min_int = regression_ceof(local_min)
    local_max_slope, local_max_int = regression_ceof(local_max)



    return local_min_slope, local_min_int, local_max_slope, local_max_int





#symbol = "RELIANCE.NS"


def support_resistance(symbol,nse_stocks):


    # Extract the data of last 6 months
    series = np.array(nse_stocks[symbol]["CLOSE"][:90])


    local_min_slope, local_min_int, local_max_slope, local_max_int = calculate_support_resistance_parameters(series)

    '''
    # Calculate the slope and resistance lines
    # y = (m * x) + b
    support = (local_min_slope * np.array(range(series.shape[0]))) + local_min_int
    resistance = (local_max_slope * np.array(range(series.shape[0]))) + local_max_int

    
    
    plt.title(symbol)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.plot(series, label=symbol)
    plt.plot(support, label='Support', c='r')
    plt.plot(resistance, label='Resistance', c='g')
    plt.legend()
    plt.show()
    '''

    support = (local_min_slope * 181) + local_min_int
    resistance = (local_max_slope * 181) + local_max_int


    return support, resistance



























































