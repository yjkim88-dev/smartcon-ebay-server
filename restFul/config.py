import sys, os, configparser
from Logger import Logger

HOST_ADR = 'LOCAL' # LOCAL, TEST, REAL

config_par = configparser.ConfigParser()
read_ok = config_par.read(os.path.dirname(os.path.abspath(__file__)) + "/../config.ini")

encticket = "460D4458B6A91623AF5DF21F3B927745537A1D1D99F552C852025F9C0E0D493929B4132A3C7952031C76CCA91E2663282C0E8411F72BD035727EAFC4F1407951311224EB8CA02825A7A626E200205768DCBF5278561BEDA36A5A733B2E2A1FC0CF1BB798A7C47169CA397B2C2E7DD48F"

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