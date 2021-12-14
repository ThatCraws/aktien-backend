from flask import request, jsonify
from flask_restx.namespace import Namespace
# from api.myapi import api
from flask_restx import Resource
# from api.stock.api_definition import page_with_stocks, stock
from api.stock.parser import pagination_parser as pagination
from database.dtos import Exchange, Index, Sector
import logging

namespace = Namespace('filters', description='')


filter_data = ''

@namespace.route('/')
class FiltersEndpoint(Resource):

    # @api.expect(pagination)
    # @api.marshal_with(page_with_stocks)
    def get(self):

        global filter_data

        #stored in global variable, because available filter data doesn't change during runtime -> data only needs to be calculated once
        if filter_data == '':
            filter_data = [{
            'name': 'sector',
            'options': []
            },
            {
            'name': 'exchange',
            'options': []
            },
            {
            'name': 'index',
            'options': []
            }
            ]

            #fill the options-lists
            sectors = Sector.query.all()
            sector_options = []
            for sector in sectors:
                if sector.language == 'deu':
                    sector_options.append({'value':sector.sector_id,'name':sector.name})
            filter_data[0]['options'] = sector_options

            exchanges = Exchange.query.all()
            exchange_options = []
            for exchange in exchanges:
                exchange_options.append({'value':exchange.exchange_id,'name':exchange.name})
            filter_data[1]['options'] = exchange_options

            indices = Index.query.all()
            index_options = []
            for index in indices:
                index_options.append({'value':index.index_id,'name':index.name})
            filter_data[2]['options'] = index_options
        return jsonify(filter_data)


