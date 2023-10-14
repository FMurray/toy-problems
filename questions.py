import duckdb


def find_leetcode(search: str):
    con = duckdb.connect("questions.db")

    matches = con.sql(f"SELECT * FROM leetcode WHERE titleSlug LIKE '%{search}%'").df()

    return matches


def get_algorithms():
    con = duckdb.connect("questions.db")

    return con.sql("SELECT * FROM algorithms").df()
