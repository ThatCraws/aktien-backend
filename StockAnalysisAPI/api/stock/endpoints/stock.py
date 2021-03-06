from flask import request, jsonify, Response
from flask_restx import Resource
from database.dtos import Exchange, Index, Sector, Stock
import yfinance as yf
import util.calculation_helper as CHelper
import logging


class StockEndpoint(Resource):

    def get(self,id):

        param_period = request.args.get('period')
        param_interval = request.args.get('interval')

        date_key = 'Datetime'

        if param_period == None:
            param_period = "1mo"
        
        if param_interval == None:
            param_interval = "1d"

        #Check for validity
        if (not(param_period == "1d" or param_period == "5d" or param_period == "1mo" or param_period == "3mo" or param_period == "6mo" or
            param_period == "1y" or param_period == "ytd" or param_period == "max")):
            logging.warning("'period' filter is not valid")
            return Response("'period' filter is not valid", status=400)

        if (param_interval != None and (not(param_interval=="1m" or param_interval=="5m" or param_interval=="15m" or param_interval=="30m" or param_interval=="60m"
            or param_interval=="1d" or param_interval=="5d" or param_interval=="1wk" or param_interval=="1mo"))):
            logging.warning("'interval' filter is not valid")
            return Response("'interval' filter is not valid", status=400)

        #Because yFinance changes the key name from Datetime to Date when we are using an interval of >= 1d
        if param_interval == "1d" or param_interval == "5d" or param_interval == "1wk" or param_interval == "1mo":
            date_key = "Date"


        query = Stock.query\
            .join(Sector, Stock.sectors)\
            .join(Exchange, Stock.exchanges)\
            .join(Index, Stock.indices)\


        if id != None:
            query = query.filter(Stock.stock_id == id)

        result = query.all()
        
        stock = None
        for i in result:
            stock = i.serialize()

            sectors = []
            for sector in i.sectors:
                if sector.language == 'deu':
                    sectors.append(sector.serialize())

            stock['sectors'] = sectors

            exchanges = []  
            for exchange in i.exchanges:
                exchanges.append(exchange.serialize())

            stock['exchanges'] = exchanges

            indices = []
            for index in i.indices:
                indices.append(index.serialize())

            stock['indices'] = indices
        
        #if the stock wasn't found
        if(stock == None):
            logging.warning("stock with id {} doesn't exist".filter(id))
            return Response("stock with id {} doesn't exist".filter(id), status=400)
            
            
        ticker_symbol = stock['symbol']
        if stock['country'] != 'US':
            ticker_symbol+='.{}'.format(stock['country'])
        y_stock = yf.Ticker(ticker_symbol)
        stock['market_capitalization'] = y_stock.info['marketCap']
        if "trailingPE" in y_stock.info:
            stock['price_earning_ratio'] = '%.2f'%y_stock.info['trailingPE']



        if param_interval == None:
            df = y_stock.history(period=param_period)
        else:
            df = y_stock.history(period=param_period,interval=param_interval)

        #Reseting the index
        df = df.reset_index()#Converting the datatype to float
        for i in ['Open', 'High', 'Close', 'Low']:
            df[i] = df[i].astype('float64')

        returns = []
        for i in range(len(df['Open'])):
            returns.append((df['Close'][i] /df['Open'][i])-1)

        gd_n = CHelper.calc_gd_n(df['Close'],20)
        deviation = CHelper.calc_deviation(gd_n,df['Close'])
        upper = CHelper.calc_upper(gd_n, deviation)
        lower = CHelper.calc_lower(gd_n, deviation)

        y_stock_data = {
            'price': y_stock.info['currentPrice'],
            'averageDailyVolume10Day' : y_stock.info['averageDailyVolume10Day'],
            'fiftyTwoWeekLow' : y_stock.info['fiftyTwoWeekLow'],
            'fiftyTwoWeekHigh' : y_stock.info['fiftyTwoWeekHigh'],
            'averageVolume' : y_stock.info['averageVolume'],
            'regularMarketVolume' : y_stock.info['regularMarketVolume'],
            'dayLow' : y_stock.info['dayLow'],
            'dayHigh' : y_stock.info['dayHigh'],
            'historicalVolatility' : '%.3f'%CHelper.calc_historical_volatility(returns),
            'rsi' : '%.3f'%CHelper.calc_current_rsi(df['Close']),
            'gd' : gd_n,
            'upper': upper,
            'lower': lower
        }
        stock.update(y_stock_data)

        new_data = []

        #Create a new json-object for each date-key, also trim the decimals to 3
        for i in range(len(df[date_key])):
            candle = {
                'x' : df[date_key][i].isoformat(),
                'o' : '%.3f'%(df['Open'][i]),
                'h' : '%.3f'%(df['High'][i]),
                'l' : '%.3f'%(df['Low'][i]),
                'c' : '%.3f'%(df['Close'][i])
            }
            new_data.append(candle)
        
        new_graph = {
            'data' : new_data
        }

        stock.update(new_graph)
        

        return jsonify(stock)
