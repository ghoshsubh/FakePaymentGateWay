import mysql.connector

__cnx = None
def get_sql_connections():
    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(user = 'root', password = 'mysqlradhe', host = '127.0.0.1', database = 'payment_details')
    return __cnx