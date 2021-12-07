from flask import Flask
import settings
import pymysql
from api.myapi import blueprint as stock_api
from database.db import db
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

def configure_app(app):
    app.config['SWAGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VAL
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JSON_SORT_KEYS'] = settings.JSON_SORT_KEYS

def init_app(app):
    configure_app(app)
    pymysql.install_as_MySQLdb()
    app.register_blueprint(stock_api)
    print("he")
    db.init_app(app)

def main():
    init_app(app)
    app.run(debug=settings.FLASK_DEBUG, threaded=settings.FLASK_THREADED)

if __name__ == 'app':
    main()
