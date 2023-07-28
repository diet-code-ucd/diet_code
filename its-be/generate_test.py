import os
import openai
from dotenv import load_dotenv
load_dotenv()

'''api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

stack = ""
MODEL = "gpt-3.5-turbo-0301"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Give me 20 science multiple questions for a 10-15 year old student with answers, justifications, tags(keywords of the topic of question) and also increase the difficulty after exery 5 questions."},
        {"role": "user", "content": "Give the requested data in json format"}
    ],
    temperature=0.3,
    max_tokens=800
)

output = response['choices'][0]['message']['content']
stack == output
print(output)'''

api_key = os.getenv('OPENAI_KEY')
openai.api_key = api_key

def generate_quiz(subject):
    MODEL = "gpt-3.5-turbo-0301"

    # Construct the user prompt based on the subject choice
    prompt = f"Give me 20 {subject} multiple choice questions for a 10-15 year old student with answers, justifications, tags (keywords of the topic of question) and also increase the difficulty after every 5 questions."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": "Give the requested data in JSON format"}
        ],
        temperature=0.3,
        max_tokens=800
    )

    # Process the API response as needed
    # ...

    return response['choices'][0]['message']['content']

# Example usage: Get quiz questions for the subject "Science"
subject_choice = "Science"
quiz_response = generate_quiz(subject_choice)

# Print or process the quiz_response as needed
print(quiz_response)
