use indicatif::ProgressBar;
use std::time::Duration;

use crate::problems::{Problem, Mode, CompiledProblem};

enum RunMode {
    Interactive,
    NonInteractive,
}

pub fn run(problem: &Problem, verbose: bool) -> Result<(), ()> {
    match problem.mode {
        Mode::Compile => compile_and_run(problem)?,
        Mode::Test => test(problem, verbose)?,
    }
    Ok(())
}

fn compile_and_run(problem: &Problem) -> Result<(), ()> {
    let progress_bar = ProgressBar::new_spinner();
    progress_bar.set_message(format!("Compiling {problem}..."));
    progress_bar.enable_steady_tick(Duration::from_millis(100));

    let compilation_result = problem.compile();
    let compilation = match compilation_result {
        Ok(compilation) => compilation,
        Err(output) => {
            progress_bar.finish_and_clear();
            println!(
                "Compilation of {} failed!, Compiler error message:\n",
                problem
            );
            println!("{}", output.stderr);
            return Err(());
        }
    };

    progress_bar.set_message(format!("Running {problem}..."));
    let result = compilation.run();
    progress_bar.finish_and_clear();

    match result {
        Ok(output) => {
            println!("{}", output.stdout);
            println!("Successfully ran {}", problem);
            Ok(())
        }
        Err(output) => {
            println!("{}", output.stdout);
            println!("{}", output.stderr);

            println!("Ran {} with errors", problem);
            Err(())
        }
    }
}

fn test(problem: &Problem, verbose: bool) -> Result<(), ()> {
    compile_and_test(problem, verbose)?;
    Ok(())
}

fn compile_and_test(problem: &Problem, verbose: bool) -> Result<bool, ()> {
    let progress_bar = ProgressBar::new_spinner();
    progress_bar.set_message(format!("Testing {problem}..."));
    progress_bar.enable_steady_tick(Duration::from_millis(100));

    let compilation = compile(problem, &progress_bar)?;
    let result = compilation.run();
    progress_bar.finish_and_clear();

    match result {
        Ok(output) => {
            if verbose {
                println!("{}", output.stdout);
            }
            Ok(true)
        }
        Err(output) => {
            println!(
                "Testing of {} failed",
                problem
            );
            println!("{}", output.stdout);
            Err(())
        }
    }
}

fn compile<'a, 'b>(
    problem: &'a Problem, 
    progress_bar: &'b ProgressBar,
) -> Result<CompiledProblem<'a>, ()> {
    let compilation_result = problem.compile();

    match compilation_result {
        Ok(compilation) => Ok(compilation),
        Err(output) => {
            progress_bar.finish_and_clear();
            println!(
                "Compiling of {} failed! Here's the output:",
                problem
            );
            println!("{}", output.stderr);
            Err(())
        }
    }
}