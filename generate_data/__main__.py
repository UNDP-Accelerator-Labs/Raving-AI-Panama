from sys import path as syspath, argv
from os.path import join, dirname

from psycopg2.extensions import connection as connectionType

syspath.append(join(dirname(__file__)))
import generate

syspath.append(join(dirname(__file__), '..'))
from db import execute, close, init as init_db

def generate_and_store_data(conn: connectionType) -> None:
	grievance, prompt = generate.grievance(stream_output=False)

	sql: str = """
		INSERT INTO grievances (message, prompt)
		VALUES (%s,%s);
	"""
	execute(
		conn,
		sql,
		values=[grievance,prompt],
	)
	print('Stored data')

if __name__ == '__main__':
	conn: connectionType = init_db()

	if len(argv) > 1:
		try:
			n = int(argv[1])
			for i in range(n):
				generate_and_store_data(conn)
		except:
			print('Failed to pass a number. Please declare the number of datapoints you would like to generate.')
	else:
		print('Failed to pass a number. Please declare the number of datapoints you would like to generate.')

	close(conn)