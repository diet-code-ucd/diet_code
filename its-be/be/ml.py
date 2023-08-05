from langchain.llms import OpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

def generate_questions(subject):
    model_name = "text-davinci-003"
    temperature = 0.3
    llm = OpenAI(model_name=model_name, temperature=temperature, max_tokens=-1)
    
    parser = PydanticOutputParser(pydantic_object=ListQuestions)
    
    system_prompt = """You are a helpful assistant.
    A user will provide you with a subject, and you should generate 10 multiple-choice questions in that subject.
    For each question, you should provide the following information:
    - The question itself
    - The options for the question
    - The correct answer option
    - An explanation on why the correct option is the answer
    - The difficulty of the question on a scale from 1 to 5
    - Tags, which are keywords related to the topic of the question
    Please provide the requested data in JSON format, following the given structure:
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "Paris",
        "explanation": "Paris is the capital city of France.",
        "difficulty": 2,
        "tags": ["geography"]
    }
    Please only include the requested data in the JSON object and nothing more.
    {format_instructions}
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_prompt = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    input = {"format_instructions": parser.get_format_instructions(), "text": subject}

    chain = LLMChain(
        llm=llm, 
        prompt=chat_prompt,
    )

    response = chain.run(input)
    parsed_response = parser.parse(response)
    return parsed_response


#TODO: Implement this function
def generate_learning_material(subject):
    pass

class Question(BaseModel):
    question: str = Field(description="The question.")
    answer: str = Field(description="The answer to the question.")
    explanation: str = Field(description="The explanation of the answer.")
    difficulty: str = Field(description="The difficulty of the question on a scale of 1 to 5.")
    ageRange: str = Field(description="The age range that the question is appropriate for, should be one of the following 0-10, 10-15, 16-18, 18-22, 23-150.")
    tags: List[str] = Field(description="The tags of the question describing keywords of the topic of question.")
    options: Optional[List[str]] = Field(description="The options of the question if it is a multiple choice question.")

class ListQuestions(BaseModel):
    questions: List[Question] = Field(description="The list of questions generated.")
