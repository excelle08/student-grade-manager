# -*- coding: utf-8 -*-

from routers import *

from config import configs
import sys, os


def get_mysql_conn_str():
    db_user = configs.db.user
    db_pass = configs.db.password
    db_name = configs.db.database
    db_host = configs.db.host
    db_port = configs.db.port

    return 'mysql+mysqlconnector://' + db_user + ':' + db_pass + '@' + db_host + ':' + str(db_port) + '/' + db_name


def run_app(environ, start_response):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_mysql_conn_str()
    app._static_folder = os.path.abspath('.') + '/static'
    app.config['debug'] = True
    app.config.from_object('config.config')
    return app(environ, start_response)


if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_mysql_conn_str()
    app._static_folder = os.path.abspath('.') + '/static'
    app.config.from_object('config.config')
    app.run(debug=True, host='0.0.0.0')
