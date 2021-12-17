import logging

flask_host = ''
flask_port = 0
flask_debug = False
flask_threaded = False
sqlalchemy_database_uri = ''
sqlalchemy_track_modifications = False
json_sort_keys = False
log_file_path = ''
log_level = logging.DEBUG

def set_settings(config):
    global flask_host
    global flask_port
    global flask_debug
    global flask_threaded
    global sqlalchemy_database_uri
    global sqlalchemy_track_modifications
    global json_sort_keys
    global log_file_path
    global log_level

    flask_host = config['host']
    flask_port = config['port']
    flask_debug = config['debugMode']
    flask_threaded = config['flaskThreaded']
    sqlalchemy_database_uri = 'mysql://' + config['databases']['stock_analysis']['user'] + ':' + config['databases']['stock_analysis']['password'] + '@' + config['databases']['stock_analysis']['address'] + ':' + str(config['databases']['stock_analysis']['port']) + '/' + config['databases']['stock_analysis']['database']
    sqlalchemy_track_modifications = config['sqlalchemyTrackModifications']
    json_sort_keys = config['jsonSortKeys']
    log_file_path = config["logger"]["logFilePath"]
    log_level = getLoggerLevel(config)

def getLoggerLevel(config):
    switcher = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "crictical": logging.CRITICAL,
    }

    return switcher.get(config["logger"]["level"], logging.ERROR)
