"""
This script is for basic, zero-shot prompting.
It might be worth exploring few-shot prompting, or if there is properly annotated data, 
it could be worth thinking about training a proper classifier.

This is inspired by: https://www.youtube.com/watch?v=3z0a3Ymwj1k
"""

import pprint
import json
from sys import path as syspath
from os.path import join, dirname

syspath.append(join(dirname(__file__), '..'))
from LLM import generate

def sentiment(docs,**kwargs) -> dict:
	stream_output = kwargs.get('stream_output', False)
	model = kwargs.get('model', 'llama3.1:8B')

	prompt = f"""
		You are an expert linguist who is good at classifying the sentiment of posts into Positive/Neutral/Negative labels.
		Help me classify a list of posts as: Positive (label=1), Neutral (label=0), and Negative (label=-1).
		The posts are provided to you below between three consecutive backticks, in the form of a python list of strings.
		You return a new ordered list of the sentiment values and only those values. 
		Your only task is to predict labels.
		You do not include references to the posts in your output.
		The output should strictly follow the format below between the three hashtags.
		```
		{json.dumps(docs)}
		```
		###
		{{'sentiments': [list of length {len(docs)} of sentiment values (-1, 0, or 1) for each post]}}
		###
	"""

	full_response = generate(
		prompt,
		model=model, 
		format='json',
		stream=stream_output,
	)

	return json.loads(full_response)['sentiments']

if __name__ == '__main__':
	docs=["""
		Subject: Request for more street art and public murals in Casco Viejo

		Dear Municipalidad de Panamá,

		I am writing to propose an innovative idea that I believe will revitalize the cultural scene of our beloved city. As you know, Casco Viejo is one of the most visited districts in Panama City, attracting tourists and locals alike with its rich history and vibrant atmosphere.
		I would like to suggest creating a public art project featuring large-scale murals throughout the district, highlighting Panamanian culture, history, and identity. These colorful works of art will not only add visual appeal but also provide an educational experience for visitors and residents.
		Imagine strolling through the cobblestone streets of Casco Viejo surrounded by stunning street art, immersing yourself in the sights and sounds of our beautiful country. It would be a unique opportunity to promote local artists, stimulate tourism, and showcase Panamanian creativity on a global scale.
		I propose allocating a specific area for this project, such as the walls surrounding the old city, or even transforming the facades of abandoned buildings into vibrant murals. This initiative will not only beautify our urban landscape but also serve as a platform to share our rich cultural heritage with the world.
		Thank you for considering my proposal. I would be more than happy to discuss this idea further and provide any additional information you may need.

		Sincerely,
		[Your Name]
	""",
	"""
		Dear Municipality of Panama,

		I am writing to express my concern about the recent installation of street art murals on the walls of old buildings in Casco Viejo. While I appreciate the effort to revitalize the area, some of the murals are obstructing the visibility for drivers and pedestrians at certain intersections.
		Could you please consider relocating or adjusting the placement of these murals to ensure public safety and enhance the aesthetic appeal of our city?
		Thank you for your attention to this matter.

		Sincerely,
		Ana Rodriguez
	"""]

	data = sentiment(docs)
	pprint.pprint(data)
