import duckdb
import html2text
import requests
import pandas as pd


def find_leetcode(search: str):
    con = duckdb.connect("questions.db")

    matches = con.sql(f"SELECT * FROM leetcode WHERE titleSlug LIKE '%{search}%'").df()

    return matches


def get_algorithms(con):
    return con.sql("SELECT * FROM algorithms").df()


class Question:
    def __init__(self, question_dict: pd.Series):
        self.title_slug = question_dict["titleSlug"]
        self.info = self.get_info()
        self.hints = self.info["data"]["question"]["hints"]
        self.md = self.get_question_markdown()

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

    def get_question_markdown(self):
        return html_to_markdown(self.info["data"]["question"]["content"])


class QuestionList:
    """iterator for getting one question at a time"""

    def __init__(self, con):
        self.con = con
        self.questions = get_problems(con)
        self.idx = 0
        self.current = Question(self.questions.iloc[self.idx])

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < len(self.questions):
            q = self.questions.iloc[self.idx]
            self.idx += 1
            self.current = Question(q)
            return self.current
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
