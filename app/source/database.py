from mysql.connector import connect as db

CONFIG = {
	'host': '127.0.0.1',
	'user': 'root',
	'password': '',
	'database': 'burguer',
	'autocommit': False
}

def connect():
	connection = db(**CONFIG)
	return connection
