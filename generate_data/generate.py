"""
For the purposes of the prototype, we do not distinguish between 
the 10 types of information stored in the TransDoc system.
In case it is necessary, create different prompts for each of the following categories:
- Citizen letter
- Citizen complaint
- Curriculum (CV)
- Invitation
- Note
- Complaint
- Request for social support
- Request for meeting
- Request for information
- Suggestion
"""

from sys import path as syspath, argv
from os.path import join, dirname

syspath.append(join(dirname(__file__), '..'))
from LLM import generate

def grievance(**kwargs) -> tuple[str, str]:
	stream_output = kwargs.get('stream_output', False)
	model = kwargs.get('model', 'llama3.1:8B')

	prompt: str = """
		Generate a short message that a citizen of the city of Panama might write to the municipality government. Write it in English.
		Be creative in the topic of the message.

		Only generate the message. Do not add contextual information like "Here is a sample message".
	"""

	full_response = generate(
		prompt,
		options={},
		model=model,
		stream=stream_output,
	)
	return full_response, prompt

if __name__ == '__main__':
	grievance(stream_output=True)