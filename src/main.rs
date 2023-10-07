use crate::drill::drill;
use crate::problems::{Problem, ProblemList};
use crate::run::run;
use argh::FromArgs;
use dialoguer::{console::Term, theme::ColorfulTheme, Select};
use std::fs;
// use pyo3::prelude::*;
// use pyo3::types::IntoPyDict;

mod drill;
mod problems;
mod run;

#[derive(FromArgs, PartialEq, Debug)]
/// For running toy problems with implementations in several languages
struct Args {
    /// show outputs from test problems
    #[argh(switch)]
    nocapture: bool,
    #[argh(subcommand)]
    nested: Option<Subcommands>,
}

#[derive(FromArgs, PartialEq, Debug)]
#[argh(subcommand)]
enum Subcommands {
    Run(RunArgs),
    List(ListArgs),
    Drill(DrillArgs),
}

#[derive(FromArgs, PartialEq, Debug)]
#[argh(subcommand, name = "list")]
/// Lists the available problems
struct ListArgs {
    #[argh(switch, short = 'n')]
    /// show the names of the problems
    names: bool,
}

#[derive(FromArgs, PartialEq, Debug)]
#[argh(subcommand, name = "run")]
/// Runs a specific problem
struct RunArgs {
    #[argh(positional)]
    /// name of the problem
    name: String,
}

#[derive(FromArgs, PartialEq, Debug)]
#[argh(subcommand, name = "drill")]
/// Provides a few differnt drills for quick practice
struct DrillArgs {
    #[argh(positional)]
    /// type of drill
    drill_type: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Args = argh::from_env();

    let toml_str = &fs::read_to_string("info.toml").unwrap();
    let problems = toml::from_str::<ProblemList>(toml_str).unwrap().problems;

    let command = args
        .nested
        .unwrap_or(Subcommands::List(ListArgs { names: true }));
    let verbose = args.nocapture;

    match command {
        Subcommands::List(subargs) => {
            let selection: Option<usize> = Select::with_theme(&ColorfulTheme::default())
                .with_prompt("Select a toy problem")
                .default(0)
                .items(&problems[..])
                .interact_on_opt(&Term::stderr())?;

            match selection {
                Some(index) => {
                    let problem = &problems[index];
                    run(problem, true).unwrap_or_else(|_| std::process::exit(1));
                }
                None => println!("User did not select anything"),
            }
        }
        Subcommands::Run(subargs) => {
            let problem = find_problem(&subargs.name, &problems);
            run(problem, verbose).unwrap_or_else(|_| std::process::exit(1));
        }
        Subcommands::Drill(subargs) => {
            println!("{}", subargs.drill_type);
            let _ = drill();
        }
    }

    // Python::with_gil(|py| {
    //     let builtins = PyModule::import(py, "builtins")?;
    //     let total: i32 = builtins
    //         .getattr("sum")?
    //         .call1((vec![1, 2, 3],),)?
    //         .extract()?;

    //     assert_eq!(total, 6);
    // });

    Ok(())
}

fn find_problem<'a>(name: &str, problems: &'a [Problem]) -> &'a Problem {
    problems.iter().find(|p| p.name == name).unwrap_or_else(|| {
        println!("No problem found for '{name}'");
        std::process::exit(1);
    })
}
