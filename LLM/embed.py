from ollama import embed as ollama_embed

def embed(docs):
	embedding = ollama_embed(
		model='nomic-embed-text',
		input=docs
	)
	return list(zip(docs, embedding['embeddings']))

if __name__ == '__main__':
	embedding = embed(['urban landscape', 'artistic expression'])
	print(embedding)