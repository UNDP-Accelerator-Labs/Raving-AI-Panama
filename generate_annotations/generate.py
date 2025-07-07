"""
Without further tuning, it is recommended to use the LLM_keywords function here.
Note however that the script is for basic, zero-shot prompting.
It might be worth exploring few-shot prompting.
"""

from colorama import Fore # this is to colorize the terminal output

import pprint
import json
from sys import path as syspath
from os.path import join, dirname

from keybert import KeyBERT

syspath.append(join(dirname(__file__), '..'))
from LLM import generate

class Keywords:
	def __init__(self,docs,**kwargs):
		self.docs = docs
		self.stream_output = kwargs.get('stream_output', False)
		self.model = kwargs.get('model', 'llama3.1:8B')

		print(Fore.YELLOW)
		print(json.dumps(self.docs))
		print(sum([len(d.split(' ')) for d in self.docs]))
		print(Fore.WHITE)

	def keyBERT(self) -> list[tuple]:
		kw_model = KeyBERT()
		kws = kw_model.extract_keywords(
			self.docs, 
			keyphrase_ngram_range=(1, 5), 
			stop_words=None, 
			min_df=1, 
			use_mmr=True, 
			top_n=5,
			# diversity=.75
		)
		return kws

	def LLM(self) -> dict:
		prompt = f"""
			You are an expert linguist who is good at annotating posts with keywords.
			Help me annotate a list of posts. 
			The posts are provided to you below between three consecutive backticks, in the form of a python list of strings. 
			Each post should not have more than 5 keywords.
			The list of keywords you can chose from is open ended, meaning there is no pre-defined taxonomy.
			You return a list of the keywords for each post, and only those keywords. 
			Your only task is to predict keywords.
			Do not include references to the posts in your output.
			The output should strictly follow the format below between the three hashtags.
			```
			{json.dumps(self.docs)}
			```
			###
			{{'keywords': [[list of keywords for the first post], [list of keywords for the first post], [etc.]]}}
			###
		"""

		full_response = generate(
			prompt,
			model=self.model,
			format='json',
			stream=self.stream_output,
		)

		try:
			return json.loads(full_response)['keywords']
		except:
			print(Fore.RED)
			print('an error in the LLM output occurred')
			print(json.loads(full_response))
			print(Fore.WHITE)
			return []
			# return json.loads(full_response)['keywords']

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
	""",
	"""
		Dear Honorable Municipal Authorities,

		I am writing to express my concern about the lack of streetlights on Calle 50, particularly between Avenida Balboa and Via España. As a resident who lives in this area, I have noticed that the absence of adequate lighting has led to increased instances of petty theft and vandalism during the night.
		I kindly request that you consider installing additional streetlights or increasing the frequency of maintenance for the existing ones to ensure public safety and security.
		Thank you for your attention to this matter.

		Sincerely,
		Ana Gómez'
	""",
	"""
		The new policy has been met with criticism from various stakeholders, who argue that it will disproportionately affect low-income households. 
		They claim that the increased costs will be a significant burden on their already strained budgets.
	""", 
	"""
		I am writing to request permission to hold a charity event in the park. 
		We plan to raise funds for local children's hospitals and would like to use the park as our venue due to its central location and ample space.
	""",
	"""
		The recent changes to the company's policies have caused concern among employees, who feel that their work-life balance has been compromised. 
		They are worried about the impact on their mental health and well-being.
	""",
	"""
		I am writing to express my disappointment with the service I received at your restaurant. The food was cold, and the staff seemed unfriendly and unhelpful
	"""]

	kws = Keywords(docs).LLM()
	pprint.pprint(kws)