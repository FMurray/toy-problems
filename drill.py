from typing import Optional
import duckdb
import click
import requests


@click.command()
def drill():
    """While the program is running, give prompt user to gues the question type"""
    con = duckdb.connect("questions.db")
    lc_questions = con.sql("SELECT * FROM leetcode").df()

    all_types = get_alg_types(con)

    dvals = sorted(all_types)

    for idx, q in lc_questions.iterrows():
        click.echo("Question: " + q["title"])
        q_info = get_q_info(q["titleSlug"])
        md = html_to_markdown(q_info.get("data").get("question").get("content"))
        click.echo(md)
        alg_answer = q["algorithm"]
        ds_answer = q["data_structures"]
        while alg_answer:
            print_n_columns(dvals, 6)
            value = click.prompt("What type of algorithm is this?", type=str)
            if value in alg_answer:
                click.echo(click.style("Correct", fg="green", bold=True))
                alg_answer = None
            else:
                click.echo("Incorrect")

        while ds_answer:
            value = click.prompt("What type of data_structures can you use?", type=str)
            if value in ds_answer:
                click.echo("Correct")
                ds_answer = None
            else:
                click.echo("Incorrect")


def get_types_from_distinct_vals(dvals):
    """Given a tuple of tuples, create a list of all the distinct values"""
    all = set()

    for d in dvals:
        for v in d:
            s = v.split(",")
            for t in s:
                all.add(t)

    return list(all)


def get_alg_types(con):
    types = con.sql("SELECT DISTINCT types FROM algorithms").df()["types"][0]
    return list(types)


def print_n_columns(data_list, n):
    # Determine number of rows needed
    rows = (len(data_list) + n - 1) // n

    # Iterate through rows and columns and print data
    for row in range(rows):
        for col in range(n):
            idx = row + rows * col
            if idx < len(data_list):
                print(f"{data_list[idx]:<20}", end=" ")
        print()  # Print newline at the end of each row


def get_q_info(titleSlug):
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
        "variables": {"titleSlug": titleSlug},
    }
    req = requests.post(BASE_URL, json=data)
    return req.json()


import html2text


def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    return converter.handle(html_content)


if __name__ == "__main__":
    drill()
