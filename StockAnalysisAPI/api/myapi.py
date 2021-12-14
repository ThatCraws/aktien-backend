from flask import Blueprint
from flask_restx import Api
from api.stock.endpoints.stocks import namespace as stocksnamespace
from api.stock.endpoints.filters import namespace as filtersnamespace
from api.stock.endpoints.stock import namespace as stocknamespace

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, version='0.1', title='My Demo API', description='Test')
api.add_namespace(stocksnamespace)
api.add_namespace(filtersnamespace)
api.add_namespace(stocknamespace)

@api.errorhandler
def std_handler(exception):
    return {'message': 'An unexpected error has occured. Please contact the support.'}, 500