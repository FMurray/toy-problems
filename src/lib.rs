// use pyo3::prelude::*;

// mod dynamic_connectivity {
//     pub mod quick_union;
// }

// pub use crate::dynamic_connectivity::quick_union::QuickUnion;

// /// Formats the sum of two numbers as string.
// #[pyfunction]
// fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }

// /// A Python module implemented in Rust.
// #[pymodule]
// fn toy_problems(_py: Python, m: &PyModule) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
//     m.add_class::<QuickUnion>()?;
//     Ok(())
// }

use rand::Rng;

fn choose_pivot_idx(a: &Vec<i32>) -> usize {
    let mut rng = rand::thread_rng();
    rng.gen_range(0..a.len())
}