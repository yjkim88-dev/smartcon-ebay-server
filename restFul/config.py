import sys, os, configparser
from Logger import Logger

HOST_ADR = 'TEST' # LOCAL, TEST, REAL

config_par = configparser.ConfigParser()
read_ok = config_par.read(os.path.dirname(os.path.abspath(__file__)) + "/../config.ini")

if len(read_ok) == 0:
    Logger.logger.info ("Not found file the config.ini")
    sys.exit()


class Config():
    UPLOAD_FOLDER = config_par['RESTFUL']['UPLOAD_FOLDER']

class DbCfg():
    DB = config_par[HOST_ADR +'-DB']['DB']
    HOST = config_par[HOST_ADR +'-DB']['HOST']
    PORT = config_par[HOST_ADR +'-DB']['PORT']
    ID = config_par[HOST_ADR +'-DB']['ID']
    PASSWORD = config_par[HOST_ADR +'-DB']['PASSWORD']
    CHARSET = config_par[HOST_ADR +'-DB']['CHARSET']
    # NAME = config_par[HOST_ADR +'-DB']['NAME']