import sys, os, configparser
from Logger import Logger

config_par = configparser.ConfigParser()
read_ok = config_par.read(os.path.dirname(os.path.abspath(__file__)) + "/../config.ini")

if len(read_ok) == 0:
    Logger.logger.info ("Not found file the config.ini")
    sys.exit()


class Config():
    UPLOAD_FOLDER = config_par['RESTFUL']['UPLOAD_FOLDER']

class DbCfg():
    DB = config_par['DATABASE']['DB']
    HOST = config_par['DATABASE']['HOST']
    PORT = config_par['DATABASE']['PORT']
    ID = config_par['DATABASE']['ID']
    PASSWORD = config_par['DATABASE']['PASSWORD']
    CHARSET = config_par['DATABASE']['CHARSET']
    # NAME = config_par['DATABASE']['NAME']