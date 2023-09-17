use serde::Deserialize;
use std::path::PathBuf;
use std::process::{self, Command};
use std::fmt;
use std::fs::remove_file;

const LANGUAGES: &[&str] = &["rust", "python"];
const RUSTC_COLOR_ARGS: &[&str] = &["--color", "always"];
const RUSTC_EDITION_ARGS: &[&str] = &["--edition", "2021"];

#[inline]
fn temp_file() -> String {
    let thread_id: String = format!("{:?}", std::thread::current().id())
        .chars()
        .filter(|c| c.is_alphanumeric())
        .collect();

    format!("./temp_{}_{thread_id}", process::id())
}

#[derive(Deserialize, Copy, Clone, Debug)]
#[serde(rename_all = "lowercase")]
pub enum Language {
    Rust,
    Python,
}

#[derive(Deserialize, Copy, Clone, Debug)]
#[serde(rename_all = "lowercase")]
pub enum Mode {
    Compile, 
    Test,
}

#[derive(Deserialize)]
pub struct ProblemList {
    pub problems: Vec<Problem>,
}

#[derive(Deserialize, Debug)]
pub struct Problem {
    pub name: String,
    pub path: PathBuf,
    pub language: Language,
    pub mode: Mode,
}

impl fmt::Display for Problem {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.name)
    }
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
pub struct ProblemOutput {
    pub stdout: String,
    pub stderr: String,
}

struct FileHandle;

impl Drop for FileHandle {
    fn drop(&mut self) {
        clean();
    }
}

#[inline]
fn clean() {
    let _ignored = remove_file(&temp_file());
}

impl Problem {
    pub fn compile(&self) -> Result<CompiledProblem, ProblemOutput> {

        let cmd = match self.mode {
            Mode::Compile => {
                match self.language {
                    Language::Rust => Command::new("rustc")
                        .args(&[self.path.to_str().unwrap(), "-o", &temp_file()])
                        .args(RUSTC_COLOR_ARGS)
                        .args(RUSTC_EDITION_ARGS)
                        .output(), 
                    Language::Python => Command::new("python")
                        .args(&[self.path.to_str().unwrap(), "-o", &temp_file()])
                }



            },
            Mode::Test => Command::new("rustc")
                .args(&["--test", self.path.to_str().unwrap(), "-o", &temp_file()])
                .args(RUSTC_COLOR_ARGS)
                .args(RUSTC_EDITION_ARGS)
                .output(),
            // Language::Python => Ok(())
        }
        .expect("Failed to run 'compile' command");

        if cmd.status.success() {
            Ok(CompiledProblem {
                problem: self,
                _handle: FileHandle,
            })
        } else {
            clean();
            Err(ProblemOutput {
                stdout: String::from_utf8_lossy(&cmd.stdout).to_string(),
                stderr: String::from_utf8_lossy(&cmd.stderr).to_string()
            })
        }
    }

    pub fn run(&self) -> Result<ProblemOutput, ProblemOutput> {
        let arg = match self.mode {
            Mode::Test => "--show-output",
            _ => "",
        };

        let cmd = Command::new(&temp_file())
            .arg(arg)
            .output()
            .expect("Failed to run 'run' command");

        let output = ProblemOutput {
            stdout: String::from_utf8_lossy(&cmd.stdout).to_string(),
            stderr: String::from_utf8_lossy(&cmd.stderr).to_string(),
        };

        if cmd.status.success() {
            Ok(output)
        } else {
            Err(output)
        }
    }
}