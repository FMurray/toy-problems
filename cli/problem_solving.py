import duckdb

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

import dotenv
import os
from dataclasses import dataclass

from questions import QuestionList


@dataclass
class Step:
    instructions: str
    human_input: str
    tutor_response: str


class ProblemSolvingTutor:
    step_instructions = [
        """
        Step 1. Listen to the problem. Are there any hints in the problem statement?
        """,
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

    def __init__(self) -> None:
        con = duckdb.connect("../questions.db")
        self.question_list = QuestionList(con)
        self.question = next(self.question_list)
        self.step = self.get_next_step()

    def get_next_step(self):
        return Step(
            instructions=self.step_instructions.pop(0),
            human_input="",
            tutor_response="",
        )


def problem_solving_chain(question):
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


from textual import events
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import (
    Button,
    Footer,
    Header,
    Static,
    MarkdownViewer,
    TextArea,
    RichLog,
)


class ProblemSolver(App):
    """Practice solving toy problems."""

    question_list: QuestionList

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        # ("shift+enter", "answer_submit", "Submit your answer"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield MarkdownViewer(self.question_list.current.md, show_table_of_contents=True)
        yield TextArea(
            """# Start solving the problem -> """,
            language="python",
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_answer_submit(self) -> None:
        """An action to submit an answer."""
        self.submit_answer()

    def submit_answer(self):
        print("submitting answer")


if __name__ == "__main__":
    dotenv.load_dotenv()
    set_llm_cache(InMemoryCache())
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))
    con = duckdb.connect("../questions.db")
    question_list = QuestionList(con)
    app = ProblemSolver()
    app.question_list = question_list
    app.run()
