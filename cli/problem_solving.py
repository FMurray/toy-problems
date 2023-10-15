import duckdb

from questions import QuestionList, Question, Step

import asyncio

from textual import events
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer, Container
from textual.widgets import (
    Button,
    Footer,
    Header,
    Static,
    MarkdownViewer,
    TextArea,
    LoadingIndicator,
)


class ProblemSolver(App):
    """Practice solving toy problems."""

    def __init__(self, QuestionList, Question):
        self.question_list = QuestionList
        self.question = self.question_list.question
        self.question.callback_handler = self.text_handler
        super().__init__()

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("s", "submit_step", "Submit the current step")
        # ("shift+enter", "answer_submit", "Submit your answer"),
    ]

    CSS_PATH = "problem_solving.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield MarkdownViewer(self.question.md, show_table_of_contents=True, id="md")
        yield TextArea(
            self.question.step.display_text,
            language="python",
            id="code-editor",
        )

    def text_handler(self, text: str) -> None:
        text_area = self.query_one("#code-editor")
        text_area.insert(text)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    async def action_submit_step(self) -> None:
        """An action to submit an answer."""
        text_area = self.query_one("#code-editor")
        task = asyncio.create_task(
            self.question.chain.apredict(human_input=text_area.text)
        )

        async for i in self.question.token_callback.aiter():
            display_text = self.question.update_response(i)
            text_area.insert(display_text)

        await task


if __name__ == "__main__":
    con = duckdb.connect("../questions.db")
    question_list = QuestionList(con)
    question = question_list.question
    app = ProblemSolver(question_list, question)
    app.run()
