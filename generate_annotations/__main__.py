from colorama import Fore # this is to colorize the terminal output

import pprint
from sys import path as syspath
from os.path import join, dirname

syspath.append(join(dirname(__file__)))
import classify
import generate

syspath.append(join(dirname(__file__), '..'))
from db import connect, execute, close
from LLM import batch

def run (conn):
	sql = """
		SELECT id, message FROM grievances
		WHERE id NOT IN (
			SELECT grievance FROM grievance_sentiments
		) AND id NOT IN (
			SELECT grievance FROM grievance_keywords
		)
		ORDER BY id
		LIMIT 10;
	"""
	res = execute(conn,sql)

	if len(res) == 0:
		return 0
	else:
		batches = batch([{ 'id': d[0], 'message': d[1], 'length': len(d[1].split(' ')), 'i': i } for i,d in enumerate(res)])

		for b in batches:
			sentiment = classify.sentiment([d['message'][:int(4000*.75)] for d in b])
			kws = generate.Keywords([d['message'][:int(4000*.75)] for d in b]).LLM()

			print(Fore.YELLOW)
			print(sentiment)
			print(len(sentiment))
			print(kws)
			print(len(kws))
			print(Fore.WHITE)

			if len(sentiment) == len(res) and len(kws) == len(res):
				for i,d in enumerate(b):
					# Store the grievance sentiment value
					insert_grievance_sentiment = """
						INSERT INTO grievance_sentiments (grievance, sentiment)
						VALUES (%s,%s)
						ON CONFLICT ON CONSTRAINT grievance_sentiments_grievance_key
						DO UPDATE
							SET sentiment = EXCLUDED.sentiment;
					"""
					execute(conn,insert_grievance_sentiment,[d['id'], sentiment[i]])
					# Store the keywords
					insert_keywords = """
						INSERT INTO keywords (keyword)
						VALUES (unnest(array[%s]))
						ON CONFLICT ON CONSTRAINT keywords_keyword_key
						DO UPDATE
							SET keyword = EXCLUDED.keyword
						RETURNING id;
					"""
					keyword_ids = execute(conn,insert_keywords,[[k.lower() for k in kws[i]]])
					# Store the grievance keywords values
					insert_grievance_keywords = """
						INSERT INTO grievance_keywords (grievance, keyword)
						SELECT %s, vals::int 
						FROM unnest(array[%s]) vals;
					"""
					execute(conn,insert_grievance_keywords,[d['id'], keyword_ids])
			else:
				print(Fore.RED)
				print('failed because either sentiment or keywords length does not match number of posts')
				pass
		return len(res)

if __name__ == '__main__':
	conn = connect()
	remaining = 1
	while remaining > 0: # This is for batching
		remaining = run(conn)
		print(remaining)
	close(conn)