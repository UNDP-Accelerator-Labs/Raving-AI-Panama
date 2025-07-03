from flask import Flask, render_template, url_for, request, redirect

from sys import path as syspath, argv
from os.path import join, dirname

from statistics import mean

syspath.append(join(dirname(__file__), '..'))
from db import connect, execute, close

app = Flask(__name__)
conn = connect()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/get_clusters')
def get_clusters():
	get_groups = """
		SELECT g.id, g.keyword, 
			json_agg(
				json_build_object(
					'id', k.id, 
					'name', k.keyword, 
					'tree', k.tree,
					'value', 1
				)
			) 
		FROM keywords g
		INNER JOIN keywords k
			ON g.tree @> k.tree
		WHERE g.type = 'group'
			AND k.type = 'leaf'
		GROUP BY g.id
		;
	"""
	get_counts = """
		SELECT gk.keyword, COUNT(gk.grievance),
			json_agg(
				json_build_object(
					'grievance', gk.grievance,
					'sentiment', gs.sentiment
				)
			)
		FROM grievance_keywords gk
		LEFT JOIN grievance_sentiments gs
			ON gs.grievance = gk.grievance
		GROUP BY keyword
		;
	"""
	counts = [{ 'kw_id': d[0], 'count': d[1], 'sentiments': d[2] } for d in execute(conn, get_counts)]
	
	groups = [
		{ 
			'id': d[0], 
			'name': d[1], 
			'children': [
				{
					'id': c['id'],
					'name': c['name'],
					'tree': c['tree'],
					'value': next(filter(lambda x: x['kw_id'] == c['id'], counts), None)['count'],
					'avg_sentiment': mean(b['sentiment'] for b in next(filter(lambda x: x['kw_id'] == c['id'], counts), None)['sentiments']),
				}
				for c in d[2] 
			]
		} 
		for d in execute(conn, get_groups)
	]
	clusters = { 'name': 'tree', 'children': groups }
	return clusters

@app.route('/get_grievances/<int:kw>')
def get_grievances(kw):
	print(kw)

	get_grievances = """
		SELECT g.id, g.message,
		json_agg(
			json_build_object(
				'id', k.id,
				'keyword', k.keyword,
				'tree', k.tree
			)
		)
		FROM grievances g
		LEFT JOIN grievance_keywords gk
			ON gk.grievance = g.id
		LEFT JOIN keywords k
			ON k.id = gk.keyword 
		WHERE g.id IN (
			SELECT grievance FROM grievance_keywords
			WHERE keyword = %s
		)
		GROUP BY g.id
		;
	"""
	grievances = [{ 'id': d[0], 'message': d[1], 'keywords': d[2] } for d in execute(conn, get_grievances, [kw])]
	return grievances

if __name__ == '__main__':
	app.run(debug=True)