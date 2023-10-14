import duckdb

algorithms_table = "algorithms"
leetcode_table = "leetcode"
db = "questions.db"


def _con():
    return duckdb.connect(db)


def seed_algorithms():
    con = duckdb.connect(db)
    duckdb.read_json("algorithms.json")

    con.sql("CREATE OR REPLACE TABLE algorithms AS SELECT * FROM algorithms.json")
    con.close()


def get_algorithms():
    con = _con()

    return con.sql(f"SELECT * FROM {algorithms_table}").df()
