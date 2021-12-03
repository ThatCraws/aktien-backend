from flask_restx import fields
from api.myapi import api

stock = api.model('Stock', {
    'stock_id': fields.Integer(readOnly=True, description=''),
    'name': fields.String(required=True, description=''),
    'country': fields.String(required=True, description=''),
    'market_capitalization': fields.Integer(description=''),
    'isin': fields.String(description=''),
    'symbol': fields.String(required=True, description=''),
})

pagination = api.model('One page of stocks', {
    'page': fields.Integer(description='Current page'),
    'pages': fields.Integer(description='Total pages'),
    'items_per_page': fields.Integer(description='Items per page'),
    'total_items': fields.Integer(description='Total amount of items'),
})

page_with_stocks = api.inherit('Page with stocks', pagination, {
    'items': fields.List(fields.Nested(stock))
})