from flask import request, jsonify
from flask_restx.namespace import Namespace
# from api.myapi import api
from flask_restx import Resource
# from api.stock.api_definition import page_with_stocks, stock
from api.stock.parser import pagination_parser as pagination
from database.dtos import Exchange, Index, Sector, Stock

namespace = Namespace('stocks', description='')

@namespace.route('/')
class StocksEndpoint(Resource):

    # @api.expect(pagination)
    # @api.marshal_with(page_with_stocks)
    def get(self):
        # args = pagination.parse_args(request)
        # page = args.get('page', 1)
        # items_per_page = args.get('items_per_page', 10)
        # stocks = Stock.query.paginate(page, items_per_page, error_out=False)
        # return stocks

        param_name = request.args.get('name')
        param_index_id = request.args.get('index')
        param_country = request.args.get('country')
        param_sector_id = request.args.get('sector')

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
