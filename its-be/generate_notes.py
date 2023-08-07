#pip install openai

import os
import openai
from dotenv import load_dotenv
load_dotenv()



api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key


def generate_notes(tags):   # If we get Age of user we can also modify the parameters and give age specific study material.
    MODEL = "gpt-3.5-turbo-0301"

    # Construct the user prompt based on the subject choice. In "{...}" there can be subject name or tags.
    prompt = f"Please generate study notes on {tags}. Include key concepts, important details, and any relevant examples and website links to relevant material."
    
    #prompt2 = f"Check the quiz result (result after the test is solved), give scores and the correct feedback for the wrong answers"
    
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            #{"role": "user", "content": prompt2},
            {"role": "user", "content": prompt},
            {"role": "user", "content": "Give the requested data in text format"}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    # Process the API response as needed
    # ...

    return response['choices'][0]['message']['content']

# Example usage: Get quiz questions for the subject "Science"
tags_choice = "Photosynthesis"
notes_response = generate_notes(tags_choice)

# Print or process the quiz_response as needed
print(notes_response)