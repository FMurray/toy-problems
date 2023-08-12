use pyo3::prelude::*;

#[pyclass]
pub struct QuickUnion {
    id: Vec<usize>,
    sz: Vec<usize>,
}

#[pymethods]
impl QuickUnion {
    
    #[new]
    pub fn new(n: usize) -> Self {
        QuickUnion {
            id: (0..n).collect(),
            sz: (0..n).collect(),
        }
    }

    fn root(&mut self, p: usize) -> usize {
        let mut n = p;
        while self.id[n] != n {
            // path compression!
            // point every node in path to it's grandparent
            // thereby halving path length
            self.id[n] = self.id[self.id[n]];
            n = self.id[n]
        }
        n
    }

    pub fn connected(&mut self, p: usize, q: usize) -> bool {
        self.root(p) == self.root(q)
    }

    pub fn union(&mut self, p: usize, q: usize) {
        let i = self.root(p);
        let j = self.root(q);
        if i == j {
            return
        }
        if self.sz[i] < self.sz[j] {
            self.id[i] = j;
            self.sz[j] += self.sz[i];
        } else {
            self.id[j] = i;
            self.sz[i] += self.sz[j];
        }
    }
}

// #[cfg(test)]
// mod tests {
//     #[test]
//     fn it_works() {
        
//     }
// }