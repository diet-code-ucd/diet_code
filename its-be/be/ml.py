from flask import current_app
import openai


def generate_quiz(subject):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    MODEL = "gpt-3.5-turbo-0613"

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

    print(response)

    # Process the API response as needed
    # ...

    return response['choices'][0]['message']['content']
