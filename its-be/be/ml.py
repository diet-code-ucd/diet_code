from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class Question(BaseModel):
    question: str = Field(description="The question.")
    answer: str = Field(description="The answer to the question.")
    explanation: str = Field(description="The explanation of the answer.")
    difficulty: str = Field(description="The difficulty of the question on a scale of 1 to 5.")
    ageRange: str = Field(description="The age range that the question is appropriate for, should be one of the following 0-10, 10-15, 16-18, 18-22, 23-150.")
    tags: List[str] = Field(description="The tags of the question describing keywords of the topic of question.")
    options: List[str] = Field(description="Answer options.")

class ListQuestions(BaseModel):
    questions: List[Question] = Field(description="The list of questions generated.")

model_name = "gpt-3.5-turbo-0613"
temperature = 0.3
llm = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=2500)
parser = PydanticOutputParser(pydantic_object=ListQuestions)

def generate_questions(subject, age, tags):
    system_prompt = """You are a helpful assistant.
    A user will provide you a subject, their age, and any tags to focus on.
    You should generate 10 questions in that subject, appropriate to that age and should be related to the tags.
    At least 3 questions should be from the subject itself, and at least 5 questions should be from the tags.
    With each question, you should also provide the answer, the answer options, explaination (how to solve), a difficulty (scale 1 to 5), and tags (keywords of the topic of question).

    ONLY provide the requested data in JSON a object, and nothing more.
    {format_instructions}
    """
    human_prompt = "My age is {age}. The suject is {subject} with the tags {tags}"

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    input = {"format_instructions": parser.get_format_instructions(), "age": age, "subject": subject, "tags": tags}

    chain = LLMChain(
        llm=llm, 
        prompt=chat_prompt,
    )

    response = chain.run(input)
    parsed_response = parser.parse(response)
    return parsed_response

def generate_learning_material(course, tags): # If we get Age of user we can also modify the parameters and give age specific study material.
    system_prompt = """You are a helpful assistant.
    A user will provide you a list of tags to focus on.
    You should generate study material for the user on that topic.
    The study material should include key concepts, important details, and any relevant examples and website links to relevant material.
    If no tags are provided, you should generate study material on a random topic for the course.
    """
    human_prompt = "The course is {course}, The tags are {tags}"

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    input = {"course": course, "tags": tags}

    chain = LLMChain(
            llm=llm, 
            prompt=chat_prompt,
        )
    
    response = chain.run(input)

    print(response)

    return response

