"""
This is a helper function that comes on top of the ollama.generate interface to handle the streaming output.
"""
from sys import argv

import pprint
import json
from ollama import generate as ollama_generate

def generate(prompt,**kwargs) -> dict:
	stream_output = kwargs.get('stream_output', False)
	model = kwargs.get('model', 'llama3.1:8B')
	options = kwargs.get('options', {
		'seed': 42,
		'temperature': 0.2,
		'num_ctx': 4000,
	})
	output_format = kwargs.get('format', None)

	stream = ollama_generate(
		prompt=prompt,
		model=model, 
		options=options,
		format=output_format,
		stream=stream_output,
	)

	full_response = ''

	if stream_output == True:
		for chunk in stream:
			print(chunk['response'], end='', flush=True)
			full_response += chunk['response']
		print('\n')
	else:
		full_response = stream['response']

	return full_response

if __name__ == '__main__':
	if len(argv) > 1:
		generate(argv[1], stream_output=True)
	else:
		print('Please add a prompt when calling this module.')
