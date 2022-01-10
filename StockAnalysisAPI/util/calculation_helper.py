import math
import logging

"""Returns percentage of historical data from returns list"""
def calc_historical_volatility(returns):
    if len(returns) < 2:
        logging.warning("Not enough data(<2) provided to calculate 'historical volatility'")
        return -1

    average_return = sum(returns)/len(returns)
    historical_volatility = 0

    for i in range(len(returns)):
        historical_volatility+=pow((returns[i]-average_return),2)

    historical_volatility = math.sqrt(historical_volatility*(1/len(returns)))
    return '%.3f'%(historical_volatility*100)

"""Best with period of 1-4weeks and 1d interval. Learned from https://www.macroption.com/rsi-calculation/"""
def calc_rsi(closes):
    if len(closes) < 4:
        logging.warning("Not enough data(<4) provided to calculate 'RSI'")
        return [-1]
    #1.calculate up moves(u) and down moves(d)
    u = []
    d = []
    for i in range(len(closes)-1):
        #positive if closes[i] > closes[i+1]
        difference = closes[i]-closes[i+1]

        if difference > 0:
            d.append(difference)
            u.append(0)
        else:
            d.append(0)
            u.append(difference*-1)
    #2.averagaging the advances and declines using simple moving average
    avg_u = []
    avg_d = []
    for i in range(len(u)):
        avg_u.append(sum(u[:(i+1)])/(i+1))
        avg_d.append(sum(d[:(i+1)])/(i+1))
    
    #3.calculate Relative Strength
    rs = []
    for i in range(len(avg_u)):
        if(avg_d[i] != 0):
            rs.append(avg_u[i]/avg_d[i])
        else:
            rs.append(0)

    #4.calculate RSI
    rsi = []
    for i in range(len(rs)):
        rsi.append(100-100/(1+rs[i]))

    return rsi

"""returns the latest RSI"""
def calc_current_rsi(closes):
    rsi_list = calc_rsi(closes)
    return '%.3f'%(rsi_list[len(rsi_list)-1])
