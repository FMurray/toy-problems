use serde::Deserialize;
use std::path::PathBuf;

const languages: &[&str] = &["rust", "python"];

#[derive(Deserialize)]
pub struct ProblemList {
    pub problems: Vec<Problem>,
}

#[derive(Deserialize, Debug)]
pub struct Problem {
    pub name: String,
    pub path: PathBuf,
    pub lang: String,
}

pub struct CompiledProblem<'a> {
    problem: &'a Problem,
    _handle: FileHandle,
}

impl<'a>CompiledProblem<'a> {
    pub fn run(&self) -> Result<ProblemOutput, ProblemOutput> {
        self.problem.run()
    }
}

#[derive(Debug)]