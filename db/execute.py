from sys import path as syspath
from os.path import join, dirname

from psycopg2.extensions import connection as connectionType, cursor as cursorType

syspath.append(join(dirname(__file__)))
from connect import connect, close

def execute(conn: connectionType,sql: str,values: list=[]) -> list[tuple]:
	open_connection = False
	
	if not conn:
		open_connection = True	
	if open_connection == True:
		conn = connect()
	
	cur: cursorType = conn.cursor()
	cur.execute(sql,values)
	try:
		data = cur.fetchall()
	except:
		data = []
		
	conn.commit()
	cur.close()
	print('Executed SQL')

	if open_connection == True:
		close(conn)

	return data