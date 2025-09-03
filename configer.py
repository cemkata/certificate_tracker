import os
import re
import datetime

cnfgFile = "config.ini"

configuration = None

class __Configer:
    #
    # This will protect the configuration values from accidntial change
    #
    def __init__(self, fnameINI=None, fnameJSON=None):
        if fnameINI and os.path.isfile(fnameINI):
            import configparser
            config = configparser.ConfigParser()
            config.read(fnameINI)
            self._port = config['DEFAULT']['Port']
            try:
                self._WARNING = int(config['DEFAULT']['YELLOW'])
            except ValueError:
                self._WARNING = 30
            try:
                self._CRITICAL = int(config['DEFAULT']['RED'])
            except ValueError:
                self._CRITICAL = 15
            
            self._host = config['DEFAULT']['ip']
            ip_pattern = re.compile(r'(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')
            if not ip_pattern.match(self._host) or self._host.lower() == "localhost":
                raise KeyError('Server IP address')
            self._dbpath = os.path.abspath(config['DEFAULT']['dbpath'])

        else:
            self._port = 8000
            self._host = '0.0.0.0'
            self._dbpath = './default.db'

    #INI values
    @property
    def port(self):
        return self._port
    @property
    def host(self):
        return self._host
    @property
    def dbpath(self):
        return self._dbpath
    @property
    def WARNING(self):
        return self._WARNING
    @property
    def CRITICAL(self):
        return self._CRITICAL

def init():
    global configuration

    if configuration:
        return configuration

    configuration = __Configer(fnameINI = cnfgFile)

    basePath = os.path.dirname(configuration.dbpath)
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    if not os.path.isfile(configuration.dbpath):
        with open('db_schema.sql') as db_sch:
            in_sql= db_sch.read()
            from libs.database.DB_controler import create_connection
            conn = create_connection(configuration.dbpath)
            with conn:
                cur = conn.cursor()
                cur.executescript(in_sql)
                conn.commit()
        
    return configuration