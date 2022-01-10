from flask import jsonify
from flask_restx.namespace import Namespace
from flask_restx import Resource
from database.dtos import Index, Sector, Country

namespace = Namespace('filters', description='')


filter_data = ''

@namespace.route('/')
class FiltersEndpoint(Resource):


    def get(self):

        global filter_data

        #stored in global variable, because available filter data doesn't change during runtime -> data only needs to be calculated once
        if filter_data == '':
            filter_data = [{
            'name': 'sector',
            'options': []
            },
            {
            'name': 'index',
            'options': []
            },
            {
            'name': 'country',
            'options': []
            }
            ]

            #fill the options-lists
            sectors = Sector.query.order_by(Sector.name.asc()).all()
            sector_options = []
            for sector in sectors:
                if sector.language == 'deu':
                    sector_options.append({'value':sector.sector_id,'name':sector.name})
            filter_data[0]['options'] = sector_options

            indices = Index.query.all()
            index_options = []
            for index in indices:
                index_options.append({'value':index.index_id,'name':index.name})
            filter_data[1]['options'] = index_options

            countries = Country.query.order_by(Country.name.asc()).all()
            country_options = []
            for country in countries:
                if country.language == 'deu':
                    country_options.append({'value':country.country_id,'name':country.name})
            filter_data[2]['options'] = country_options

        return jsonify(filter_data)


