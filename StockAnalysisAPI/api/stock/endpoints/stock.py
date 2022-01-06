from flask import request, jsonify, Response
from flask_restx.namespace import Namespace
# from api.myapi import api
from flask_restx import Resource
# from api.stock.api_definition import page_with_stocks, stock
from api.stock.parser import pagination_parser as pagination
from database.dtos import Exchange, Index, Sector, Stock
import yfinance as yf
import util.calculation_helper as CHelper
import logging


class StockEndpoint(Resource):

    # @api.expect(pagination)
    # @api.marshal_with(page_with_stocks)
    def get(self,id):

        param_period = request.args.get('period')
        param_interval = request.args.get('interval')

        if param_period == None:
            param_period = "1mo"

        #Check for validity
        if (not(param_period == "1d" or param_period == "5d" or param_period == "1mo" or param_period == "3mo" or param_period == "6mo" or
            param_period == "1y" or param_period == "ytd" or param_period == "max")):
            logging.warning("'period' filter is not valid")
            return Response("'period' filter is not valid", status=400)

        if (param_interval != None and (not(param_interval=="1m" or param_interval=="5m" or param_interval=="15m" or param_interval=="30m" or param_interval=="60m"
            or param_interval=="1d" or param_interval=="5d" or param_interval=="1wk" or param_interval=="1mo"))):
            logging.warning("'interval' filter is not valid")
            return Response("'interval' filter is not valid", status=400)


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


        y_stock_data = {
            'price': y_stock.info['currentPrice'],
            'averageDailyVolume10Day' : y_stock.info['averageDailyVolume10Day'],
            'fiftyTwoWeekLow' : y_stock.info['fiftyTwoWeekLow'],
            'fiftyTwoWeekHigh' : y_stock.info['fiftyTwoWeekHigh'],
            'averageVolume' : y_stock.info['averageVolume'],
            'regularMarketVolume' : y_stock.info['regularMarketVolume'],
            'dayLow' : y_stock.info['dayLow'],
            'dayHigh' : y_stock.info['dayHigh'],
            'historicalVolatility' : CHelper.calc_historical_volatility(returns),
            'rsi' : CHelper.calc_current_rsi(df['Close'])
        }
        stock.update(y_stock_data)
        
        new_data = []
        for i in range(len(df['Date'])):
            candle = {
                'x' : df['Date'][i].isoformat(),
                'o' : df['Open'][i],
                'h' : df['High'][i],
                'l' : df['Low'][i],
                'c' : df['Close'][i]
            }
            new_data.append(candle)
        
        new_graph = {
            'data' : new_data
        }

        stock.update(new_graph)
        

        return jsonify(stock)
