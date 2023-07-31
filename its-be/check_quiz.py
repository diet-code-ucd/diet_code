import os
import openai
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key


def generate_notes(quiz_op):   
    MODEL = "gpt-3.5-turbo-0301"
    prompt= f"Please check the solved quiz {quiz_op} output and please provide detailed feedback and explanations for any wrong answers, along with relevant reference website links to further understand the correct concepts."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Act like you are the examiner of quiz."},
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



  # quiz_output will be the output of the quiz after hitting submit button.
    #This is just a sample output. Can be changed.
quiz_output = [
    {"question":"What is the speed of light in a vacuum?","answer":"299,792 kilometers per second","user_answer":"299","options":"","tags":"physics,light"},
    {"question":"Who is known as the father of modern physics?","answer":"Albert Einstein","user_answer":"Isaac Newton","options":"Isaac Newton,Galileo Galilei,Niels Bohr,Albert Einstein","tags":"physics,scientists"},
    {"question":"What is Newton's first law of motion?","answer":"An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.","user_answer":"Object at rest does not stay till moved.","options":"","tags":"physics,laws of motion"},
    {"question":"What is the unit of force in the International System of Units (SI)?","answer":"Newton","user_answer":"Newton","options":"Pascal,Joule,Watt,Newton","tags":"physics,units"},
    {"question":"What does E=mc^2 represent?","answer":"Energy equals mass times the speed of light squared","user_answer":"Energy","options":"","tags":"physics,relativity"}
 ] 



result_response = generate_notes(quiz_output)

# Print or process the quiz_response as needed
print(result_response)