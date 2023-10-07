use duckdb::{params, Connection, Result};

use duckdb::arrow::record_batch::RecordBatch;
use duckdb::arrow::util::pretty::print_batches;

#[derive(Debug)]
pub struct Question {
    qid: String,
    title: String,
    title_slug: String,
    topic_tags: String,
    category_slug: String,
}

pub fn drill() -> Result<()> {
    let conn = Connection::open_in_memory()?;

    // conn.execute("SELECT * FROM leetcode LIMIT 10")
    let mut stmt = conn.prepare("SELECT * FROM questions.leetcode LIMIT 10")?;

    let question_iter = stmt.query_map([], |row| {
        Ok(Question {
            qid: row.get(0)?,
            title: row.get(1)?,
            title_slug: row.get(2)?,
            topic_tags: row.get(6)?,
            category_slug: row.get(7)?,
        })
    })?;

    for q in question_iter {
        println!("Question {:?}", q.unwrap());
    }

    Ok(())
}
