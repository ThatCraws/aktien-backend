from flask import request, jsonify
from flask_cors import cross_origin
from flask_restx.namespace import Namespace
from flask_restx import Resource
from database.dtos import Exchange, Index, Sector, Stock

namespace = Namespace('stocks', description='')

@namespace.route('/')
class StocksEndpoint(Resource):


    @cross_origin()
    def get(self):

        param_name = request.args.get('name')
        param_index_id = request.args.get('index')
        param_country = request.args.get('country')
        param_sector_id = request.args.get('sector')

        #return all stocks which fit to the chosen filters as a json-list

        query = Stock.query\
            .join(Sector, Stock.sectors)\
            .join(Exchange, Stock.exchanges)\
            .join(Index, Stock.indices)\

        if param_name != None:
            query = query.filter(Stock.name.like('%' + param_name + '%'))

        if param_index_id != None:
            query = query.filter(Index.index_id == param_index_id)

        if param_country != None:
            query = query.filter(Stock.country == param_country)

        if param_sector_id != None:
            query = query.filter(Sector.sector_id == param_sector_id)


        result = query.all()

        json_list = []
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

        return jsonify(json_list)
