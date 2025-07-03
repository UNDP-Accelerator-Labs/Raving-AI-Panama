"""
Note the .hierarchy method is only for testing. It is not used in the broader pipeline.
"""

import pprint
import json
from sys import path as syspath
from os.path import join, dirname

from sklearn.cluster import AgglomerativeClustering
from itertools import groupby

syspath.append(join(dirname(__file__), '..'))
from LLM import generate, embed
from db import connect, execute, close

class Taxonomy:
	def __init__(self,**kwargs):
		self.docs = kwargs.get('docs', [])
		self.stream_output = kwargs.get('stream_output', False)
		self.model = kwargs.get('model', 'llama3.1:8B')

	def labels(self) -> dict:
		prompt = f"""
			How would you summarize the following list of terms, provided between three back ticks, in a single short phrase?
			Please return only the short phrase, and no extra explanation or suggestions.
			```
			{self.docs}
			```
		"""
		full_response = generate(
			prompt,
			model=self.model,
			stream=self.stream_output,
		)
		return full_response

	def hierarchy(self,group=[]):
		prompt = f"""
			You are an expert linguist who is good at clustering keywords into organized, hierarchical taxonomies.
			Help me cluster a list of keywords.
			The keywords are provided to you below between three consecutive backticks, in the form of a python list of strings. 
			This is not a one shot exercise. There may be pre-existing clusters that these keywords could be related to. When clustering the keywords, consider the cluster labels provided below between three percent signs. It may also be that the keywords are better suited for different, new clusters. In that case, create a new cluster.
			You will assign each keyword to a cluster. 
			You return a list of the clusters, associated with a list of all the keywords that it relates to.
			The output should follow the format below between the three hashtags.
			```
			{kws}
			```
			%%%
			{group}
			%%%
			###
			{{'clusters': [{{'cluster': 'the name of the first cluster', 'keywords': 'a list of all the keyword in the cluster'}}, {{'cluster': 'the name of the second cluster', 'keywords': 'a list of all the keyword in the cluster'}}, {{ etc. }}]}}
			###
		"""
		full_response = generate(
			prompt,
			model=self.model,
			format='json',
			stream=self.stream_output,
		)

		try:
			return json.loads(full_response)['clusters']
		except:
			print(json.loads(full_response))
			return json.loads(full_response)['clusters']
	def clusters(self,conn=None):
		close_conn = False
		if conn is None:
			conn = connect()
			close_conn = True

		sql = """
			SELECT id, keyword FROM keywords
			WHERE type = 'leaf'
				AND nlevel(tree) = 1
			ORDER BY id;
		"""
		res = execute(conn,sql)
		embeddings = embed([d[1] for d in res])

		hierarchical_cluster = AgglomerativeClustering(n_clusters=10, metric='euclidean', linkage='ward')
		labels = hierarchical_cluster.fit_predict([e[1] for e in embeddings])
		
		clusters = list(zip(res, [(l,) for l in labels]))
		# Flatten the tupples
		clusters = ([sum(c, ()) for c in clusters])
		# Group the clusters
		groups = groupby(sorted(clusters, key=lambda x: x[2]), lambda x: x[2])

		if close_conn == True:
			close(conn)

		self.groups = [(k, list(g)) for k,g in groups]
		return self
	def setDocs(self,docs=[]):
		self.docs = docs
		return self

if __name__ == '__main__':
	kws = ['public skate park', 'public spaces', 'urban park', 'public green space', 'public green spaces', 'mini park', 'green spaces', 'public space conversion', 'parks', 'public parks', 'public space', 'public skateparks', 'park']

	h = Taxonomy(kws).labels()
	pprint.pprint(h)