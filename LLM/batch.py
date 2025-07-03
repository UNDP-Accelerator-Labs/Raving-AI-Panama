"""
This helper function batches lists of messages according to the max context window used for the LLM.
"""

from colorama import Fore # this is to colorize the terminal output

from itertools import accumulate, groupby
from math import floor

def batch(data):
	"""
	Here we generally need each batch to contain at least two entries.
	Otherwise the LLM classification and keyword extractors will  hallucinate and fail.
	Interestingly, if the batch with one entry is the last in the list,
	it seems to work.
	"""
	lengths = [d['length'] for d in data]
	batch_indexes = [floor(d/(4000*.75)) for d in list(accumulate(lengths))] # Here we multiply the context window of 4000 (used in the ollama interface) by .75 as it is acknowledged that a token is ≈.75 words in English. See: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them.
	batches = [list(g) for k,g in groupby(data, lambda x: batch_indexes[x['i']])]
	print(Fore.YELLOW + 'check batch sizes:')
	print([len(b) for b in batches])
	print(Fore.WHITE)
	return batches