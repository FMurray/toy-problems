use std::{env, fs::{self, DirEntry}, path::PathBuf, collections::HashMap};
use dialoguer::{console::Term, Select, theme::ColorfulTheme};
use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

fn is_toy_problem(path: PathBuf) -> Result<bool, Box<dyn std::error::Error>> {
    let metadata = fs::metadata(&path)?;
    let filename = path.file_name().unwrap().to_str().unwrap();
    Ok(metadata.is_dir() && !filename.contains("."))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let current_dir = env::current_dir()?;
    println!("What do you want to run?");

    let mut toy_problems: HashMap<String, DirEntry> = HashMap::new();
    let mut toy_problem_names: Vec<String> = Vec::new();

    for entry in fs::read_dir(current_dir)? {
        let entry = entry?;
        let path = entry.path();
        
        let is_toy_problem = is_toy_problem(path.clone())?;
        if is_toy_problem {
            let filename = path.file_name().unwrap().to_str().unwrap();
            toy_problems.insert(filename.to_string(), entry);
            toy_problem_names.push(filename.to_string());
        }
    }

    let selection  : Option<usize> = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Select a toy problem")
        .default(0)
        .items(&toy_problem_names[..])
        .interact_on_opt(&Term::stderr())?;

    let selected_problem = toy_problems.get(&toy_problem_names[selection.unwrap()]).unwrap();

    match selection {
        Some(index) => println!("User selected item: {}", toy_problem_names[index]),
        None => println!("User did not select anything"),
    }


    let mut impls: Vec<String> = vec![]; 

    let problem_dir = selected_problem.path();
    for entry in fs::read_dir(problem_dir)? {
        let entry = entry?;
        let path = entry.path();
        let filename = path.file_name().unwrap().to_str().unwrap();
        impls.push(filename.to_string());
        if filename.contains(".rs") {
            println!("Running {}", filename);
            let output = std::process::Command::new("cargo")
                .arg("run")
                .arg("--bin")
                .arg(filename)
                .output()
                .expect("failed to execute process");
            println!("{}", String::from_utf8_lossy(&output.stdout));
        }
    }

    let selected_impl: Option<usize> = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Select an implementation")
        .default(0)
        .items(&impls[..])
        .interact_on_opt(&Term::stderr())?;


    match selected_impl {
        Some(index) => println!("User selected item: {}", impls[index]),
        None => println!("User did not select anything"),
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
