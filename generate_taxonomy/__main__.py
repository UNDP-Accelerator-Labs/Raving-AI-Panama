import pprint
from sys import path as syspath
from os.path import join, dirname

syspath.append(join(dirname(__file__)))
import generate

syspath.append(join(dirname(__file__), '..'))
from db import connect, execute, close

if __name__ == '__main__':
	conn = connect()
	taxonomy = generate.Taxonomy()
	groups = taxonomy.clusters(conn).groups

	for k,g in groups:
		# Generate a label for the groups
		# _g = list(g)
		label = taxonomy.setDocs(docs=[d[1] for d in g]).labels().lower()
		if label.endswith('.'):
			label = label[:-1]
	
		# Store the group label
		insert_group_label = """
			INSERT INTO keywords (keyword, type)
			VALUES (%s, 'group')
			ON CONFLICT ON CONSTRAINT keywords_keyword_key
			DO UPDATE
				SET keyword = EXCLUDED.keyword
			RETURNING id;
		"""
		group_label_id = execute(conn,insert_group_label,[label])[0][0]
		
		# Update the keyword levels
		update_keyword_levels = """
			UPDATE keywords
				SET tree = text2ltree(%s::text) || tree
			WHERE type = 'leaf'
				AND id IN %s
		"""
		execute(conn,update_keyword_levels,[group_label_id, tuple([d[0] for d in g])])
	close(conn)