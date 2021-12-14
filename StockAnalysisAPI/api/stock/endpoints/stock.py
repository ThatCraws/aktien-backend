from flask import request, jsonify
from flask_restx.namespace import Namespace
# from api.myapi import api
from flask_restx import Resource
# from api.stock.api_definition import page_with_stocks, stock
from api.stock.parser import pagination_parser as pagination
from database.dtos import Exchange, Index, Sector, Stock
import yfinance as yf

namespace = Namespace('stock', description='')

@namespace.route('/')
class StockEndpoint(Resource):

    # @api.expect(pagination)
    # @api.marshal_with(page_with_stocks)
    def get(self):

        param_stock_id = request.args.get('id')


        query = Stock.query\
            .join(Sector, Stock.sectors)\
            .join(Exchange, Stock.exchanges)\
            .join(Index, Stock.indices)\


        if param_stock_id != None:
            query = query.filter(Stock.stock_id == param_stock_id)

        result = query.all()
        
        json_list = []
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
            json_list.append(stock)
            
            
        ticker_symbol = stock['symbol']
        if stock['country'] != 'US':
            ticker_symbol+='.{}'.format(stock['country'])
        y_stock = yf.Ticker(ticker_symbol)
        json_list[0]['market_capitalization'] = y_stock.info['marketCap']
        print(y_stock.info)
        y_stock_data = {
            'price': y_stock.info['currentPrice'],
            'averageDailyVolume10Day' : y_stock.info['averageDailyVolume10Day'],
            'fiftyTwoWeekLow' : y_stock.info['fiftyTwoWeekLow'],
            'fiftyTwoWeekHigh' : y_stock.info['fiftyTwoWeekHigh'],
            'averageVolume' : y_stock.info['averageVolume'],
            'regularMarketVolume' : y_stock.info['regularMarketVolume'],
            'dayLow' : y_stock.info['dayLow'],
            'dayHigh' : y_stock.info['dayHigh']
        }
        y_stock_bars_df = yf.download(ticker_symbol)
        json_list.append(y_stock_data)

        #y_stock_bars_df = y_stock_bars_df.reset_index()
        #for i in ['Open','High','Close','Low']:
         #   y_stock_bars_df[i] = y_stock_bars_df[i].astype('float64')
        bar_list = []
        #print(y_stock_bars_df)
        new_keys = []
        for i in range(len(y_stock_bars_df.index)):
            new_keys.append(i)
        y_stock_bars_df.index = new_keys
        #print(y_stock_bars_df)
        #print(y_stock_bars_df.to_dict())
        #for key,row in y_stock_bars_df.iterrows():
            #print(key)

        #json_list.append(y_stock_bars_df.to_dict())


        #json_list.append(y_stock_bars_download.to_dict())
        json_list.append(y_stock_bars_df.to_dict())
        return jsonify(json_list)
