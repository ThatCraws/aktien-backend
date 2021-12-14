from flask import Flask
from flask_cors import CORS
import settings, pymysql, sys, os, logging
from api.myapi import blueprint as stock_api
from database.db import db
from werkzeug.middleware.proxy_fix import ProxyFix
from util.config_file_reader import readConfig

COMMAND_LINE_PARAM_KEY_PROFILE = "profile:"
DEFAULT_PROFILE = "develop"
CONFIGURATION_FILE_PATH = "stock_analysis_config.yaml"

app = Flask(__name__)
cors = CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

def readCommandLineArguments(paramKey):
    args = sys.argv
    for index, arg in enumerate(args):
        if arg.startswith(paramKey):
            return arg.replace(paramKey, "")

    return ""

def getProfileFromArguments():
    profile = readCommandLineArguments(COMMAND_LINE_PARAM_KEY_PROFILE)

    if profile != "":
        return profile
    else:
        print("No profile in arguments. Use default profile " + DEFAULT_PROFILE)
        return DEFAULT_PROFILE

def loadConfiguration(profile):
    config = readConfig(CONFIGURATION_FILE_PATH, profile)

    if config == None:
        print("Config " + profile + " could not be found")
        return None

    return config

def configure_app(app):
    app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.sqlalchemy_track_modifications
    app.config['JSON_SORT_KEYS'] = settings.json_sort_keys

def init_app(app):
    profile = getProfileFromArguments()
    config = loadConfiguration(profile)
    if config == None:
        logging.critical('no config found')
        exit()

    settings.set_settings(config)

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(filename=settings.log_file_path, level=settings.log_level, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    configure_app(app)
    pymysql.install_as_MySQLdb()
    app.register_blueprint(stock_api)
    db.init_app(app)

def main():
    init_app(app)
    logging.info('backend starting...')
    app.run(debug=settings.flask_debug, threaded=settings.flask_threaded)

if __name__ == '__main__':
    main()
