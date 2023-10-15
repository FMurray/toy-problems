import duckdb
import html2text
import requests
import pandas as pd
import asyncio
from dataclasses import dataclass
import dotenv
import os
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.callbacks.base import (
    BaseCallbackHandler,
    AsyncCallbackHandler,
)

from langchain.callbacks import AsyncIteratorCallbackHandler


def problem_solving_chain(question, llm):
    """Chain for practicing solving leetcode problems"""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=f"""
                You are a data structures and algorithms tutor.
                I want to practice solving leetcode problems by using a 7 step process. 
                The 7 steps are:
                1. Listen to the problem (try to find hints in the problem statement)
                2. Make an example that's large and generic. 
                3. State the brute force solution.
                4. Optimize
                5. Walk through algorithm
                6. Translate the algorithm into code.
                7. Verify the correctness of the code.

                Let's take this one step at a time. We will start with step 1. 
                At the end you can give me an evalation based on how well I did on each step.

                The question is: 
                {question.md}

                Here are some hints: 
                {question.hints}

                """,
            ),  # The persistent system prompt
            MessagesPlaceholder(
                variable_name="chat_history"
            ),  # Where the memory will be stored.
            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),  # Where the human input will injected
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
    )
    return llm_chain


def find_leetcode(search: str):
    con = duckdb.connect("questions.db")

    matches = con.sql(f"SELECT * FROM leetcode WHERE titleSlug LIKE '%{search}%'").df()

    return matches


def get_algorithms(con):
    return con.sql("SELECT * FROM algorithms").df()


# @dataclass
# class Step:
#     instructions: str
#     human_input: str
#     tutor_response: str

step_instructions = [
    "Step 1. Listen to the problem. Are there any hints in the problem statement?",
    """
    Step 2. Make an example that's large and generic. 
    """,
    """
    Step 3. State the brute force solution.
    """,
    """
    Step 4. Optimize
    """,
    """
    Step 5. Walk through algorithm
    """,
    """
    Step 6. Translate the algorithm into code.
    """,
    """
    Step 7. Verify the correctness of the code.
    """,
]


class Step:
    def __init__(self):
        self.step_idx = 0
        self.instructions = step_instructions[self.step_idx]
        self.human_input = ""
        self.tutor_response = ""
        self.display_text = str(self.instructions) + "\n\n"

    def __iter__(self):
        return self

    def __next__(self):
        if self.step_idx < len(step_instructions):
            self.step_idx += 1
            return {
                "instructions": step_instructions[self.step_idx],
                "human_input": "",
                "tutor_response": "",
            }
        else:
            raise StopIteration

    def add_tutor_response_token(self, token):
        self.tutor_response += token
        return token


class Question:
    callback_handler = None

    def __init__(self, question_dict: pd.Series):
        self.title_slug = question_dict["titleSlug"]
        self.info = self.get_info()
        self.hints = self.info["data"]["question"]["hints"]
        self.md = self.get_question_markdown()
        dotenv.load_dotenv()

        self.step = Step()

        set_llm_cache(InMemoryCache())
        self.token_callback = AsyncIteratorCallbackHandler()
        llm = ChatOpenAI(
            streaming=True,
            callbacks=[self.token_callback],
            model_name="gpt-4",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.chain = problem_solving_chain(self, llm)

    def get_info(self):
        BASE_URL = "https://leetcode.com/graphql"
        data = {
            "query": """query questionHints($titleSlug: String!) {
                        question(titleSlug: $titleSlug) {
                            questionFrontendId
                            hints
                            similarQuestions
                            codeSnippets {
                                lang
                                langSlug
                                code
                            }
                            content
                        }
                    }
                """,
            "variables": {"titleSlug": self.title_slug},
        }
        req = requests.post(BASE_URL, json=data)
        return req.json()

    def update_response(self, token):
        return self.step.add_tutor_response_token(token)

    def get_question_markdown(self):
        return html_to_markdown(self.info["data"]["question"]["content"])

    def submit_step(self, human_input):
        self.step.human_input = human_input
        response = self.chain.predict(human_input=self.step.human_input)
        self.step.tutor_response = response
        self.step = next(self.step)
        return get_tutor_reponse_comment(response)


class QuestionList:
    """iterator for getting one question at a time"""

    def __init__(self, con):
        self.con = con
        self.questions = get_problems(con)
        self.idx = 0
        self.question = Question(self.questions.iloc[self.idx])

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < len(self.questions):
            q = self.questions.iloc[self.idx]
            self.idx += 1
            self.question = Question(q)
            return self.question
        else:
            raise StopIteration

    def __getitem__(self, idx):
        q = self.questions.iloc[idx]
        return Question(q)


def get_problems(con):
    """Get all problems from the leetcode table."""

    return con.sql("SELECT * FROM leetcode").df()


def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    return converter.handle(html_content)


def get_tutor_reponse_comment(text):
    return "🤖 tutor says: \n".join([f"# {line}" for line in text.split("\n")])
