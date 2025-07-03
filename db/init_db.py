from sys import path as syspath
from os.path import join, dirname

from psycopg2.extensions import connection as connectionType

syspath.append(join(dirname(__file__)))
from connect import connect, close
from execute import execute

def init() -> connectionType:
	conn = connect()

	add_dependencies: str = """
		CREATE EXTENSION IF NOT EXISTS ltree;
	"""
	execute(conn,add_dependencies)

	create_table_grievances: str = """
		CREATE TABLE IF NOT EXISTS public.grievances (
			id SERIAL PRIMARY KEY UNIQUE NOT NULL,
			message TEXT,
			prompt TEXT,
			is_generated BOOLEAN DEFAULT FALSE
		);
	"""
	execute(conn,create_table_grievances)

	create_table_associate_grievances_sentiments: str = """
		CREATE TABLE IF NOT EXISTS public.grievance_sentiments (
			grievance INT UNIQUE REFERENCES grievances(id) ON UPDATE CASCADE ON DELETE CASCADE,
			sentiment INT
		);
	"""
	execute(conn,create_table_associate_grievances_sentiments)

	create_table_keywords: str = """
		CREATE TABLE IF NOT EXISTS public.keywords (
			id SERIAL PRIMARY KEY UNIQUE NOT NULL,
			keyword VARCHAR(99) UNIQUE,
			type VARCHAR(9) DEFAULT 'leaf',
			tree ltree default text2ltree(currval(pg_get_serial_sequence('public.keywords','id'))::text)
		);
	"""
	execute(conn,create_table_keywords)

	create_table_associate_grievances_keywords: str = """
		CREATE TABLE IF NOT EXISTS public.grievance_keywords (
			grievance INT REFERENCES grievances(id) ON UPDATE CASCADE ON DELETE CASCADE,
			keyword INT REFERENCES keywords(id) ON UPDATE CASCADE ON DELETE CASCADE
		);
	"""
	execute(conn,create_table_associate_grievances_keywords)

	return conn

if __name__ == '__main__':
	conn = init()
	close(conn)