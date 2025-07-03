from os import environ
import logging
import psycopg2
from psycopg2.extras import execute_values, Json, LoggingConnection
from psycopg2.extensions import connection as connectionType

def connect() -> connectionType:
	dbinfo = {
		'host': environ['DB_HOST'],
		'port': environ['DB_PORT'],
		'user': environ['DB_USERNAME'],
		'password': environ['DB_PASSWORD'],
		'database': environ['DB_NAME'],
	}
	if environ['FLASK_ENV'] == 'dev':
		logging.basicConfig(level = logging.DEBUG)
		logger = logging.getLogger(__name__)
		conn: connectionType = psycopg2.connect(connection_factory=LoggingConnection, **dbinfo)
		conn.initialize(logger)
	else:
		conn: connectionType = psycopg2.connect(**dbinfo)
	return conn

def close(conn):
	conn.close()