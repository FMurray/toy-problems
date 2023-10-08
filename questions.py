import duckdb


def find_leetcode(search: str):
    con = duckdb.connect("questions.db")

    matches = con.sql(f"SELECT * FROM leetcode WHERE titleSlug LIKE '%{search}'").df()

    return matches
